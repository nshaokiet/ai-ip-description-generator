import { DatabaseSync, type SQLInputValue } from 'node:sqlite';
import * as c from './v2-contracts.js';
import { computeMergeGate } from './v2-merge-gate.js';

type Row = Record<string, string | number | null>;
type ViewRow = Record<string, string | number | null | boolean>;
const reviewRole = (type:string) => type==='SECURITY' ? 'SECURITY_REVIEWER' : 'QUALITY_REVIEWER';

// All identities and provenance here are recorded claims, not authenticated facts.
// B3 computes gates from recorded claims; no external verifier is installed.
export class V2Store {
  constructor(private db:DatabaseSync, private guard:()=>void) {}
  private one(sql:string,...args:SQLInputValue[]):Row|undefined { return this.db.prepare(sql).get(...args) as Row|undefined; }
  private all(sql:string,...args:SQLInputValue[]):Row[] { return this.db.prepare(sql).all(...args) as Row[]; }
  private tx<T>(fn:()=>T):T {
    this.db.exec('BEGIN IMMEDIATE');
    try { const result=fn(); this.db.exec('COMMIT'); return result; }
    catch(error) { this.db.exec('ROLLBACK'); throw error; }
  }
  private snapshot<T>(fn:()=>T):T { return this.db.isTransaction ? fn() : this.tx(fn); }
  getMergeGate(taskId:string):ReturnType<typeof computeMergeGate> {
    if (this.db.isTransaction) return computeMergeGate(this.db,taskId);
    this.db.exec('BEGIN');
    try { const result=computeMergeGate(this.db,taskId);this.db.exec('COMMIT');return result; }
    catch(error) {this.db.exec('ROLLBACK');throw error;}
  }
  private task(taskId:string):Row {
    const t=this.one('SELECT * FROM tasks WHERE id=?',taskId);
    if (!t) throw new Error('Unknown task: '+taskId);
    return t;
  }
  workflow(taskId:string):Row|undefined { return this.one('SELECT * FROM task_workflow WHERE task_id=?',taskId); }
  private enrolled(taskId:string):Row {
    this.task(taskId);
    const row=this.workflow(taskId);
    if (!row || row.workflow_version!=='2') throw new Error('Explicit V2 enrollment required');
    return row;
  }
  private assignment(taskId:string, assignmentId:number, role?:string):Row {
    const row=this.one('SELECT * FROM task_assignments WHERE task_id=? AND id=?',taskId,assignmentId);
    if (!row || row.status!=='ACTIVE' || (role && row.role!==role)) throw new Error('Active matching role assignment required');
    return row;
  }
  private frozen(taskId:string,specSha?:string):Row {
    const row=this.one("SELECT * FROM task_specs WHERE task_id=? AND status='FROZEN'",taskId);
    if (!row || (specSha && row.spec_sha!==specSha)) throw new Error('Current FROZEN spec SHA required');
    return row;
  }
  candidate(taskId:string):Row|undefined {
    // Never infer the candidate from implementation history, order, or timestamps.
    return this.one(`SELECT e.* FROM task_workflow w JOIN implementation_evidence e
      ON e.id=w.current_implementation_evidence_id AND e.task_id=w.task_id WHERE w.task_id=?`,taskId);
  }
  private target(taskId:string,specSha:string,baseSha:string,implSha:string):Row {
    this.frozen(taskId,specSha);
    const row=this.candidate(taskId);
    if (!row || row.spec_sha!==specSha || row.base_sha!==baseSha || row.implementation_sha!==implSha)
      throw new Error('Review must target exact current task/spec/base/implementation candidate');
    return row;
  }
  enroll(input:c.Enrollment):Row {
    const p=c.enrollSchema.parse(input);
    return this.tx(()=>{
      const task=this.task(p.task_id), old=this.workflow(p.task_id);
      if (old) {
        if (old.workflow_version!=='2' || old.risk_class!==p.risk_class || old.authorization_ref!==p.authorization_ref || old.activation_commit!==p.activation_commit)
          throw new Error('Conflicting enrollment');
        return old;
      }
      if (!['PLANNED','APPROVED'].includes(String(task.status)) || task.owner!==null)
        throw new Error('Enrollment is prospective; task has existing execution/history');
      if (this.one('SELECT id FROM progress WHERE task_id=? UNION ALL SELECT id FROM checkpoints WHERE task_id=? LIMIT 1',p.task_id,p.task_id))
        throw new Error('Historical V1 task cannot be enrolled');
      this.db.prepare("INSERT INTO task_workflow(task_id,workflow_version,risk_class,authorization_ref,activation_commit,created_at) VALUES (?,'2',?,?,?,?)")
        .run(p.task_id,p.risk_class,p.authorization_ref,p.activation_commit,Date.now());
      return this.enrolled(p.task_id);
    });
  }
  assignRole(input:c.AssignmentInput):Row {
    const p=c.assignmentSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard();
      const current=this.one("SELECT * FROM task_assignments WHERE task_id=? AND role=? AND status IN ('ASSIGNED','ACTIVE')",p.task_id,p.role);
      if (current && current.agent_id===p.agent_id && current.status===p.status) {
        const audit=this.one("SELECT payload FROM progress WHERE task_id=? AND json_extract(payload,'$.assignment_id')=? ORDER BY id DESC LIMIT 1",p.task_id,current.id!);
        if (!audit || JSON.parse(String(audit.payload)).authorization_ref!==p.authorization_ref) throw new Error('Assignment authorization conflict');
        return current;
      }
      if (current && current.id!==p.expected_assignment_id) throw new Error('Assignment conflict: expected current assignment');
      const expected=p.expected_assignment_id===null ? undefined : this.one('SELECT * FROM task_assignments WHERE id=? AND task_id=? AND role=?',p.expected_assignment_id,p.task_id,p.role);
      if (p.expected_assignment_id!==null && !expected) throw new Error('Assignment conflict: invalid replacement identity');
      if (expected && expected.status==='SUPERSEDED') throw new Error('Assignment conflict: already superseded');
      if (current && current.agent_id===p.agent_id && current.status==='ASSIGNED' && p.status==='ACTIVE') {
        this.db.prepare("UPDATE task_assignments SET status='ACTIVE',started_at=? WHERE id=?").run(Date.now(),current.id!);
        return this.assignment(p.task_id,Number(current.id));
      }
      if (expected) {
        if (p.role==='IMPLEMENTER' && expected.lease_expiry!==null && Number(expected.lease_expiry)>Date.now())
          throw new Error('Cannot supersede live implementation lease');
        this.db.prepare("UPDATE task_assignments SET status='SUPERSEDED',completed_at=? WHERE id=?").run(Date.now(),expected.id!);
      }
      const version=Number(this.one('SELECT COALESCE(MAX(assignment_version),0)+1 AS v FROM task_assignments WHERE task_id=? AND role=?',p.task_id,p.role)!.v);
      const result=this.db.prepare('INSERT INTO task_assignments(task_id,role,agent_id,status,assignment_version,assigned_at,started_at) VALUES (?,?,?,?,?,?,?)')
        .run(p.task_id,p.role,p.agent_id,p.status,version,Date.now(),p.status==='ACTIVE'?Date.now():null);
      // Existing progress persistence carries authorization/actor attribution without a second assignment schema.
      this.db.prepare('INSERT INTO progress(task_id,owner,payload,created_at) VALUES (?,?,?,?)')
        .run(p.task_id,p.actor_id,JSON.stringify({milestone:'V2 role assigned',assignment_id:Number(result.lastInsertRowid),authorization_ref:p.authorization_ref,actor_type:p.actor_type}),Date.now());
      return this.one('SELECT * FROM task_assignments WHERE id=?',Number(result.lastInsertRowid))!;
    });
  }
  getAssignments(taskId:string):Row[] { this.enrolled(taskId); return this.all('SELECT * FROM task_assignments WHERE task_id=? ORDER BY role,assignment_version',taskId); }
  submitSpec(input:c.SpecInput):Row {
    const p=c.specSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard(); this.assignment(p.task_id,p.assignment_id,'PLANNER');
      const old=this.one('SELECT * FROM task_specs WHERE task_id=? AND (spec_version=? OR spec_sha=?)',p.task_id,p.spec_version,p.spec_sha);
      if (old) {
        if (old.spec_version!==p.spec_version || old.spec_sha!==p.spec_sha || old.artifact_path!==p.artifact_path || (['DRAFT','READY'].includes(String(old.status)) && old.authorization_ref!==p.authorization_ref))
          throw new Error('Spec identity collision');
        if (old.status===p.status || old.status==='FROZEN') return old;
        if (old.status!=='DRAFT' || p.status!=='READY') throw new Error('Invalid spec transition');
        this.db.prepare("UPDATE task_specs SET status='READY' WHERE id=?").run(old.id!);
        return this.one('SELECT * FROM task_specs WHERE id=?',old.id!)!;
      }
      const r=this.db.prepare('INSERT INTO task_specs(task_id,spec_version,spec_sha,status,authorization_ref,artifact_path,created_at) VALUES (?,?,?,?,?,?,?)')
        .run(p.task_id,p.spec_version,p.spec_sha,p.status,p.authorization_ref,p.artifact_path,Date.now());
      return this.one('SELECT * FROM task_specs WHERE id=?',Number(r.lastInsertRowid))!;
    });
  }
  freezeSpec(input:c.FreezeInput):Row {
    const p=c.freezeSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard();
      if (this.one("SELECT id FROM task_assignments WHERE task_id=? AND role='PLANNER' AND agent_id=?",p.task_id,p.actor_id))
        throw new Error('Planner cannot self-authorize freeze');
      const spec=this.one('SELECT * FROM task_specs WHERE task_id=? AND spec_version=? AND spec_sha=?',p.task_id,p.spec_version,p.spec_sha);
      if (!spec || !['READY','FROZEN'].includes(String(spec.status))) throw new Error('READY exact committed specification required');
      const approval=this.one("SELECT * FROM evidence_verifications WHERE id=? AND task_id=? AND subject_type='HUMAN_AUTHORIZATION' AND subject_key=?",p.approval_verification_id,p.task_id,p.approval_ref);
      if (!approval || approval.decision!=='ATTEST' || approval.verification_level==='UNVERIFIED' ||
          !approval.verification_source || !approval.verification_reference ||
          this.one('SELECT id FROM evidence_verifications WHERE supersedes_verification_id=?',p.approval_verification_id))
        throw new Error('Current explicit Human authorization provenance required');
      const metadata=JSON.parse(String(approval.metadata_json ?? '{}')) as Record<string,unknown>;
      if (metadata.human_authorized!==true || metadata.committed_artifact_exists!==true || metadata.spec_sha!==p.spec_sha ||
          metadata.spec_version!==p.spec_version || metadata.artifact_path!==spec.artifact_path)
        throw new Error('Authorization must cover exact committed artifact/version/SHA');
      const current=this.one("SELECT * FROM task_specs WHERE task_id=? AND status='FROZEN'",p.task_id);
      if (current?.id===spec.id && spec.authorization_ref===p.approval_ref) return spec;
      if ((current?.id ?? null)!==p.expected_frozen_spec_id) throw new Error('Frozen spec conflict');
      if (current) this.db.prepare("UPDATE task_specs SET status='SUPERSEDED',superseded_at=? WHERE id=?").run(Date.now(),current.id!);
      this.db.prepare("UPDATE task_specs SET status='FROZEN',authorization_ref=?,frozen_at=? WHERE id=?").run(p.approval_ref,Date.now(),spec.id!);
      // Retain the pointer/history. A spec change requires an explicit new implementation start.
      if (current && this.one("SELECT id FROM tasks WHERE id=? AND status IN ('CLAIMED','IN_PROGRESS','IMPLEMENTED','AWAITING_REVIEW','REVIEW_CHANGES_REQUIRED')",p.task_id)) {
        this.db.prepare("UPDATE tasks SET status='APPROVED',owner=NULL,branch=NULL,worktree=NULL,lease_start=NULL,lease_expiry=NULL WHERE id=?").run(p.task_id);
        this.db.prepare("UPDATE task_assignments SET lease_start=NULL,lease_expiry=NULL WHERE task_id=? AND role='IMPLEMENTER' AND status='ACTIVE'").run(p.task_id);
      }
      return this.one('SELECT * FROM task_specs WHERE id=?',spec.id!)!;
    });
  }
  getSpec(taskId:string,version?:string):Row[] { this.enrolled(taskId); return version ? this.all('SELECT * FROM task_specs WHERE task_id=? AND spec_version=?',taskId,version) : this.all('SELECT * FROM task_specs WHERE task_id=? ORDER BY id',taskId); }
  startImplementation(input:c.StartInput):Row {
    const p=c.startSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard(); this.frozen(p.task_id,p.spec_sha);
      this.recoverExpired();
      const a=this.assignment(p.task_id,p.implementer_assignment_id,'IMPLEMENTER'), t=this.task(p.task_id);
      if (p.branch==='main' || p.branch.startsWith('refs/heads/main')) throw new Error('Implementation cannot lease main');
      if (t.blockers || (t.frozen_until && Number(t.frozen_until)>Date.now()) || this.one("SELECT d.task_id FROM dependencies d JOIN tasks t ON t.id=d.requires_id WHERE d.task_id=? AND t.status!='COMPLETED'",p.task_id))
        throw new Error('Task blocked, frozen or dependencies incomplete');
      if (t.status==='IN_PROGRESS' && t.owner===a.agent_id && t.branch===p.branch && t.worktree===p.worktree && Number(t.lease_expiry)>Date.now()) return a;
      if (!['APPROVED','CLAIMED'].includes(String(t.status)) || (t.owner!==null && t.owner!==a.agent_id)) throw new Error('Task not eligible for implementation');
      if (this.one("SELECT id FROM tasks WHERE id!=? AND status IN ('CLAIMED','IN_PROGRESS') AND lease_expiry>? AND (branch=? OR worktree=?)",p.task_id,Date.now(),p.branch,p.worktree))
        throw new Error('Branch or worktree already leased');
      const now=Date.now(), expiry=now+p.lease_minutes*60000;
      this.db.prepare("UPDATE task_assignments SET branch=?,worktree=?,lease_start=?,lease_expiry=?,started_at=COALESCE(started_at,?) WHERE id=?")
        .run(p.branch,p.worktree,now,expiry,now,a.id!);
      this.db.prepare("UPDATE tasks SET status='IN_PROGRESS',owner=?,branch=?,worktree=?,lease_start=?,lease_expiry=? WHERE id=?")
        .run(a.agent_id!,p.branch,p.worktree,now,expiry,p.task_id);
      return this.assignment(p.task_id,p.implementer_assignment_id,'IMPLEMENTER');
    });
  }
  validateOwner(taskId:string,owner:string):Row {
    const a=this.one("SELECT * FROM task_assignments WHERE task_id=? AND role='IMPLEMENTER' AND agent_id=? AND status='ACTIVE'",taskId,owner);
    const t=this.task(taskId);
    if (!a || Number(a.lease_expiry)<=Date.now() || a.lease_expiry===null || a.branch!==t.branch || a.worktree!==t.worktree || a.lease_expiry!==t.lease_expiry)
      throw new Error('Active Implementer assignment and matching lease required');
    return a;
  }
  syncLease(taskId:string,expiry:number|null,status?:string):void {
    this.db.prepare(`UPDATE task_assignments SET lease_expiry=?,status=COALESCE(?,status),completed_at=CASE WHEN ?='COMPLETED' THEN ? ELSE completed_at END
      WHERE task_id=? AND role='IMPLEMENTER' AND status='ACTIVE'`).run(expiry,status??null,status??null,Date.now(),taskId);
  }
  recoverExpired():void {
    this.db.prepare("UPDATE task_assignments SET status='BLOCKED',completed_at=? WHERE role='IMPLEMENTER' AND status='ACTIVE' AND lease_expiry<=?").run(Date.now(),Date.now());
    this.db.prepare("UPDATE tasks SET status='APPROVED',owner=NULL,branch=NULL,worktree=NULL,lease_start=NULL,lease_expiry=NULL WHERE status IN ('CLAIMED','IN_PROGRESS') AND lease_expiry<=?").run(Date.now());
  }
  recordImplementation(input:c.ImplementationInput):Row {
    const p=c.implementationSchema.parse(input);
    return this.tx(()=>{
      const w=this.enrolled(p.task_id); this.guard(); this.frozen(p.task_id,p.spec_sha);
      const a=this.one('SELECT * FROM task_assignments WHERE id=? AND task_id=? AND role=?',p.assignment_id,p.task_id,'IMPLEMENTER');
      if (!a) throw new Error('Implementer assignment required');
      let row=this.one('SELECT * FROM implementation_evidence WHERE task_id=? AND implementation_sha=?',p.task_id,p.implementation_sha);
      if (row && (row.spec_sha!==p.spec_sha || row.base_sha!==p.base_sha || row.evidence_ref!==p.evidence_ref || row.recorded_by_assignment_id!==p.assignment_id))
        throw new Error('Conflicting immutable implementation fields');
      // A timed-out winning request remains retryable after finish/release, but cannot advance anything.
      if (row && w.current_implementation_evidence_id===row.id) return row;
      this.assignment(p.task_id,p.assignment_id,'IMPLEMENTER'); this.validateOwner(p.task_id,String(a.agent_id));
      if (this.task(p.task_id).status!=='IN_PROGRESS') throw new Error('Implementation must be started');
      if (!row) {
        const r=this.db.prepare('INSERT INTO implementation_evidence(task_id,spec_sha,base_sha,implementation_sha,evidence_ref,recorded_by_assignment_id,created_at) VALUES (?,?,?,?,?,?,?)')
          .run(p.task_id,p.spec_sha,p.base_sha,p.implementation_sha,p.evidence_ref,p.assignment_id,Date.now());
        row=this.one('SELECT * FROM implementation_evidence WHERE id=?',Number(r.lastInsertRowid))!;
      }
      if (w.current_implementation_evidence_id!==p.expected_current_implementation_evidence_id) throw new Error('Candidate conflict: stale expected current');
      const changed=this.db.prepare('UPDATE task_workflow SET current_implementation_evidence_id=? WHERE task_id=? AND current_implementation_evidence_id IS ?')
        .run(row.id!,p.task_id,p.expected_current_implementation_evidence_id);
      if (Number(changed.changes)!==1) throw new Error('Candidate conflict');
      return row;
    });
  }
  recordCi(input:c.CiInput):Row {
    const p=c.ciSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard();
      if (!this.one('SELECT id FROM implementation_evidence WHERE task_id=? AND implementation_sha=?',p.task_id,p.implementation_sha)) throw new Error('Unknown implementation SHA');
      const old=this.one('SELECT * FROM ci_evidence WHERE task_id=? AND reference=?',p.task_id,p.reference);
      if (old) {
        for (const key of ['implementation_sha','status','reference','source','recorded_by'] as const) if (old[key]!==p[key]) throw new Error('Conflicting CI reference');
        if (p.created_at!==undefined && old.created_at!==p.created_at) throw new Error('Conflicting CI timestamp');
        return old;
      }
      const r=this.db.prepare('INSERT INTO ci_evidence(task_id,implementation_sha,status,reference,source,recorded_by,created_at) VALUES (?,?,?,?,?,?,?)')
        .run(p.task_id,p.implementation_sha,p.status,p.reference,p.source,p.recorded_by,p.created_at??Date.now());
      return this.one('SELECT * FROM ci_evidence WHERE id=?',Number(r.lastInsertRowid))!;
    });
  }
  private independent(taskId:string,assignmentId:number,type:string):Row {
    const a=this.assignment(taskId,assignmentId,reviewRole(type));
    if (this.one("SELECT id FROM task_assignments WHERE task_id=? AND role='IMPLEMENTER' AND agent_id=? AND status IN ('ASSIGNED','ACTIVE')",taskId,a.agent_id!))
      throw new Error('Reviewer must be independent of Implementer');
    const otherRole=type==='SECURITY'?'QUALITY_REVIEWER':'SECURITY_REVIEWER';
    if (this.one("SELECT id FROM task_assignments WHERE task_id=? AND role=? AND agent_id=? AND status IN ('ASSIGNED','ACTIVE')",taskId,otherRole,a.agent_id!))
      throw new Error('Security and Quality require separate role/session identities');
      const candidate=this.candidate(taskId);
    if (candidate?.recorded_by_assignment_id) {
      const implementer=this.one('SELECT agent_id FROM task_assignments WHERE id=?',candidate.recorded_by_assignment_id);
      if (implementer?.agent_id===a.agent_id) throw new Error('Reviewer authored this candidate');
    }
    if (candidate && this.one('SELECT review_id FROM reviews WHERE task_id=? AND implementation_sha=? AND review_type!=? AND reviewer=?',taskId,candidate.implementation_sha!,type,a.agent_id!))
      throw new Error('Security and Quality verdicts require independent attribution');
    return a;
  }
  startReview(input:c.ReviewStartInput):Row {
    const p=c.reviewStartSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard(); this.independent(p.task_id,p.assignment_id,p.review_type);
      const e=this.target(p.task_id,p.spec_sha,p.base_sha,p.implementation_sha);
      const old=this.one('SELECT * FROM review_attempts WHERE task_id=? AND review_type=? AND implementation_evidence_id=? AND assignment_id=? AND submitted_review_id IS NULL',p.task_id,p.review_type,e.id!,p.assignment_id);
      if (old) return old;
      const attempt=Number(this.one(`SELECT COALESCE(MAX(attempt),0)+1 AS n FROM (
        SELECT attempt FROM review_attempts WHERE task_id=? AND review_type=? AND implementation_sha=?
        UNION ALL SELECT attempt FROM reviews WHERE task_id=? AND review_type=? AND implementation_sha=?)`,p.task_id,p.review_type,p.implementation_sha,p.task_id,p.review_type,p.implementation_sha)!.n);
      const r=this.db.prepare('INSERT INTO review_attempts(task_id,review_type,assignment_id,implementation_evidence_id,spec_sha,base_sha,implementation_sha,attempt,started_at) VALUES (?,?,?,?,?,?,?,?,?)')
        .run(p.task_id,p.review_type,p.assignment_id,e.id!,p.spec_sha,p.base_sha,p.implementation_sha,attempt,Date.now());
      this.db.prepare("UPDATE tasks SET status='AWAITING_REVIEW' WHERE id=? AND status='IMPLEMENTED'").run(p.task_id);
      return this.one('SELECT * FROM review_attempts WHERE id=?',Number(r.lastInsertRowid))!;
    });
  }
  submitReview(input:c.ReviewSubmitInput):Row {
    const p=c.reviewSubmitSchema.parse(input);
    return this.tx(()=>{
      this.guard();
      const attempt=this.one('SELECT * FROM review_attempts WHERE id=?',p.review_id);
      if (!attempt || attempt.assignment_id!==p.assignment_id) throw new Error('Correct started review assignment required');
      const taskId=String(attempt.task_id);
      this.enrolled(taskId);
      if (p.verdict==='PASS' && (p.tracked_files_modified || p.blocking_findings!==0)) throw new Error('Clean independent PASS required: no tracked modifications or blocking findings');
      const fields={verdict:p.verdict,findings_ref:p.findings_ref,blocking_findings:p.blocking_findings,evidence_ref:p.evidence_ref,artifact_path:p.artifact_path,reviewer:p.reviewer,model_profile:p.model_profile??null,tracked_files_modified:p.tracked_files_modified?1:0};
      if (attempt.submitted_review_id!==null) {
        const old=this.one('SELECT * FROM reviews WHERE review_id=?',attempt.submitted_review_id!)!;
        if (Object.entries(fields).some(([k,v])=>old[k]!==v)) throw new Error('Submitted review is immutable; start new attempt');
        return old;
      }
      const a=this.independent(taskId,p.assignment_id,String(attempt.review_type));
      if (a.agent_id!==p.reviewer) throw new Error('Reviewer attribution must match assigned agent');
      this.target(taskId,String(attempt.spec_sha),String(attempt.base_sha),String(attempt.implementation_sha));
      const r=this.db.prepare(`INSERT INTO reviews(task_id,review_type,reviewer_assignment_id,spec_sha,base_sha,implementation_sha,attempt,verdict,findings_ref,blocking_findings,evidence_ref,artifact_path,reviewer,model_profile,created_at,tracked_files_modified)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`).run(taskId,attempt.review_type!,p.assignment_id,attempt.spec_sha!,attempt.base_sha!,attempt.implementation_sha!,attempt.attempt!,p.verdict,p.findings_ref,p.blocking_findings,p.evidence_ref,p.artifact_path,p.reviewer,p.model_profile??null,Date.now(),p.tracked_files_modified?1:0);
      this.db.prepare('UPDATE review_attempts SET submitted_review_id=? WHERE id=? AND submitted_review_id IS NULL').run(Number(r.lastInsertRowid),p.review_id);
      if (p.verdict==='REQUEST_CHANGES') this.db.prepare("UPDATE tasks SET status='REVIEW_CHANGES_REQUIRED' WHERE id=? AND status IN ('IMPLEMENTED','AWAITING_REVIEW')").run(taskId);
      return this.one('SELECT * FROM reviews WHERE review_id=?',Number(r.lastInsertRowid))!;
    });
  }
  recordVerification(input:c.VerificationInput):Row {
    const p=c.verificationSchema.parse(input);
    return this.tx(()=>{
      this.enrolled(p.task_id); this.guard();
      const internal:Record<string,[string,string,string]>={SPECIFICATION:['task_specs','id','task_spec_id'],IMPLEMENTATION:['implementation_evidence','id','implementation_evidence_id'],CI:['ci_evidence','id','ci_evidence_id'],SECURITY_REVIEW:['reviews','review_id','review_id'],QUALITY_REVIEW:['reviews','review_id','review_id']};
      const kind=internal[p.subject_type];
      if (kind) {
        if (!p.applicable_subject_id || p.subject_key!==String(p.applicable_subject_id)) throw new Error('Canonical internal subject identity required');
        const subject=this.one(`SELECT * FROM ${kind[0]} WHERE ${kind[1]}=? AND task_id=?`,p.applicable_subject_id,p.task_id);
        if (!subject || (p.subject_type.endsWith('_REVIEW') && subject.review_type!==p.subject_type.replace('_REVIEW',''))) throw new Error('Subject type/task mismatch');
      } else {
        if (p.applicable_subject_id!==undefined) throw new Error('External subject cannot have internal ID');
        if (p.subject_type==='PR_BRANCH_STATE' && !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+#[1-9][0-9]*@[a-f0-9]{40}$/.test(p.subject_key)) throw new Error('Canonical repo#PR@head key required');
        if (p.subject_type==='MERGE_RESULT' && !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+@[a-f0-9]{40}$/.test(p.subject_key)) throw new Error('Canonical repo@merge key required');
        if (p.subject_type==='PR_BRANCH_STATE' || p.subject_type==='MERGE_RESULT') p.subject_key=p.subject_key.toLowerCase();
      }
      if (p.verification_level==='VERIFIED' && (!p.verifier_type || !p.verifier_id || !p.verification_source || !p.verification_reference || p.verified_at===undefined))
        throw new Error('VERIFIED requires explicit verifier/source/reference/time provenance; no trust promotion');
      if (p.decision==='REVOKE' && p.verification_level!=='UNVERIFIED') throw new Error('REVOKE must be UNVERIFIED');
      const chain=this.all('SELECT * FROM evidence_verifications WHERE task_id=? AND subject_type=? AND subject_key=? ORDER BY verification_version',p.task_id,p.subject_type,p.subject_key);
      for (let i=0;i<chain.length;i++) if (chain[i]!.verification_version!==i+1 || chain[i]!.supersedes_verification_id!==(i===0?null:chain[i-1]!.id)) throw new Error('Invalid verification chain');
      const last=chain.at(-1);
      if ((last?.id??null)!==p.expected_effective_verification_id) throw new Error('Verification conflict: stale expected chain');
      const r=this.db.prepare(`INSERT INTO evidence_verifications(task_id,subject_type,subject_key,task_spec_id,implementation_evidence_id,ci_evidence_id,review_id,verification_version,supersedes_verification_id,decision,verification_level,recorded_by,verifier_type,verifier_id,verification_source,verification_reference,verified_at,created_at,metadata_json)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`).run(p.task_id,p.subject_type,p.subject_key,kind?.[2]==='task_spec_id'?p.applicable_subject_id!:null,kind?.[2]==='implementation_evidence_id'?p.applicable_subject_id!:null,kind?.[2]==='ci_evidence_id'?p.applicable_subject_id!:null,kind?.[2]==='review_id'?p.applicable_subject_id!:null,chain.length+1,last?.id??null,p.decision,p.verification_level,p.recorded_by,p.verifier_type??null,p.verifier_id??null,p.verification_source??null,p.verification_reference??null,p.verified_at??null,Date.now(),p.metadata_json??null);
      return this.one('SELECT * FROM evidence_verifications WHERE id=?',Number(r.lastInsertRowid))!;
    });
  }
  private current(row:Row,taskId:string):boolean {
    const candidate=this.candidate(taskId), spec=this.one("SELECT * FROM task_specs WHERE task_id=? AND status='FROZEN'",taskId);
    return !!candidate && !!spec && candidate.spec_sha===spec.spec_sha && row.implementation_sha===candidate.implementation_sha && (!row.spec_sha || row.spec_sha===spec.spec_sha);
  }
  reviewStatus(taskId:string,implementationSha?:string):object {
    return this.snapshot(()=>this.reviewStatusUnsafe(taskId,implementationSha));
  }
  private reviewStatusUnsafe(taskId:string,implementationSha?:string):object {
    this.enrolled(taskId);
    const history=this.all('SELECT * FROM reviews WHERE task_id=? ORDER BY review_type,implementation_sha,attempt',taskId).map<ViewRow>(r=>{
      const a=this.one('SELECT * FROM task_assignments WHERE id=?',r.reviewer_assignment_id!);
      const isCurrent=this.current(r,taskId) && a?.status==='ACTIVE';
      return {...r,targets_current_candidate:this.current(r,taskId),current:isCurrent,stale:!isCurrent};
    });
    const starts=this.all('SELECT * FROM review_attempts WHERE task_id=? AND submitted_review_id IS NULL ORDER BY attempt',taskId).map<ViewRow>(r=>({...r,current:this.current(r,taskId)&&this.one("SELECT id FROM task_assignments WHERE id=? AND status='ACTIVE'",r.assignment_id!)!==undefined}));
    const summary=(type:string)=>{
      const targetSha=implementationSha??this.candidate(taskId)?.implementation_sha;
      const results=history.filter(r=>r.review_type===type && r.implementation_sha===targetSha);
      const pending=starts.filter(r=>r.review_type===type && r.implementation_sha===targetSha && r.current);
      const latest=results.at(-1), active=pending.at(-1);
      if (active && (!latest || Number(active.attempt)>Number(latest.attempt))) return {...active,status:'IN_PROGRESS',stale:!active.current};
      return latest ? {...latest,status:latest.verdict} : {status:'NOT_STARTED',implementation_sha:targetSha??null};
    };
    return {security:summary('SECURITY'),quality:summary('QUALITY'),history:implementationSha?history.filter(r=>r.implementation_sha===implementationSha):history,in_progress:starts};
  }
  state(taskId:string):object {
    return this.snapshot(()=>this.stateUnsafe(taskId));
  }
  private stateUnsafe(taskId:string):object {
    const workflow=this.enrolled(taskId);
    const candidate=this.candidate(taskId);
    const ci=this.all('SELECT * FROM ci_evidence WHERE task_id=? ORDER BY id',taskId).map(row=>({...row,current:this.current(row,taskId),stale:!this.current(row,taskId)}));
    return {workflow_version:2,workflow,risk_class:workflow.risk_class,assignments:this.getAssignments(taskId),
      frozen_spec:this.one("SELECT * FROM task_specs WHERE task_id=? AND status='FROZEN'",taskId)??null,
      current_implementation:candidate?{...candidate,current:this.current(candidate,taskId),stale:!this.current(candidate,taskId)}:null,ci_evidence:ci,reviews:this.reviewStatus(taskId),
      verification_records:this.all('SELECT * FROM evidence_verifications WHERE task_id=? ORDER BY subject_type,subject_key,verification_version',taskId).map(row=>{
        let applicable:boolean|null=null;
        if (row.task_spec_id!==null) applicable=this.one("SELECT id FROM task_specs WHERE task_id=? AND status='FROZEN' AND id=?",taskId,row.task_spec_id!)!==undefined;
        if (row.implementation_evidence_id!==null) applicable=!!candidate && row.implementation_evidence_id===workflow.current_implementation_evidence_id && this.current(candidate,taskId);
        if (row.ci_evidence_id!==null) {
          const ci=this.one('SELECT * FROM ci_evidence WHERE id=? AND task_id=?',row.ci_evidence_id!,taskId);
          applicable=!!ci && this.current(ci,taskId);
        }
        if (row.review_id!==null) {
          const review=this.one('SELECT * FROM reviews WHERE review_id=? AND task_id=?',row.review_id!,taskId);
          applicable=!!review && this.current(review,taskId) && !!this.one("SELECT id FROM task_assignments WHERE id=? AND status='ACTIVE'",review.reviewer_assignment_id!);
        }
        return {...row,applicable,stale:applicable===null?null:!applicable,authority_validated:false};
      }),
      merge_gate:this.getMergeGate(taskId),
      trust_boundary:'RECORDED CLAIMS; provenance is not independently authenticated',workflow_v2_governance:'NOT ACTIVATED'};
  }
  checkpointAssignment(taskId:string,owner:string,role:string,assignmentId:number):Row {
    this.enrolled(taskId); const a=this.assignment(taskId,assignmentId,role);
    if (a.agent_id!==owner) throw new Error('Checkpoint actor must match role assignment');
    return a;
  }
}
