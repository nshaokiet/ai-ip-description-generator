import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { spawn } from 'node:child_process';
import { dirname,join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { A,B,C,D,governance,fixture,assign,frozen,started,implementation,verification,reviewStart,checkpoint } from './v2-fixture.js';
import type { ReviewSubmitInput } from '../src/v2-contracts.js';
import { Store } from '../src/store.js';

type ReviewView={security:{status:string;stale?:boolean;attempt?:number};quality:{status:string};history:Array<{stale:boolean;verdict:string;review_id:number}>;in_progress:Array<{current:boolean}>};
function reviews(f:ReturnType<typeof fixture>):ReviewView { return f.store.v2.reviewStatus('B2-T') as ReviewView; }
function submit(reviewId:number,assignment:number,reviewer:string,extra:Partial<ReviewSubmitInput>={}):ReviewSubmitInput {
  return {review_id:reviewId,assignment_id:assignment,verdict:'PASS',findings_ref:'synthetic:NONE',blocking_findings:0,evidence_ref:'synthetic:report',artifact_path:'synthetic/review.md',reviewer,model_profile:'synthetic-test-profile',tracked_files_modified:false,...extra};
}
function query(f:ReturnType<typeof fixture>,sql:string) { const db=new DatabaseSync(f.file); try{return db.prepare(sql).all();}finally{db.close();} }
function exec(f:ReturnType<typeof fixture>,sql:string) { const db=new DatabaseSync(f.file);try{db.exec(sql);}finally{db.close();} }
async function race(f:ReturnType<typeof fixture>,operation:string,payloads:unknown[]) {
  const worker=join(dirname(fileURLToPath(import.meta.url)),'v2-worker.js');
  return Promise.all(payloads.map(p=>new Promise<{ok:boolean;error?:string;result?:{id:number}}>((resolve,reject)=>{
    const child=spawn(process.execPath,[worker,f.file,operation,JSON.stringify(p)],{stdio:['ignore','pipe','pipe']});
    let output='',error=''; child.stdout.on('data',c=>output+=String(c));child.stderr.on('data',c=>error+=String(c));
    child.on('error',reject);child.on('close',code=>{if(code!==0)reject(new Error(error));else try{resolve(JSON.parse(output));}catch(e){reject(e);}});
  })));
}

test('explicit prospective enrollment is idempotent; conflicting enrollment and historical V1 backfill are rejected',()=>{
  const f=fixture(false);try{
    const p={task_id:'B2-T',risk_class:'R3' as const,authorization_ref:'AUTH-T',activation_commit:A};
    assert.deepEqual(f.store.v2.enroll(p),f.store.v2.enroll(p));
    assert.throws(()=>f.store.v2.enroll({...p,activation_commit:B}),/Conflicting enrollment/);
    f.store.addTask('OLD-T','old',2);f.store.approveTask('OLD-T','old');f.store.claim('OLD-T','old','feat/old','/old');
    assert.throws(()=>f.store.v2.enroll({...p,task_id:'OLD-T'}),/prospective/);
    f.store.checkpoint('OLD-T','old',checkpoint);f.store.release('OLD-T','old');
    assert.throws(()=>f.store.v2.enroll({...p,task_id:'OLD-T'}),/Historical/);
  }finally{f.cleanup();}
});
test('non-enrolled V1 tasks keep legacy operations, owner and state shape with additive version marker',()=>{
  const f=fixture(false);try{
    assert.throws(()=>assign(f.store,'PLANNER'),/enrollment/);
    f.store.claim('B2-T','v1','feat/v1','/v1');f.store.checkpoint('B2-T','v1',checkpoint);
    const state=f.store.getState('B2-T') as {tasks:Array<Record<string,unknown>>};
    assert.equal(state.tasks[0]!.workflow_version,1);assert.equal(state.tasks[0]!.owner,'v1');
    assert.equal('assignments' in state.tasks[0]!,false);assert.equal('role' in f.store.latestCheckpoint('B2-T')!,false);
    f.store.finish('B2-T','v1',['PASS'],B);assert.equal(query(f,'SELECT COUNT(*) AS n FROM task_workflow')[0]!.n,0);
  }finally{f.cleanup();}
});
test('all four role identities and deterministic assignment history survive restart',()=>{
  const f=fixture();try{
    for(const role of ['PLANNER','IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER'] as const) assign(f.store,role);
    const old=f.store.v2.getAssignments('B2-T').find(r=>r.role==='PLANNER')!;
    assert.throws(()=>assign(f.store,'PLANNER','replacement'),/conflict/);
    const next=f.store.v2.assignRole({task_id:'B2-T',...governance,role:'PLANNER',agent_id:'replacement',authorization_ref:'ASSIGN-T',expected_assignment_id:Number(old.id)});
    assert.equal(next.assignment_version,2);f.restart();
    assert.equal(f.store.v2.getAssignments('B2-T').length,5);assert.equal(f.store.v2.getAssignments('B2-T').find(r=>r.id===old.id)!.status,'SUPERSEDED');
  }finally{f.cleanup();}
});
test('assignment retry is idempotent and conflicting authority reference is rejected',()=>{
  const f=fixture();try{
    const a=assign(f.store,'PLANNER');assert.equal(assign(f.store,'PLANNER').id,a.id);
    assert.throws(()=>f.store.v2.assignRole({task_id:'B2-T',...governance,role:'PLANNER',agent_id:'planner',authorization_ref:'different'}),/authorization conflict/);
  }finally{f.cleanup();}
});
test('concurrent incompatible role assignment produces precisely one winner',async()=>{
  const f=fixture();try{
    const p={task_id:'B2-T',...governance,role:'PLANNER',authorization_ref:'ASSIGN-T'};
    const results=await race(f,'assignment',[{...p,agent_id:'p1'},{...p,agent_id:'p2'}]);
    assert.equal(results.filter(r=>r.ok).length,1);assert.match(results.find(r=>!r.ok)!.error!,/conflict/);
    assert.equal(f.store.v2.getAssignments('B2-T').length,1);
  }finally{f.cleanup();}
});
test('spec DRAFT to READY is Planner-scoped, collision-safe and durable',()=>{
  const f=fixture();try{
    const planner=assign(f.store,'PLANNER'),reviewer=assign(f.store,'SECURITY_REVIEWER');
    const p={task_id:'B2-T',assignment_id:Number(planner.id),spec_version:'1',spec_sha:A,artifact_path:'spec.md',authorization_ref:'s'};
    const draft=f.store.v2.submitSpec({...p,status:'DRAFT'});assert.equal(draft.status,'DRAFT');
    assert.equal(f.store.v2.submitSpec({...p,status:'READY'}).id,draft.id);
    assert.throws(()=>f.store.v2.submitSpec({...p,spec_sha:B}),/collision/);
    assert.throws(()=>f.store.v2.submitSpec({...p,assignment_id:Number(reviewer.id)}),/role assignment/);
    f.restart();assert.equal(f.store.v2.getSpec('B2-T','1')[0]!.status,'READY');
  }finally{f.cleanup();}
});
test('Human freeze requires exact artifact/version/SHA evidence and rejects Planner self-authorization',()=>{
  const f=fixture();try{
    const planner=assign(f.store,'PLANNER');
    f.store.v2.submitSpec({task_id:'B2-T',assignment_id:Number(planner.id),spec_version:'1',spec_sha:A,artifact_path:'spec.md',authorization_ref:'AUTH-T'});
    const approval=f.store.v2.recordVerification(verification());
    const p={task_id:'B2-T',...governance,spec_version:'1',spec_sha:A,approval_ref:'AUTH-T',approval_verification_id:Number(approval.id),expected_frozen_spec_id:null};
    assert.throws(()=>f.store.v2.freezeSpec({...p,actor_id:'planner'}),/self-authorize/);
    assert.throws(()=>f.store.v2.freezeSpec(p),/exact committed/);
    const valid=f.store.v2.recordVerification(verification({expected_effective_verification_id:Number(approval.id),metadata_json:JSON.stringify({human_authorized:true,committed_artifact_exists:true,spec_sha:A,spec_version:'1',artifact_path:'spec.md'})}));
    assert.throws(()=>f.store.v2.freezeSpec(p),/authorization provenance/);
    assert.equal(f.store.v2.freezeSpec({...p,approval_verification_id:Number(valid.id)}).status,'FROZEN');
    assert.equal(f.store.v2.freezeSpec({...p,approval_verification_id:Number(valid.id)}).status,'FROZEN');
  }finally{f.cleanup();}
});
test('freeze/supersession is atomic; old candidate/history cannot silently retarget the new spec',()=>{
  const f=fixture();try{
    const implementer=started(f.store), old=f.store.v2.getSpec('B2-T')[0]!;
    const candidate=f.store.v2.recordImplementation(implementation(implementer));
    assert.throws(()=>frozen(f.store,'2.0.0',C,999),/Frozen spec conflict/);
    assert.equal(f.store.v2.getSpec('B2-T','1.0.0')[0]!.status,'FROZEN');
    const specs=f.store.v2.getSpec('B2-T','2.0.0');assert.equal(specs[0]!.status,'READY');
    const approvals=query(f,"SELECT id FROM evidence_verifications WHERE subject_key='AUTH-2.0.0'");
    f.store.v2.freezeSpec({task_id:'B2-T',...governance,spec_version:'2.0.0',spec_sha:C,approval_ref:'AUTH-2.0.0',approval_verification_id:Number(approvals[0]!.id),expected_frozen_spec_id:Number(old.id)});
    assert.equal(f.store.v2.getSpec('B2-T','1.0.0')[0]!.status,'SUPERSEDED');
    assert.equal(f.store.v2.candidate('B2-T')!.id,candidate.id);
    assert.throws(()=>f.store.v2.recordImplementation(implementation(implementer,D,Number(candidate.id))),/FROZEN spec/);
    assert.throws(()=>f.store.v2.recordImplementation(implementation(implementer,D,Number(candidate.id),C)),/lease/);
    f.restart();assert.equal(f.store.v2.getSpec('B2-T').filter(r=>r.status==='FROZEN').length,1);
  }finally{f.cleanup();}
});
test('implementation start rejects missing frozen spec and reviewers, protects collisions and main, retries idempotently',()=>{
  const f=fixture();try{
    const implementer=assign(f.store,'IMPLEMENTER'),security=assign(f.store,'SECURITY_REVIEWER');
    const p={task_id:'B2-T',implementer_assignment_id:Number(implementer.id),spec_sha:A,branch:'feat/b2',worktree:'/b2'};
    assert.throws(()=>f.store.v2.startImplementation(p),/FROZEN/);frozen(f.store);
    assert.throws(()=>f.store.v2.startImplementation({...p,implementer_assignment_id:Number(security.id)}),/role assignment/);
    assert.throws(()=>f.store.v2.startImplementation({...p,branch:'main'}),/main/);
    f.store.addTask('OTHER-T','other',2);f.store.approveTask('OTHER-T','auth');f.store.claim('OTHER-T','other','feat/collision','/collision');
    assert.throws(()=>f.store.v2.startImplementation({...p,branch:'feat/collision'}),/leased/);
    assert.throws(()=>f.store.claim('B2-T','implementer','feat/b2','/b2'),/start_implementation/);
    assert.deepEqual(f.store.v2.startImplementation(p),f.store.v2.startImplementation(p));f.restart();
    assert.equal((f.store.getState('B2-T') as {tasks:Array<{owner:string}>}).tasks[0]!.owner,'implementer');
  }finally{f.cleanup();}
});
test('V2 legacy renew/report/release/expiry paths preserve atomic assignment mirror and frozen-spec start requirements',()=>{
  const f=fixture();try{
    const assignment=started(f.store);
    f.store.renew('B2-T','implementer',5);
    f.store.report('B2-T','implementer',{milestone:'progress',tests:[],files_changed:[],commit_sha:null,remaining_work:'continue',blockers:[]});
    assert.equal(query(f,'SELECT lease_expiry FROM tasks WHERE id=\'B2-T\'')[0]!.lease_expiry,f.store.v2.getAssignments('B2-T').find(a=>a.id===assignment)!.lease_expiry);
    f.store.release('B2-T','implementer');assert.equal(f.store.v2.getAssignments('B2-T').find(a=>a.id===assignment)!.lease_expiry,null);
    f.store.v2.startImplementation({task_id:'B2-T',implementer_assignment_id:assignment,spec_sha:A,branch:'feat/restart',worktree:'/restart'});
    exec(f,"UPDATE tasks SET lease_expiry=1 WHERE id='B2-T'; UPDATE task_assignments SET lease_expiry=1 WHERE id="+assignment);
    f.store.nextTask();assert.equal(f.store.v2.getAssignments('B2-T').find(a=>a.id===assignment)!.status,'BLOCKED');
  }finally{f.cleanup();}
});
test('F-07 first candidate and A to B CAS retry remain immutable and restart-safe',()=>{
  const f=fixture();try{
    const a=started(f.store), first=f.store.v2.recordImplementation(implementation(a));
    const next=f.store.v2.recordImplementation(implementation(a,C,Number(first.id)));
    assert.equal(f.store.v2.recordImplementation(implementation(a,C,Number(first.id))).id,next.id);
    assert.throws(()=>f.store.v2.recordImplementation({...implementation(a,C,Number(first.id)),evidence_ref:'conflict'}),/immutable/);
    assert.equal(query(f,'SELECT COUNT(*) AS n FROM implementation_evidence')[0]!.n,2);
    f.restart();assert.equal(f.store.v2.candidate('B2-T')!.id,next.id);
    f.store.finish('B2-T','implementer',['PASS'],C);assert.equal(f.store.v2.recordImplementation(implementation(a,C,Number(first.id))).id,next.id);
  }finally{f.cleanup();}
});
test('F-07 stale non-current transition rolls back inserted loser and leaves winning pointer intact',()=>{
  const f=fixture();try{
    const a=started(f.store), first=f.store.v2.recordImplementation(implementation(a));
    assert.throws(()=>f.store.v2.recordImplementation(implementation(a,C,null)),/stale expected/);
    assert.equal(query(f,'SELECT COUNT(*) AS n FROM implementation_evidence')[0]!.n,1);
    assert.equal(f.store.v2.candidate('B2-T')!.id,first.id);
    assert.throws(()=>f.store.v2.recordImplementation({...implementation(a,D,Number(first.id)),spec_sha:C}),/FROZEN/);
    assert.equal(f.store.v2.candidate('B2-T')!.id,first.id);
  }finally{f.cleanup();}
});
test('F-07 concurrent A to B and A to C admits exactly one durable winner',async()=>{
  const f=fixture();try{
    const a=started(f.store), first=f.store.v2.recordImplementation(implementation(a));
    const results=await race(f,'candidate',[implementation(a,C,Number(first.id)),implementation(a,D,Number(first.id))]);
    assert.equal(results.filter(r=>r.ok).length,1);assert.match(results.find(r=>!r.ok)!.error!,/Candidate conflict/);
    assert.equal(query(f,'SELECT COUNT(*) AS n FROM implementation_evidence')[0]!.n,2);
    f.restart();assert.equal(f.store.v2.candidate('B2-T')!.id,results.find(r=>r.ok)!.result!.id);
  }finally{f.cleanup();}
});
test('F-07 state resolves solely from pointer even when a higher ID/timestamp exists',()=>{
  const f=fixture();try{
    const a=started(f.store), first=f.store.v2.recordImplementation(implementation(a));
    exec(f,`INSERT INTO implementation_evidence(task_id,spec_sha,base_sha,implementation_sha,evidence_ref,created_at) VALUES ('B2-T','${A}','${A}','${D}','unselected',9999999999999)`);
    f.restart();assert.equal(f.store.v2.candidate('B2-T')!.id,first.id);
    assert.equal((f.store.getState('B2-T') as {tasks:Array<{current_implementation:{id:number}}>}).tasks[0]!.current_implementation.id,first.id);
  }finally{f.cleanup();}
});
test('CI references retry idempotently, reject conflicting payload, and retain stale SHA history',()=>{
  const f=fixture();try{
    const a=started(f.store), first=f.store.v2.recordImplementation(implementation(a));
    const p={task_id:'B2-T',implementation_sha:B,status:'SUCCESS' as const,reference:'run:1',source:'synthetic-ci',recorded_by:'automation'};
    const ci=f.store.v2.recordCi(p);assert.equal(f.store.v2.recordCi(p).id,ci.id);
    assert.throws(()=>f.store.v2.recordCi({...p,status:'FAILURE'}),/Conflicting/);
    assert.throws(()=>f.store.v2.recordCi({...p,created_at:0}),/timestamp/);
    assert.throws(()=>f.store.v2.recordCi({...p,implementation_sha:D,reference:'run:unknown'}),/Unknown/);
    f.store.v2.recordImplementation(implementation(a,C,Number(first.id)));
    f.store.v2.recordCi({...p,reference:'run:late-old'});
    const state=f.store.getState('B2-T') as {tasks:Array<{ci_evidence:Array<{stale:boolean}>}>};
    assert.equal(state.tasks[0]!.ci_evidence.length,2);assert.ok(state.tasks[0]!.ci_evidence.every(r=>r.stale));
    assert.equal(query(f,"SELECT COUNT(*) AS n FROM evidence_verifications WHERE subject_type='CI'")[0]!.n,0);
  }finally{f.cleanup();}
});
test('Security/Quality start are independent, type-safe and idempotent with durable pending state',()=>{
  const f=fixture();try{
    const a=started(f.store);f.store.v2.recordImplementation(implementation(a));
    const s=Number(assign(f.store,'SECURITY_REVIEWER').id), q=Number(assign(f.store,'QUALITY_REVIEWER').id);
    const start=f.store.v2.startReview(reviewStart(s,'SECURITY'));
    assert.equal(f.store.v2.startReview(reviewStart(s,'SECURITY')).id,start.id);
    f.store.v2.startReview(reviewStart(q,'QUALITY'));assert.equal(reviews(f).security.status,'IN_PROGRESS');
    assert.throws(()=>f.store.v2.startReview(reviewStart(s,'QUALITY')),/role assignment/);
    assert.throws(()=>f.store.v2.startReview(reviewStart(q,'QUALITY',C)),/exact current/);
    f.restart();assert.equal(reviews(f).quality.status,'IN_PROGRESS');
  }finally{f.cleanup();}
});
test('Implementer cannot review own candidate under a different reviewer role, even after lease release',()=>{
  const f=fixture();try{
    const a=started(f.store);f.store.v2.recordImplementation(implementation(a));
    const s=Number(assign(f.store,'SECURITY_REVIEWER','implementer').id);
    assert.throws(()=>f.store.v2.startReview(reviewStart(s,'SECURITY')),/independent/);
    f.store.release('B2-T','implementer');assert.throws(()=>f.store.v2.startReview(reviewStart(s,'SECURITY')),/independent/);
  }finally{f.cleanup();}
});
test('review submission validates attribution, blocked findings and tracked modifications; PASS is immutable',()=>{
  const f=fixture();try{
    const a=started(f.store);f.store.v2.recordImplementation(implementation(a));
    const s=Number(assign(f.store,'SECURITY_REVIEWER').id), attempt=Number(f.store.v2.startReview(reviewStart(s,'SECURITY')).id);
    assert.throws(()=>f.store.v2.submitReview(submit(attempt,s,'security_reviewer',{tracked_files_modified:true})),/Clean independent/);
    assert.throws(()=>f.store.v2.submitReview(submit(attempt,s,'security_reviewer',{blocking_findings:1})),/Clean independent/);
    assert.throws(()=>f.store.v2.submitReview(submit(attempt,s,'impostor')),/attribution/);
    const p=submit(attempt,s,'security_reviewer'), result=f.store.v2.submitReview(p);
    assert.equal(f.store.v2.submitReview(p).review_id,result.review_id);
    assert.throws(()=>f.store.v2.submitReview({...p,verdict:'BLOCKED'}),/immutable/);
    const second=f.store.v2.startReview(reviewStart(s,'SECURITY'));assert.equal(second.attempt,2);
    assert.equal(reviews(f).security.status,'IN_PROGRESS');
    f.store.v2.submitReview(submit(Number(second.id),s,'security_reviewer',{verdict:'REQUEST_CHANGES',blocking_findings:1}));
    assert.equal(reviews(f).history.length,2);assert.equal(reviews(f).security.status,'REQUEST_CHANGES');
  }finally{f.cleanup();}
});
test('candidate change stales old PASS/CI, prevents stale in-flight submit, preserves history after restart',()=>{
  const f=fixture();try{
    const a=started(f.store),first=f.store.v2.recordImplementation(implementation(a));
    const s=Number(assign(f.store,'SECURITY_REVIEWER').id),q=Number(assign(f.store,'QUALITY_REVIEWER').id);
    const security=f.store.v2.startReview(reviewStart(s,'SECURITY'));f.store.v2.submitReview(submit(Number(security.id),s,'security_reviewer'));
    const quality=f.store.v2.startReview(reviewStart(q,'QUALITY'));f.store.v2.submitReview(submit(Number(quality.id),q,'quality_reviewer'));
    const pending=f.store.v2.startReview(reviewStart(s,'SECURITY'));
    f.store.v2.recordImplementation(implementation(a,C,Number(first.id)));
    assert.throws(()=>f.store.v2.submitReview(submit(Number(pending.id),s,'security_reviewer')),/exact current/);
    f.restart();assert.ok(reviews(f).history.every(r=>r.stale));assert.equal(reviews(f).security.status,'NOT_STARTED');
    const old=f.store.v2.reviewStatus('B2-T',B) as ReviewView;assert.equal(old.security.status,'PASS');assert.equal(old.security.stale,true);
  }finally{f.cleanup();}
});
test('review BLOCKED and REQUEST_CHANGES are stored separately and cannot authorize merge lifecycle',()=>{
  const f=fixture();try{
    const a=started(f.store);f.store.v2.recordImplementation(implementation(a));f.store.finish('B2-T','implementer',['PASS'],B);
    const s=Number(assign(f.store,'SECURITY_REVIEWER').id),q=Number(assign(f.store,'QUALITY_REVIEWER').id);
    const sr=f.store.v2.startReview(reviewStart(s,'SECURITY')),qr=f.store.v2.startReview(reviewStart(q,'QUALITY'));
    f.store.v2.submitReview(submit(Number(sr.id),s,'security_reviewer',{verdict:'BLOCKED',blocking_findings:1}));
    f.store.v2.submitReview(submit(Number(qr.id),q,'quality_reviewer',{verdict:'REQUEST_CHANGES',blocking_findings:2}));
    assert.equal(reviews(f).security.status,'BLOCKED');assert.equal(reviews(f).quality.status,'REQUEST_CHANGES');
    assert.throws(()=>f.store.transition('B2-T','REVIEW_PASS','claim'),/B3/);
    assert.equal((f.store.getState('B2-T') as {tasks:Array<{status:string}>}).tasks[0]!.status,'REVIEW_CHANGES_REQUIRED');
  }finally{f.cleanup();}
});
test('superseding reviewer assignment invalidates in-flight submission and historical PASS applicability',()=>{
  const f=fixture();try{
    const a=started(f.store);f.store.v2.recordImplementation(implementation(a));
    const s=Number(assign(f.store,'SECURITY_REVIEWER').id),r=f.store.v2.startReview(reviewStart(s,'SECURITY'));
    f.store.v2.submitReview(submit(Number(r.id),s,'security_reviewer'));
    const pending=f.store.v2.startReview(reviewStart(s,'SECURITY'));
    f.store.v2.assignRole({task_id:'B2-T',...governance,role:'SECURITY_REVIEWER',agent_id:'new-security',authorization_ref:'replace',expected_assignment_id:s});
    assert.throws(()=>f.store.v2.submitReview(submit(Number(pending.id),s,'security_reviewer')),/role assignment/);
    assert.equal(reviews(f).history[0]!.stale,true);
  }finally{f.cleanup();}
});
test('verification append/revoke/re-attest is sequential, exact-current and restart-safe',()=>{
  const f=fixture();try{
    const first=f.store.v2.recordVerification(verification());
    const revoked=f.store.v2.recordVerification(verification({decision:'REVOKE',verification_level:'UNVERIFIED',expected_effective_verification_id:Number(first.id)}));
    const last=f.store.v2.recordVerification(verification({expected_effective_verification_id:Number(revoked.id)}));
    assert.equal(last.verification_version,3);assert.equal(last.supersedes_verification_id,revoked.id);
    assert.throws(()=>f.store.v2.recordVerification(verification({expected_effective_verification_id:Number(first.id)})),/conflict/);
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_key:'OTHER',expected_effective_verification_id:Number(last.id)})),/conflict/);
    assert.throws(()=>f.store.v2.recordVerification(verification({decision:'REVOKE'})),/UNVERIFIED/);
    f.restart();assert.equal(query(f,"SELECT COUNT(*) AS n FROM evidence_verifications WHERE subject_key='AUTH-T'")[0]!.n,3);
  }finally{f.cleanup();}
});
test('concurrent verification writers cannot fork or skip a version',async()=>{
  const f=fixture();try{
    const first=f.store.v2.recordVerification(verification());
    const p=verification({expected_effective_verification_id:Number(first.id)});
    const results=await race(f,'verification',[{...p,verification_reference:'a'},{...p,verification_reference:'b'}]);
    assert.equal(results.filter(r=>r.ok).length,1);assert.match(results.find(r=>!r.ok)!.error!,/Verification conflict/);
    assert.equal(query(f,"SELECT COUNT(*) AS n FROM evidence_verifications WHERE subject_key='AUTH-T'")[0]!.n,2);
  }finally{f.cleanup();}
});
test('VERIFIED is provenance-validated only; no caller-requested implicit promotion or authority claim',()=>{
  const f=fixture();try{
    assert.throws(()=>f.store.v2.recordVerification(verification({verification_level:'VERIFIED'})),/provenance/);
    const row=f.store.v2.recordVerification(verification({verification_level:'VERIFIED',verifier_type:'synthetic',verifier_id:'test',verified_at:123}));
    assert.equal(row.verification_level,'VERIFIED');
    const state=JSON.stringify(f.store.getState('B2-T'));
    assert.match(state,/"authority_validated":false/);
    // B3 adds computed fields, but a provenance-only row still grants no authority.
    const gate=f.store.v2.getMergeGate('B2-T');
    assert.equal(gate.provisional_ready,false);
    assert.equal(gate.authoritative_merge_eligible,false);
    assert.ok(gate.blockers.includes('AUTHORITATIVE_VERIFIER_UNAVAILABLE'));
  }finally{f.cleanup();}
});
test('typed verification subjects validate same-task IDs, review type and canonical external keys',()=>{
  const f=fixture();try{
    const a=started(f.store),e=f.store.v2.recordImplementation(implementation(a));
    const ci=f.store.v2.recordCi({task_id:'B2-T',implementation_sha:B,status:'SUCCESS',reference:'run',source:'synthetic',recorded_by:'test'});
    const s=Number(assign(f.store,'SECURITY_REVIEWER').id),r=f.store.v2.startReview(reviewStart(s,'SECURITY'));
    const review=f.store.v2.submitReview(submit(Number(r.id),s,'security_reviewer'));
    const spec=f.store.v2.getSpec('B2-T')[0]!;
    for(const [type,rowId] of [['SPECIFICATION',spec.id],['IMPLEMENTATION',e.id],['CI',ci.id],['SECURITY_REVIEW',review.review_id]] as const)
      f.store.v2.recordVerification(verification({subject_type:type,subject_key:String(rowId),applicable_subject_id:Number(rowId)}));
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_type:'QUALITY_REVIEW',subject_key:String(review.review_id),applicable_subject_id:Number(review.review_id)})),/type\/task/);
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_type:'IMPLEMENTATION',subject_key:'wrong',applicable_subject_id:Number(e.id)})),/Canonical/);
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_type:'CI',subject_key:'999',applicable_subject_id:999})),/type\/task/);
    f.store.v2.recordVerification(verification({subject_type:'PR_BRANCH_STATE',subject_key:'synthetic/repo#42@'+B}));
    f.store.v2.recordVerification(verification({subject_type:'MERGE_RESULT',subject_key:'synthetic/repo@'+B}));
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_type:'PR_BRANCH_STATE',subject_key:'repo#42'})),/Canonical/);
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_type:'HUMAN_AUTHORIZATION',applicable_subject_id:1})),/External/);
  }finally{f.cleanup();}
});
test('V2 role checkpoints and Implementer handoff work at quota threshold, with legacy history unchanged',()=>{
  const f=fixture();try{
    const a=started(f.store),planner=f.store.v2.getAssignments('B2-T').find(r=>r.role==='PLANNER')!;
    f.store.setBudget(8);
    assert.throws(()=>f.store.v2.recordImplementation(implementation(a)),/quota/);
    const cp=f.store.checkpoint('B2-T','planner',checkpoint,'PLANNER',Number(planner.id));
    assert.equal(cp.branch,null);assert.equal(f.store.latestCheckpoint('B2-T','PLANNER')!.id,cp.id);
    assert.throws(()=>f.store.checkpoint('B2-T','planner',checkpoint,'IMPLEMENTER',a),/match/);
    const handoff=f.store.stopAndHandoff('B2-T','implementer',checkpoint,'IMPLEMENTER',a);
    assert.equal((handoff as unknown as {role:string}).role,'IMPLEMENTER');f.restart();assert.equal(f.store.latestCheckpoint('B2-T')!.id,handoff.id);
  }finally{f.cleanup();}
});
test('V2 task state exposes precise assignments/spec/candidate/staleness without activating project governance',()=>{
  const f=fixture();try{
    const a=started(f.store),candidate=f.store.v2.recordImplementation(implementation(a));
    const state=f.store.getState('B2-T') as {tasks:Array<{workflow_version:number;workflow_v2_governance:string;current_implementation:{id:number};assignments:unknown[];frozen_spec:{spec_sha:string}}>};
    assert.equal(state.tasks[0]!.workflow_version,2);assert.equal(state.tasks[0]!.workflow_v2_governance,'NOT ACTIVATED');
    assert.equal(state.tasks[0]!.current_implementation.id,candidate.id);assert.equal(state.tasks[0]!.frozen_spec.spec_sha,A);assert.equal(state.tasks[0]!.assignments.length,2);
    assert.equal(query(f,"SELECT COUNT(*) AS n FROM task_workflow WHERE task_id!='B2-T'")[0]!.n,0);
  }finally{f.cleanup();}
});

test('B1 database with persisted spec/candidate/evidence upgrades additively to B2 and remains restart-safe',()=>{
  const f=fixture();try{
    const a=started(f.store),candidate=f.store.v2.recordImplementation(implementation(a));
    const before=query(f,'SELECT * FROM implementation_evidence');
    // Remove only B2 objects from the isolated test fixture to reproduce the exact B1 schema.
    exec(f,'DROP TABLE checkpoint_assignments; DROP TABLE review_attempts; DELETE FROM schema_migrations WHERE version=3');
    f.restart();assert.equal(f.store.v2.candidate('B2-T')!.id,candidate.id);
    assert.deepEqual(query(f,'SELECT * FROM implementation_evidence'),before);
    assert.equal(query(f,'SELECT MAX(version) AS v FROM schema_migrations')[0]!.v,4);
    f.restart();assert.equal(query(f,'SELECT COUNT(*) AS n FROM schema_migrations WHERE version=3')[0]!.n,1);
  }finally{f.cleanup();}
});
test('Security and Quality cannot share role/session identity or consume each other as independent verdict',()=>{
  const f=fixture();try{
    const a=started(f.store);f.store.v2.recordImplementation(implementation(a));
    const s=Number(assign(f.store,'SECURITY_REVIEWER','shared-session').id);
    assign(f.store,'QUALITY_REVIEWER','shared-session');
    assert.throws(()=>f.store.v2.startReview(reviewStart(s,'SECURITY')),/separate role\/session/);
  }finally{f.cleanup();}
});
test('a replaced Planner identity cannot self-authorize a freeze',()=>{
  const f=fixture();try{
    const p=assign(f.store,'PLANNER');frozen(f.store);
    f.store.v2.assignRole({task_id:'B2-T',...governance,role:'PLANNER',agent_id:'new-planner',authorization_ref:'replace',expected_assignment_id:Number(p.id)});
    const approval=query(f,"SELECT id FROM evidence_verifications WHERE subject_key='AUTH-1.0.0'")[0]!;
    assert.throws(()=>f.store.v2.freezeSpec({task_id:'B2-T',actor_type:'ADMIN',actor_id:'planner',spec_version:'1.0.0',spec_sha:A,approval_ref:'AUTH-1.0.0',approval_verification_id:Number(approval.id),expected_frozen_spec_id:null}),/self-authorize/);
  }finally{f.cleanup();}
});
test('verification rejects cross-task subject links and cross-task supersession IDs',()=>{
  const f=fixture();try{
    const a=started(f.store),candidate=f.store.v2.recordImplementation(implementation(a));
    const old=f.store.v2.recordVerification(verification());
    f.store.addTask('B2-OTHER','other synthetic',2);
    f.store.v2.enroll({task_id:'B2-OTHER',risk_class:'R0',authorization_ref:'other',activation_commit:A});
    assert.throws(()=>f.store.v2.recordVerification(verification({task_id:'B2-OTHER',subject_type:'IMPLEMENTATION',subject_key:String(candidate.id),applicable_subject_id:Number(candidate.id)})),/type\/task/);
    assert.throws(()=>f.store.v2.recordVerification(verification({task_id:'B2-OTHER',expected_effective_verification_id:Number(old.id)})),/conflict/);
    assert.equal(query(f,"SELECT COUNT(*) AS n FROM evidence_verifications WHERE task_id='B2-OTHER'")[0]!.n,0);
  }finally{f.cleanup();}
});
test('canonical repository subject keys prevent casing aliases from forking verification identity',()=>{
  const f=fixture();try{
    const v=f.store.v2.recordVerification(verification({subject_type:'PR_BRANCH_STATE',subject_key:'Synthetic/Repo#42@'+B}));
    assert.equal(v.subject_key,'synthetic/repo#42@'+B);
    assert.throws(()=>f.store.v2.recordVerification(verification({subject_type:'PR_BRANCH_STATE',subject_key:'synthetic/repo#42@'+B})),/conflict/);
  }finally{f.cleanup();}
});
test('a new frozen spec makes selected candidate, reviews and verification applicability stale without rewriting rows',()=>{
  const f=fixture();try{
    const a=started(f.store),candidate=f.store.v2.recordImplementation(implementation(a));
    f.store.v2.recordVerification(verification({subject_type:'IMPLEMENTATION',subject_key:String(candidate.id),applicable_subject_id:Number(candidate.id)}));
    const old=f.store.v2.getSpec('B2-T')[0]!;frozen(f.store,'2.0.0',C,Number(old.id));
    const state=f.store.getState('B2-T') as {tasks:Array<{current_implementation:{id:number;stale:boolean};verification_records:Array<{subject_type:string;stale:boolean}>}>};
    assert.equal(state.tasks[0]!.current_implementation.id,candidate.id);assert.equal(state.tasks[0]!.current_implementation.stale,true);
    assert.equal(state.tasks[0]!.verification_records.find(v=>v.subject_type==='IMPLEMENTATION')!.stale,true);
  }finally{f.cleanup();}
});

test('incompatible B2 migration rolls back version bookkeeping and preserves B1 data without reset',()=>{
  const f=fixture();try{
    const a=started(f.store),candidate=f.store.v2.recordImplementation(implementation(a));
    exec(f,'DROP TABLE checkpoint_assignments; DROP TABLE review_attempts; DELETE FROM schema_migrations WHERE version=3; CREATE TABLE review_attempts(id INTEGER PRIMARY KEY)');
    assert.throws(()=>new Store(f.file),/no such column|Schema version 3 is incompatible/);
    assert.equal(query(f,'SELECT COUNT(*) AS n FROM schema_migrations WHERE version=3')[0]!.n,0);
    assert.equal(query(f,"SELECT COUNT(*) AS n FROM sqlite_master WHERE name='checkpoint_assignments'")[0]!.n,0);
    assert.equal(f.store.v2.candidate('B2-T')!.id,candidate.id);
  }finally{f.cleanup();}
});
test('version-3 metadata with incompatible attempt schema fails closed and preserves existing candidate',()=>{
  const f=fixture();try{
    const a=started(f.store),candidate=f.store.v2.recordImplementation(implementation(a));
    exec(f,'DROP TABLE review_attempts; CREATE TABLE review_attempts(id INTEGER PRIMARY KEY)');
    assert.throws(()=>new Store(f.file),/Schema version 3 is incompatible/);
    assert.equal(f.store.v2.candidate('B2-T')!.id,candidate.id);
  }finally{f.cleanup();}
});
test('verification recording detects a tampered/gapped chain and refuses further appends',()=>{
  const f=fixture();try{
    const v=f.store.v2.recordVerification(verification());
    // Corruption is simulated only in an isolated test DB; production triggers reject this write.
    exec(f,`DROP TRIGGER trg_evidence_verifications_chain; INSERT INTO evidence_verifications(task_id,subject_type,subject_key,verification_version,supersedes_verification_id,decision,verification_level,recorded_by,created_at) VALUES ('B2-T','HUMAN_AUTHORIZATION','AUTH-T',3,${v.id},'ATTEST','RECORDED','tampered',1)`);
    assert.throws(()=>f.store.v2.recordVerification(verification({expected_effective_verification_id:Number(v.id)})),/Invalid verification chain/);
    assert.equal(query(f,'SELECT COUNT(*) AS n FROM evidence_verifications')[0]!.n,2);
  }finally{f.cleanup();}
});
