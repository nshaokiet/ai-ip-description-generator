import type { DatabaseSync, SQLInputValue } from 'node:sqlite';
import { mergePolicySchema, type MergePolicy } from './v2-contracts.js';

type Row = Record<string, string | number | null>;
type Level = 'UNVERIFIED' | 'RECORDED' | 'VERIFIED';
const types = ['HUMAN_AUTHORIZATION','SPECIFICATION','IMPLEMENTATION','CI',
  'SECURITY_REVIEW','QUALITY_REVIEW','PR_BRANCH_STATE','MERGE_RESULT'] as const;
type Subject = typeof types[number];
const internal:Partial<Record<Subject,[string,string,string]>> = {
  SPECIFICATION:['task_specs','id','task_spec_id'],
  IMPLEMENTATION:['implementation_evidence','id','implementation_evidence_id'],
  CI:['ci_evidence','id','ci_evidence_id'], SECURITY_REVIEW:['reviews','review_id','review_id'],
  QUALITY_REVIEW:['reviews','review_id','review_id']
};
const fks = ['task_spec_id','implementation_evidence_id','ci_evidence_id','review_id'];
const sha = (v:unknown):v is string => typeof v==='string' && /^[a-f0-9]{40}$/.test(v);
const nonempty = (v:unknown):v is string => typeof v==='string' && !!v.trim();

// §18.1 responsibilities, not a registry of trusted caller-supplied identities.
// No approved source adapter exists in B3. In particular admin metadata cannot
// opt into an accepted verifier, including by copying one of these descriptions.
export const sourcePolicy:Record<Subject,{source:string;verifier:string;adapter_available:false;fresh_check_required:boolean}> = {
  HUMAN_AUTHORIZATION:{source:'Approved governance artifact / Human-controlled authorization',verifier:'Human authority / approved governance verifier',adapter_available:false,fresh_check_required:false},
  SPECIFICATION:{source:'Git exact spec/version/SHA plus freeze authorization',verifier:'Git verifier with freeze-authorization reconciliation',adapter_available:false,fresh_check_required:false},
  IMPLEMENTATION:{source:'Git exact implementation/base SHA',verifier:'Git repository / Git-host verifier',adapter_available:false,fresh_check_required:false},
  CI:{source:'CI provider exact run and head SHA',verifier:'CI provider integration / authoritative run check',adapter_available:false,fresh_check_required:false},
  SECURITY_REVIEW:{source:'Canonical immutable Security artifact and valid assignment',verifier:'Approved review-artifact / assignment verifier',adapter_available:false,fresh_check_required:false},
  QUALITY_REVIEW:{source:'Canonical immutable Quality artifact and valid assignment',verifier:'Approved review-artifact / assignment verifier',adapter_available:false,fresh_check_required:false},
  PR_BRANCH_STATE:{source:'Git host authoritative PR/ref state',verifier:'Immediate authoritative Git-host pre-merge check',adapter_available:false,fresh_check_required:true},
  MERGE_RESULT:{source:'Git-host merge result plus final-main reconciliation',verifier:'Git-host integration plus exact final-main check',adapter_available:false,fresh_check_required:false}
};

export type EffectiveVerification = {
  subject_type:string; subject_key:string; subject_id:number|null; chain_valid:boolean;
  history_ids:number[]; superseded_ids:number[]; terminal_id:number|null;
  verification_level:Level; revoked:boolean; applicable:boolean; stale:boolean;
  authority_validated:false; provenance:Row|null; blockers:string[];
};
export type Gate = {
  gate:string; required:boolean; requirement_status:'REQUIRED'|'NOT_REQUIRED'|'UNRESOLVED';
  provisional_required:boolean; subject_type:Subject|null; subject_key:string|null;
  subject_id:number|null; evidence_present:boolean; applicable:boolean;
  recorded_satisfied:boolean; verification_level:Level; authoritative_satisfied:false;
  stale:boolean; revoked:boolean; effective_verification_id:number|null;
  blockers:string[]; authoritative_blockers:string[]; observed:Row|null;
  expected_authoritative_source:string|null; fresh_check_required:boolean;
};

// Call only inside a transaction; all queries share the caller's one snapshot.
export function computeMergeGate(db:DatabaseSync, taskId:string) {
  if (!db.isTransaction) throw new Error('Merge gate requires a consistent transaction snapshot');
  const all = (sql:string,...args:SQLInputValue[])=>db.prepare(sql).all(...args) as Row[];
  const one = (sql:string,...args:SQLInputValue[])=>db.prepare(sql).get(...args) as Row|undefined;
  const task=one('SELECT * FROM tasks WHERE id=?',taskId);
  if (!task) throw new Error('Unknown task: '+taskId);
  const w=one('SELECT * FROM task_workflow WHERE task_id=?',taskId);
  if (!w) return {task_id:taskId,workflow_version:1,status:'NOT_APPLICABLE',provisional_ready:false,
    authoritative_merge_eligible:false,blockers:['V2_ENROLLMENT_REQUIRED'],workflow_v2_governance:'NOT ACTIVATED'};
  const specs=all("SELECT * FROM task_specs WHERE task_id=? AND status='FROZEN'",taskId);
  const spec=specs.length===1?specs[0]:undefined;
  // The pointer is the sole selector. No history/order/MAX/time fallback.
  const candidate=one('SELECT * FROM implementation_evidence WHERE id=? AND task_id=?',w.current_implementation_evidence_id??null,taskId);
  const F=candidate?.implementation_sha??null;
  const candidateCurrent=!!candidate && !!spec && sha(F) && sha(candidate.base_sha) && candidate.spec_sha===spec.spec_sha;
  const assignments=all('SELECT * FROM task_assignments WHERE task_id=?',taskId);
  const reviews=all('SELECT * FROM reviews WHERE task_id=?',taskId);
  const attempts=all('SELECT * FROM review_attempts WHERE task_id=?',taskId);
  const cis=all('SELECT * FROM ci_evidence WHERE task_id=? ORDER BY id',taskId);
  const reviewApplicable=(r:Row)=>{
    const a=assignments.find(a=>a.id===r.reviewer_assignment_id);
    const author=assignments.find(a=>a.id===candidate?.recorded_by_assignment_id);
    const role=r.review_type==='SECURITY'?'SECURITY_REVIEWER':'QUALITY_REVIEWER';
    return candidateCurrent && r.implementation_sha===F && r.spec_sha===spec?.spec_sha && r.base_sha===candidate?.base_sha &&
      !!a && a.role===role && a.status==='ACTIVE' && a.agent_id===r.reviewer &&
      !!author && author.role==='IMPLEMENTER' && author.agent_id!==r.reviewer &&
      !assignments.some(other=>other.status==='ACTIVE' && other.role!==role &&
        ['IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER'].includes(String(other.role)) && other.agent_id===r.reviewer);
  };
  const verifications=all('SELECT * FROM evidence_verifications WHERE task_id=? ORDER BY subject_type,subject_key,verification_version',taskId);
  const grouped=new Map<string,Row[]>();
  const key=(t:string,k:string)=>JSON.stringify([t,k]);
  for (const r of verifications) {
    const k=key(String(r.subject_type),String(r.subject_key));
    grouped.set(k,[...(grouped.get(k)??[]),r]);
  }
  // Resolve typed identities for EVERY row, including history, not only terminal.
  const validIdentity=(r:Row)=>{
    const t=String(r.subject_type) as Subject, k=String(r.subject_key), kind=internal[t];
    if (!types.includes(t) || r.task_id!==taskId || !nonempty(k)) return false;
    if (kind) {
      if (!Number.isSafeInteger(r[kind[2]]) || Number(r[kind[2]])<=0 || k!==String(r[kind[2]]) || fks.some(f=>f!==kind[2] && r[f]!==null)) return false;
      const subject=one(`SELECT * FROM ${kind[0]} WHERE ${kind[1]}=? AND task_id=?`,r[kind[2]]??null,taskId);
      return !!subject && (!t.endsWith('_REVIEW') || subject.review_type===t.replace('_REVIEW',''));
    }
    if (fks.some(f=>r[f]!==null)) return false;
    if (t==='PR_BRANCH_STATE') return /^[a-z0-9_.-]+\/[a-z0-9_.-]+#[1-9][0-9]*@[a-f0-9]{40}$/.test(k);
    if (t==='MERGE_RESULT') return /^[a-z0-9_.-]+\/[a-z0-9_.-]+@[a-f0-9]{40}$/.test(k);
    return t==='HUMAN_AUTHORIZATION';
  };
  const effective=new Map<string,EffectiveVerification>();
  for (const [k,chain] of grouped) {
    const first=chain[0]!, last=chain.at(-1)!;
    const valid=chain.every((r,i)=>validIdentity(r) && r.verification_version===i+1 &&
      r.supersedes_verification_id===(i===0?null:chain[i-1]!.id) &&
      Number.isSafeInteger(r.id) && Number(r.id)>0 && nonempty(r.recorded_by) &&
      ['ATTEST','REVOKE'].includes(String(r.decision)) && ['UNVERIFIED','RECORDED','VERIFIED'].includes(String(r.verification_level)) &&
      (r.decision!=='REVOKE' || r.verification_level==='UNVERIFIED') &&
      (r.verification_level!=='VERIFIED' || ['verifier_type','verifier_id','verification_source','verification_reference'].every(f=>nonempty(r[f])) &&
        Number.isSafeInteger(r.verified_at) && Number(r.verified_at)>=0)) &&
      new Set(chain.map(r=>r.id)).size===chain.length;
    effective.set(k,{subject_type:String(first.subject_type),subject_key:String(first.subject_key),
      subject_id:internal[first.subject_type as Subject]?Number(first[internal[first.subject_type as Subject]![2]]):null,
      chain_valid:valid,history_ids:chain.map(r=>Number(r.id)),superseded_ids:valid?chain.slice(0,-1).map(r=>Number(r.id)):[],
      terminal_id:valid?Number(last.id):null,verification_level:valid?(last.decision==='REVOKE'?'UNVERIFIED':last.verification_level as Level):'UNVERIFIED',
      revoked:valid && last.decision==='REVOKE',applicable:false,stale:false,authority_validated:false,
      provenance:valid?last:null,blockers:valid?(last.decision==='REVOKE'?['VERIFICATION_REVOKED']:[]):['VERIFICATION_CHAIN_INVALID']});
  }
  const find=(type:Subject,k:string|null)=>k===null?undefined:effective.get(key(type,k));
  const auth=find('HUMAN_AUTHORIZATION',String(w.authorization_ref));
  let policy:MergePolicy|undefined;
  let metadata:Record<string,unknown>|undefined;
  try {
    const parsed:unknown=JSON.parse(String(auth?.provenance?.metadata_json??'null'));
    if (parsed && typeof parsed==='object' && !Array.isArray(parsed)) metadata=parsed as Record<string,unknown>;
    const p=mergePolicySchema.safeParse(metadata?.merge_policy);
    if (p.success) policy=p.data;
  } catch { /* malformed recorded context is an explicit unresolved policy */ }
  const prKey=candidateCurrent && policy?.repository && policy.pr_number?
    `${policy.repository}#${policy.pr_number}@${F}`:null;
  const humanRefs=new Set([String(w.authorization_ref),...(spec?[String(spec.authorization_ref)]:[]),...(policy?.required_human_exception_refs??[])]);
  for (const e of effective.values()) {
    const r=e.provenance, t=e.subject_type;
    if (!e.chain_valid || !r) continue;
    if (t==='HUMAN_AUTHORIZATION') e.applicable=humanRefs.has(e.subject_key);
    if (t==='SPECIFICATION') e.applicable=!!spec && r.task_spec_id===spec.id;
    if (t==='IMPLEMENTATION') e.applicable=candidateCurrent && r.implementation_evidence_id===candidate?.id;
    if (t==='CI') e.applicable=candidateCurrent && cis.some(c=>c.id===r.ci_evidence_id && c.implementation_sha===F);
    if (t.endsWith('_REVIEW')) e.applicable=reviews.some(review=>review.review_id===r.review_id && reviewApplicable(review) &&
      ![...reviews,...attempts].some(next=>next.review_type===review.review_type && next.implementation_sha===F && Number(next.attempt)>Number(review.attempt)));
    if (t==='PR_BRANCH_STATE') e.applicable=prKey!==null && e.subject_key===prKey;
    // Valid post-merge history remains visible, never an inferred current merge.
    if (t==='MERGE_RESULT') e.applicable=false;
    e.stale=!e.applicable;
  }
  const gates:Gate[]=[];
  function gate(name:string,type:Subject|null,k:string|null,observed:Row|null,satisfied:boolean,
    reasons:string[]=[],required=true,provisionalRequired=true,unresolved=false):Gate {
    const e=type?find(type,k):undefined;
    const blockers=[...reasons];
    if (required && !satisfied && blockers.length===0) blockers.push('GATE_UNSATISFIED');
    if (required && e && (!e.chain_valid || e.revoked || e.verification_level==='UNVERIFIED'))
      blockers.push(...(e.blockers.length?e.blockers:['EVIDENCE_UNVERIFIED']));
    if (required && e?.stale) blockers.push('STALE_VERIFICATION');
    if (required && type==='HUMAN_AUTHORIZATION' && e?.provenance &&
      (!nonempty(e.provenance.verification_source) || !nonempty(e.provenance.verification_reference))) blockers.push('HUMAN_AUTHORIZATION_PROVENANCE_MISSING');
    const source=type?sourcePolicy[type]:undefined;
    const authoritativeBlockers:string[]=[];
    if (required && type) {
      if (e?.verification_level!=='VERIFIED') authoritativeBlockers.push(`${type}_NOT_VERIFIED`);
      if (e?.verification_level==='VERIFIED') authoritativeBlockers.push('AUTHORITATIVE_SOURCE_POLICY_UNACCEPTED');
      authoritativeBlockers.push('AUTHORITATIVE_VERIFIER_UNAVAILABLE');
      if (source?.fresh_check_required) authoritativeBlockers.push('FRESH_PREMERGE_CHECK_UNAVAILABLE');
    }
    const result:Gate={gate:name,required,requirement_status:unresolved?'UNRESOLVED':required?'REQUIRED':'NOT_REQUIRED',
      provisional_required:required && provisionalRequired,subject_type:type,subject_key:k,subject_id:e?.subject_id??
        (type && internal[type] && observed?Number(observed[internal[type]![1]]):null),
      evidence_present:observed!==null || !!e,applicable:e?e.applicable:satisfied,
      recorded_satisfied:required?satisfied && blockers.length===0:false,verification_level:e?.verification_level??(observed?'RECORDED':'UNVERIFIED'),
      authoritative_satisfied:false,stale:e?.stale??false,revoked:e?.revoked??false,effective_verification_id:e?.terminal_id??null,
      blockers:required?[...new Set(blockers)]:[],authoritative_blockers:authoritativeBlockers,observed,
      expected_authoritative_source:source?.source??null,fresh_check_required:source?.fresh_check_required??false};
    gates.push(result);return result;
  }
  gate('V2_ENROLLMENT',null,null,w,w.workflow_version==='2' && sha(w.activation_commit),
    w.workflow_version==='2' && sha(w.activation_commit)?[]:['V2_ENROLLMENT_INVALID']);
  const authorized=nonempty(w.authorization_ref) && task.approval_ref===w.authorization_ref && !!auth;
  gate('HUMAN_AUTHORIZATION','HUMAN_AUTHORIZATION',String(w.authorization_ref),auth?.provenance??null,authorized,
    authorized?[]:['HUMAN_AUTHORIZATION_MISSING']);
  gate('RECORDED_POLICY',null,null,auth?.provenance??null,!!policy,policy?[]:['MERGE_POLICY_UNRESOLVED'],true,true,!policy);
  const specValid=!!spec && sha(spec.spec_sha) && nonempty(spec.spec_version) && nonempty(spec.artifact_path);
  gate('SPECIFICATION','SPECIFICATION',spec?String(spec.id):null,spec??null,specValid,
    specValid?[]:[specs.length>1?'FROZEN_SPEC_AMBIGUOUS':'NO_FROZEN_SPEC']);
  if (spec) {
    const freeze=find('HUMAN_AUTHORIZATION',String(spec.authorization_ref));
    let freezeMetadata:Record<string,unknown>|null=null;
    try { freezeMetadata=JSON.parse(String(freeze?.provenance?.metadata_json??'null')) as Record<string,unknown>|null; } catch { /* fail closed */ }
    const covered=!!freeze && freezeMetadata?.human_authorized===true && freezeMetadata.committed_artifact_exists===true &&
      freezeMetadata.spec_sha===spec.spec_sha && freezeMetadata.spec_version===spec.spec_version && freezeMetadata.artifact_path===spec.artifact_path;
    gate('FREEZE_AUTHORIZATION','HUMAN_AUTHORIZATION',String(spec.authorization_ref),freeze?.provenance??null,covered,covered?[]:['FREEZE_AUTHORIZATION_MISSING']);
  }
  gate('IMPLEMENTATION','IMPLEMENTATION',candidate?String(candidate.id):null,candidate??null,candidateCurrent,
    candidateCurrent?[]:[!candidate?(w.current_implementation_evidence_id===null?'MISSING_CURRENT_CANDIDATE':'CURRENT_CANDIDATE_INVALID'):'SPEC_CANDIDATE_MISMATCH']);
  const currentCi=cis.filter(c=>c.implementation_sha===F);
  if (!currentCi.length) gate('CI','CI',null,null,false,[cis.length?'CI_SHA_MISMATCH':'MISSING_CI']);
  for (const ci of currentCi) {
    const complete=nonempty(ci.reference) && nonempty(ci.source) && nonempty(ci.recorded_by);
    gate('CI:'+ci.id,'CI',String(ci.id),ci,candidateCurrent && ci.status==='SUCCESS' && complete,
      [...(ci.status==='SUCCESS'?[]:['CI_NOT_SUCCESS']),...(complete?[]:['CI_PROVENANCE_MISSING'])]);
  }
  const risk=String(w.risk_class), higher=['R3','R4'].includes(risk);
  const securityRequired=higher || policy?.security_required===true;
  const securityUnresolved=!higher && policy?.security_required===undefined;
  const reviewSelections:Row[]=[];
  let unresolvedOptionalReview=false;
  for (const type of ['SECURITY','QUALITY'] as const) {
    const required=type==='QUALITY' || securityRequired || securityUnresolved;
    const candidates=reviews.filter(r=>r.review_type===type && r.implementation_sha===F);
    const pending=attempts.filter(a=>a.review_type===type && a.implementation_sha===F && a.submitted_review_id===null);
    const ordered=[...candidates,...pending].sort((a,b)=>Number(a.attempt)-Number(b.attempt));
    const selected=ordered.at(-1);
    const duplicate=new Set(ordered.map(r=>r.attempt)).size!==ordered.length;
    const submitted=!!selected && selected.review_id!==undefined;
    if (!required && !submitted) {
      const previous=candidates.sort((a,b)=>Number(a.attempt)-Number(b.attempt)).at(-1);
      unresolvedOptionalReview=!!previous && reviewApplicable(previous) && (previous.blocking_findings!==0 || previous.verdict!=='PASS');
    }
    const reasons:string[]=[];
    if (type==='SECURITY' && securityUnresolved) reasons.push('SECURITY_REQUIREMENT_UNRESOLVED');
    if (!selected) reasons.push(reviews.some(r=>r.review_type===type)?'STALE_REVIEW':`MISSING_${type}_REVIEW`);
    else if (!submitted) reasons.push('REVIEW_IN_PROGRESS');
    else {
      reviewSelections.push(selected);
      if (!reviewApplicable(selected)) reasons.push('STALE_REVIEW');
      if (selected.verdict!=='PASS') reasons.push(`${type}_REVIEW_NOT_PASS`);
      if (selected.blocking_findings!==0) reasons.push('BLOCKING_FINDINGS');
      if (selected.tracked_files_modified!==0) reasons.push('REVIEW_NOT_READ_ONLY');
      if (!nonempty(selected.findings_ref) || !nonempty(selected.evidence_ref) || !nonempty(selected.artifact_path)) reasons.push('REVIEW_ARTIFACT_MISSING');
    }
    if (duplicate) reasons.push('REVIEW_ATTEMPT_AMBIGUOUS');
    const g=gate(type+'_REVIEW',type+'_REVIEW' as Subject,submitted?String(selected!.review_id):null,submitted?selected!:null,
      submitted && reasons.length===0,reasons,required,true,type==='SECURITY' && securityUnresolved);
    if (submitted && !reviewApplicable(selected!)) {g.stale=true;g.applicable=false;}
  }
  const independent=reviewSelections.length<2 || reviewSelections[0]!.reviewer!==reviewSelections[1]!.reviewer;
  gate('REVIEW_INDEPENDENCE',null,null,null,independent,independent?[]:['REVIEW_STREAM_SUBSTITUTION']);
  const optionalBlocking=reviewSelections.some(r=>reviewApplicable(r) && (r.blocking_findings!==0 || r.verdict!=='PASS'));
  const stop=!!task.blockers || ['PLANNED','BLOCKED','REVIEW_CHANGES_REQUIRED'].includes(String(task.status)) ||
    (policy?.stop_conditions.length??0)>0 || optionalBlocking || unresolvedOptionalReview ||
    (Number(task.frozen_until)>Date.now()) || !!one("SELECT d.task_id FROM dependencies d JOIN tasks t ON t.id=d.requires_id WHERE d.task_id=? AND t.status!='COMPLETED'",taskId);
  gate('STOP_CONDITIONS',null,null,task,!stop,stop?['STOP_CONDITION_PRESENT']:[]);
  gate('SCOPE',null,null,null,!!policy && !policy.scope_violation,policy?.scope_violation?['SCOPE_VIOLATION']:policy?[]:['SCOPE_STATUS_UNRESOLVED']);
  gate('CONFIDENTIALITY',null,null,null,!!policy && !policy.secret_or_confidential_exposure,
    policy?.secret_or_confidential_exposure?['SECRET_OR_CONFIDENTIAL_EXPOSURE']:policy?[]:['CONFIDENTIALITY_STATUS_UNRESOLVED']);
  if (!['R0','R1','R2','R3','R4'].includes(risk)) gate('RISK_POLICY',null,null,w,false,['RISK_POLICY_UNRESOLVED']);
  for (const ref of policy?.required_human_exception_refs??[]) {
    const e=find('HUMAN_AUTHORIZATION',ref);
    gate('HUMAN_EXCEPTION:'+ref,'HUMAN_AUTHORIZATION',ref,e?.provenance??null,!!e,e?[]:['HUMAN_EXCEPTION_MISSING']);
  }
  const pr=find('PR_BRANCH_STATE',prKey);
  gate('PR_BRANCH_STATE','PR_BRANCH_STATE',prKey,pr?.provenance??null,!!pr,
    prKey?pr?[]:['PR_HEAD_NOT_VERIFIED']:['PR_CONTEXT_MISSING'],true,false);
  const malformed=Array.from(effective.values()).some(e=>!e.chain_valid);
  if (malformed) gate('VERIFICATION_INTEGRITY',null,null,null,false,['VERIFICATION_CHAIN_INVALID']);
  const provisionalBlockers=[...new Set(gates.filter(g=>g.provisional_required && !g.recorded_satisfied).flatMap(g=>g.blockers))];
  const authoritativeBlockers=[...new Set([...provisionalBlockers,...gates.filter(g=>g.required).flatMap(g=>[...g.blockers,...g.authoritative_blockers])])];
  return {task_id:taskId,workflow_version:2,risk_class:risk,workflow_v2_governance:'NOT ACTIVATED',
    frozen_spec:spec??null,current_implementation_evidence_id:w.current_implementation_evidence_id,
    implementation_sha:F,current_implementation:candidate??null,provisional_ready:gates.every(g=>!g.provisional_required || g.recorded_satisfied),
    authoritative_merge_eligible:false,required_gates:gates.filter(g=>g.required).map(g=>g.gate),observed_gates:gates,
    effective_verifications:Array.from(effective.values()),provisional_blockers:provisionalBlockers,
    authoritative_blockers:authoritativeBlockers,blockers:authoritativeBlockers,
    missing_evidence:gates.filter(g=>g.required && !g.evidence_present && g.subject_type).map(g=>g.gate),
    sha_mismatches:{ci:cis.filter(c=>c.implementation_sha!==F),reviews:reviews.filter(r=>r.implementation_sha!==F || r.spec_sha!==spec?.spec_sha || r.base_sha!==candidate?.base_sha)},
    fresh_check_requirements:[{subject_type:'PR_BRANCH_STATE',expected_subject_key:prKey,available:false}],
    human_gates:gates.filter(g=>g.subject_type==='HUMAN_AUTHORIZATION'),
    authoritative_source_policy:sourcePolicy,recorded_policy:policy??null,
    trust_limitations:['RECORDED != VERIFIED','Persisted VERIFIED fields are untrusted claims without an accepted source adapter',
      'No authoritative verifier or fresh pre-merge adapter is available','This computation never performs or authorizes a Git merge']};
}
