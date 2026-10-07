import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { A,B,C,D,fixture,assign,started,implementation,verification,reviewStart,frozen } from './v2-fixture.js';
import { computeMergeGate, type EffectiveVerification, type Gate } from '../src/v2-merge-gate.js';
import type { MergePolicy, VerificationInput } from '../src/v2-contracts.js';

type Fixture=ReturnType<typeof fixture>;
type Result={provisional_ready:boolean;authoritative_merge_eligible:boolean;implementation_sha:string|null;
  observed_gates:Gate[];blockers:string[];provisional_blockers:string[];effective_verifications:EffectiveVerification[];
  current_implementation_evidence_id:number|null;workflow_v2_governance:string;sha_mismatches:{ci:unknown[];reviews:unknown[]}};
const policy:MergePolicy={security_required:true,required_human_exception_refs:[],stop_conditions:[],
  scope_violation:false,secret_or_confidential_exposure:false,repository:'synthetic/repo',pr_number:42};
function sql(f:Fixture,statement:string) {const db=new DatabaseSync(f.file);try {db.exec('PRAGMA busy_timeout=5000');db.exec(statement);}finally{db.close();}}
function query(f:Fixture,statement:string) {const db=new DatabaseSync(f.file);try {return db.prepare(statement).all() as Record<string,string|number|null>[];}finally{db.close();}}
const result=(f:Fixture)=>f.store.v2.getMergeGate('B2-T') as Result;
const gate=(f:Fixture,name:string)=>result(f).observed_gates.find(g=>g.gate===name)!;
const has=(f:Fixture,code:string)=>assert.ok(result(f).blockers.includes(code),JSON.stringify(result(f).blockers));
function recordedPolicy(f:Fixture,extra:Partial<MergePolicy>={}) {
  const prior=query(f,"SELECT id FROM evidence_verifications WHERE subject_type='HUMAN_AUTHORIZATION' AND subject_key='AUTH-T' ORDER BY verification_version DESC")[0];
  return f.store.v2.recordVerification(verification({expected_effective_verification_id:prior?Number(prior.id):null,
    metadata_json:JSON.stringify({merge_policy:{...policy,...extra}})}));
}
function review(f:Fixture,type:'SECURITY'|'QUALITY',options:{verdict?:'PASS'|'REQUEST_CHANGES'|'BLOCKED';blocking?:number;modified?:boolean}={}) {
  const a=f.store.v2.getAssignments('B2-T').find(a=>a.role===type+'_REVIEWER' && a.status==='ACTIVE')??assign(f.store,type+'_REVIEWER' as 'SECURITY_REVIEWER'|'QUALITY_REVIEWER');
  const start=f.store.v2.startReview(reviewStart(Number(a.id),type));
  return f.store.v2.submitReview({review_id:Number(start.id),assignment_id:Number(a.id),reviewer:String(a.agent_id),
    verdict:options.verdict??'PASS',blocking_findings:options.blocking??0,tracked_files_modified:options.modified??false,
    findings_ref:'synthetic:NONE',artifact_path:'synthetic/'+type+'.md',evidence_ref:'synthetic:review',model_profile:'synthetic-test-only'});
}
function ci(f:Fixture,status:'SUCCESS'|'PENDING'|'FAILURE'|'CANCELLED'|'UNKNOWN'='SUCCESS',impl=B,reference='synthetic:ci') {
  return f.store.v2.recordCi({task_id:'B2-T',implementation_sha:impl,status,reference,source:'synthetic',recorded_by:'automation'});
}
function ready(options:{security?:boolean;quality?:boolean;ci?:boolean;policy?:boolean}={}) {
  const f=fixture();const implementer=started(f.store);
  const candidate=f.store.v2.recordImplementation(implementation(implementer));
  if(options.policy!==false) recordedPolicy(f);
  if(options.ci!==false) ci(f);
  if(options.security!==false) review(f,'SECURITY');
  if(options.quality!==false) review(f,'QUALITY');
  return Object.assign(f,{implementer,candidate});
}
function attest(f:Fixture,type:VerificationInput['subject_type'],key:string,id?:number,extra:Partial<VerificationInput>={}) {
  const prior=query(f,`SELECT id FROM evidence_verifications WHERE subject_type='${type}' AND subject_key='${key}' ORDER BY verification_version DESC`)[0];
  return f.store.v2.recordVerification(verification({subject_type:type,subject_key:key,applicable_subject_id:id,
    expected_effective_verification_id:prior?Number(prior.id):null,verification_level:'VERIFIED',
    verifier_type:'synthetic',verifier_id:'test',verification_source:'synthetic',verification_reference:'synthetic:proof',verified_at:123,...extra}));
}
function dump(f:Fixture) {
  const db=new DatabaseSync(f.file);
  try {const tables=db.prepare("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").all() as {name:string}[];
    return JSON.stringify(tables.map(t=>[t.name,db.prepare('SELECT * FROM "'+t.name+'"').all()]));
  }finally{db.close();}
}

test('complete recorded R3 evidence is provisional only; missing adapters block authority',()=>{
  const f=ready();try {assert.equal(result(f).provisional_ready,true);assert.equal(result(f).authoritative_merge_eligible,false);
    has(f,'AUTHORITATIVE_VERIFIER_UNAVAILABLE');has(f,'FRESH_PREMERGE_CHECK_UNAVAILABLE');
    assert.equal(result(f).workflow_v2_governance,'NOT ACTIVATED');assert.equal(result(f).implementation_sha,B);
  }finally{f.cleanup();}
});
test('larger/newer unselected implementation row never changes persisted F',()=>{
  const f=ready();try {sql(f,`INSERT INTO implementation_evidence(task_id,spec_sha,base_sha,implementation_sha,evidence_ref,recorded_by_assignment_id,created_at) VALUES ('B2-T','${A}','${A}','${C}','synthetic',${f.implementer},9999999999999)`);
    assert.equal(result(f).implementation_sha,B);assert.equal(result(f).current_implementation_evidence_id,f.candidate.id);assert.equal(result(f).provisional_ready,true);
  }finally{f.cleanup();}
});
for(const [name,pointer,code] of [['missing','NULL','MISSING_CURRENT_CANDIDATE'],['broken','99999','CURRENT_CANDIDATE_INVALID']] as const) {
  test(name+' pointer fails closed without history fallback',()=>{const f=ready();try{
    sql(f,"PRAGMA foreign_keys=OFF; UPDATE task_workflow SET current_implementation_evidence_id="+pointer+" WHERE task_id='B2-T'");
    assert.equal(result(f).implementation_sha,null);assert.equal(result(f).provisional_ready,false);has(f,code);
    assert.doesNotThrow(()=>f.store.getState('B2-T'));
  }finally{f.cleanup();}});
}
test('cross-task candidate pointer cannot select another task evidence',()=>{
  const f=ready();try {sql(f,`INSERT INTO tasks(id,title,priority,status) VALUES ('OTHER','synthetic',2,'PLANNED');
    INSERT INTO implementation_evidence(task_id,spec_sha,base_sha,implementation_sha,created_at) VALUES ('OTHER','${A}','${A}','${C}',1);
    PRAGMA foreign_keys=OFF; UPDATE task_workflow SET current_implementation_evidence_id=(SELECT id FROM implementation_evidence WHERE task_id='OTHER') WHERE task_id='B2-T'`);
    has(f,'CURRENT_CANDIDATE_INVALID');assert.equal(result(f).implementation_sha,null);
  }finally{f.cleanup();}
});
test('effective linear chain resolves terminal and derives superseded history',()=>{
  const f=ready();try{const first=attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    const last=attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{verification_level:'RECORDED'});
    const e=result(f).effective_verifications.find(e=>e.subject_type==='IMPLEMENTATION')!;
    assert.equal(e.terminal_id,last.id);assert.deepEqual(e.superseded_ids,[first.id]);assert.equal(e.verification_level,'RECORDED');assert.equal(e.chain_valid,true);
  }finally{f.cleanup();}
});
test('terminal REVOKE invalidates earlier VERIFIED for provisional and authority',()=>{
  const f=ready();try{attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{decision:'REVOKE',verification_level:'UNVERIFIED'});
    const g=gate(f,'IMPLEMENTATION');assert.equal(g.revoked,true);assert.equal(g.verification_level,'UNVERIFIED');
    assert.equal(result(f).provisional_ready,false);has(f,'VERIFICATION_REVOKED');
  }finally{f.cleanup();}
});
test('re-attestation after revocation restores recorded applicability without granting authority',()=>{
  const f=ready();try{attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{decision:'REVOKE',verification_level:'UNVERIFIED'});
    attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{verification_level:'RECORDED'});
    assert.equal(gate(f,'IMPLEMENTATION').revoked,false);assert.equal(result(f).provisional_ready,true);assert.equal(result(f).authoritative_merge_eligible,false);
  }finally{f.cleanup();}
});
for(const name of ['gap','fork'] as const) {
  test('malformed '+name+' verification chain fails closed',()=>{
    const f=ready();try{const first=attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{verification_level:'RECORDED'});
      if(name==='fork') attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{verification_level:'RECORDED'});
      sql(f,'DROP TRIGGER trg_evidence_verifications_chain; DROP INDEX uq_evidence_verifications_supersedes;');
      // After version 2 a second successor of version 1 is a real fork;
      // without version 2 the same insertion represents a version gap.
      const subjectKey=String(f.candidate.id);
      sql(f,`PRAGMA ignore_check_constraints=ON; INSERT INTO evidence_verifications(task_id,subject_type,subject_key,implementation_evidence_id,verification_version,supersedes_verification_id,decision,verification_level,recorded_by,created_at)
        VALUES ('B2-T','IMPLEMENTATION','${subjectKey}',${f.candidate.id},3,${first.id},'ATTEST','RECORDED','tamper',1)`);
      has(f,'VERIFICATION_CHAIN_INVALID');assert.equal(result(f).provisional_ready,false);
    }finally{f.cleanup();}
  });
}
test('cross-type verification FK tampering is invalid despite valid version order',()=>{
  const f=ready();try{attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    sql(f,"DROP TRIGGER trg_evidence_verifications_no_update; PRAGMA ignore_check_constraints=ON; UPDATE evidence_verifications SET task_spec_id=1 WHERE subject_type='IMPLEMENTATION'");
    has(f,'VERIFICATION_CHAIN_INVALID');
  }finally{f.cleanup();}
});
test('cross-task typed subject tampering fails identity validation',()=>{
  const f=ready();try{attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    sql(f,`INSERT INTO tasks(id,title,priority,status) VALUES ('OTHER','synthetic',2,'PLANNED');
      INSERT INTO implementation_evidence(task_id,spec_sha,base_sha,implementation_sha,created_at) VALUES ('OTHER','${A}','${A}','${C}',1);
      PRAGMA foreign_keys=OFF; DROP TRIGGER trg_evidence_verifications_no_update;
      UPDATE evidence_verifications SET implementation_evidence_id=(SELECT id FROM implementation_evidence WHERE task_id='OTHER'),subject_key=CAST((SELECT id FROM implementation_evidence WHERE task_id='OTHER') AS TEXT) WHERE subject_type='IMPLEMENTATION'`);
    has(f,'VERIFICATION_CHAIN_INVALID');
  }finally{f.cleanup();}
});
test('terminal UNVERIFIED cannot satisfy recorded evidence',()=>{
  const f=ready();try{attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{verification_level:'UNVERIFIED'});
    assert.equal(result(f).provisional_ready,false);has(f,'EVIDENCE_UNVERIFIED');
  }finally{f.cleanup();}
});
test('missing task authorization is never inherited from a spec freeze',()=>{
  const f=ready({policy:false});try{has(f,'HUMAN_AUTHORIZATION_MISSING');assert.equal(result(f).provisional_ready,false);}
  finally{f.cleanup();}
});
test('task approval reference mismatch blocks recorded authorization',()=>{
  const f=ready();try{sql(f,"UPDATE tasks SET approval_ref='OTHER' WHERE id='B2-T'");has(f,'HUMAN_AUTHORIZATION_MISSING');}
  finally{f.cleanup();}
});
test('missing frozen spec fails closed',()=>{
  const f=ready();try{sql(f,"UPDATE task_specs SET status='SUPERSEDED' WHERE task_id='B2-T'");has(f,'NO_FROZEN_SPEC');assert.equal(result(f).provisional_ready,false);}
  finally{f.cleanup();}
});
test('spec supersession retains pointer and makes previous verifications stale',()=>{
  const f=ready();try{attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    const current=f.store.v2.getSpec('B2-T').find(s=>s.status==='FROZEN')!;
    attest(f,'SPECIFICATION',String(current.id),Number(current.id));
    frozen(f.store,'2.0.0',D,Number(current.id));
    has(f,'SPEC_CANDIDATE_MISMATCH');assert.equal(result(f).implementation_sha,B);
    assert.ok(result(f).effective_verifications.filter(e=>['IMPLEMENTATION','SPECIFICATION'].includes(e.subject_type)).every(e=>e.stale));
  }finally{f.cleanup();}
});
test('revoked freeze authorization blocks an otherwise frozen spec',()=>{
  const f=ready();try{attest(f,'HUMAN_AUTHORIZATION','AUTH-1.0.0',undefined,{decision:'REVOKE',verification_level:'UNVERIFIED'});
    has(f,'VERIFICATION_REVOKED');assert.equal(gate(f,'FREEZE_AUTHORIZATION').recorded_satisfied,false);
  }finally{f.cleanup();}
});
test('missing current CI blocks readiness',()=>{
  const f=ready({ci:false});try{has(f,'MISSING_CI');assert.equal(result(f).provisional_ready,false);}finally{f.cleanup();}
});
for(const status of ['PENDING','FAILURE','CANCELLED','UNKNOWN'] as const) {
  test('current CI '+status+' cannot satisfy SUCCESS gate',()=>{
    const f=ready({ci:false});try{ci(f,status);has(f,'CI_NOT_SUCCESS');assert.equal(result(f).provisional_ready,false);}finally{f.cleanup();}
  });
}
test('contradictory current CI observations cannot cherry-pick SUCCESS',()=>{
  const f=ready();try{ci(f,'FAILURE',B,'synthetic:other-ci');has(f,'CI_NOT_SUCCESS');assert.equal(result(f).provisional_ready,false);}finally{f.cleanup();}
});
test('candidate change stales all A review/CI/attestations and requires B evidence',()=>{
  const f=ready();try{
    attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id));
    const c=query(f,'SELECT id FROM ci_evidence')[0]!;attest(f,'CI',String(c.id),Number(c.id));
    for(const r of query(f,'SELECT * FROM reviews')) attest(f,(r.review_type+'_REVIEW') as 'SECURITY_REVIEW'|'QUALITY_REVIEW',String(r.review_id),Number(r.review_id));
    f.store.v2.recordImplementation(implementation(f.implementer,C,Number(f.candidate.id)));
    assert.equal(result(f).implementation_sha,C);has(f,'CI_SHA_MISMATCH');has(f,'STALE_REVIEW');
    assert.ok(result(f).effective_verifications.filter(e=>['IMPLEMENTATION','CI','SECURITY_REVIEW','QUALITY_REVIEW'].includes(e.subject_type)).every(e=>e.stale));
    assert.equal(result(f).sha_mismatches.ci.length,1);assert.equal(result(f).sha_mismatches.reviews.length,2);
    f.restart();assert.equal(result(f).implementation_sha,C);assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
for(const type of ['SECURITY','QUALITY'] as const) {
  test('missing '+type+' review cannot be substituted by the other stream',()=>{
    const f=ready(type==='SECURITY'?{security:false}:{quality:false});try{has(f,'MISSING_'+type+'_REVIEW');assert.equal(result(f).provisional_ready,false);}finally{f.cleanup();}
  });
  for(const verdict of ['REQUEST_CHANGES','BLOCKED'] as const) test(type+' '+verdict+' blocks merge evidence',()=>{
    const f=ready(type==='SECURITY'?{security:false}:{quality:false});try{review(f,type,{verdict});has(f,type+'_REVIEW_NOT_PASS');assert.equal(result(f).provisional_ready,false);}finally{f.cleanup();}
  });
  test(type+' mismatched exact implementation SHA fails current gate',()=>{
    const f=ready();try{sql(f,`DROP TRIGGER trg_reviews_no_update; UPDATE reviews SET implementation_sha='${C}' WHERE review_type='${type}'`);
      has(f,'STALE_REVIEW');assert.equal(result(f).provisional_ready,false);
    }finally{f.cleanup();}
  });
}
test('blocking findings in a current review defeat readiness',()=>{
  const f=ready({security:false});try{review(f,'SECURITY',{verdict:'REQUEST_CHANGES',blocking:1});has(f,'BLOCKING_FINDINGS');}finally{f.cleanup();}
});
test('tampered PASS with tracked modifications cannot satisfy independent review',()=>{
  const f=ready();try{sql(f,"DROP TRIGGER trg_reviews_no_update; UPDATE reviews SET tracked_files_modified=1 WHERE review_type='QUALITY'");has(f,'REVIEW_NOT_READ_ONLY');}finally{f.cleanup();}
});
test('new in-progress review attempt prevents reuse of older PASS',()=>{
  const f=ready();try{const s=f.store.v2.getAssignments('B2-T').find(a=>a.role==='SECURITY_REVIEWER')!;
    f.store.v2.startReview(reviewStart(Number(s.id),'SECURITY'));has(f,'REVIEW_IN_PROGRESS');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
test('later immutable review attempt makes earlier same-SHA verification historically stale',()=>{
  const f=ready();try{const old=query(f,"SELECT review_id FROM reviews WHERE review_type='SECURITY'")[0]!;
    attest(f,'SECURITY_REVIEW',String(old.review_id),Number(old.review_id));review(f,'SECURITY');
    const e=result(f).effective_verifications.find(e=>e.subject_type==='SECURITY_REVIEW')!;
    assert.equal(e.stale,true);assert.equal(e.applicable,false);assert.equal(result(f).provisional_ready,true);
    assert.equal(gate(f,'SECURITY_REVIEW').verification_level,'RECORDED');
  }finally{f.cleanup();}
});
test('superseded reviewer assignment stales previous PASS',()=>{
  const f=ready();try{const s=f.store.v2.getAssignments('B2-T').find(a=>a.role==='SECURITY_REVIEWER')!;
    sql(f,'UPDATE task_assignments SET status=\'SUPERSEDED\' WHERE id='+s.id);has(f,'STALE_REVIEW');
  }finally{f.cleanup();}
});
test('recorded Security and Quality cannot share an identity',()=>{
  const f=ready();try{sql(f,"UPDATE task_assignments SET agent_id='quality_reviewer' WHERE role='SECURITY_REVIEWER'; DROP TRIGGER trg_reviews_no_update; UPDATE reviews SET reviewer='quality_reviewer' WHERE review_type='SECURITY'");
    has(f,'REVIEW_STREAM_SUBSTITUTION');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
for(const type of ['HUMAN_AUTHORIZATION','CI','SECURITY_REVIEW','QUALITY_REVIEW'] as const) test('RECORDED '+type+' never implies authoritative verification',()=>{
  const f=ready();try{assert.equal(result(f).provisional_ready,true);has(f,type+'_NOT_VERIFIED');assert.equal(result(f).authoritative_merge_eligible,false);}finally{f.cleanup();}
});
test('all required subjects claiming VERIFIED cannot enable authority without approved adapters',()=>{
  const f=ready();try{
    // Use plausible source labels as well as complete fields; neither is proof.
    for(const ref of ['AUTH-T','AUTH-1.0.0']) {
      const old=query(f,`SELECT * FROM evidence_verifications WHERE subject_key='${ref}' ORDER BY verification_version DESC`)[0]!;
      attest(f,'HUMAN_AUTHORIZATION',ref,undefined,{verifier_type:'HUMAN_AUTHORITY',verification_source:'approved-governance',metadata_json:String(old.metadata_json)});
    }
    const spec=f.store.v2.getSpec('B2-T').find(s=>s.status==='FROZEN')!;
    attest(f,'SPECIFICATION',String(spec.id),Number(spec.id),{verifier_type:'GIT_REPOSITORY',verification_source:'git'});
    attest(f,'IMPLEMENTATION',String(f.candidate.id),Number(f.candidate.id),{verifier_type:'GIT_HOST',verification_source:'github'});
    const c=query(f,'SELECT id FROM ci_evidence')[0]!;attest(f,'CI',String(c.id),Number(c.id),{verifier_type:'CI_PROVIDER',verification_source:'github-actions'});
    for(const r of query(f,'SELECT * FROM reviews')) attest(f,(r.review_type+'_REVIEW') as 'SECURITY_REVIEW'|'QUALITY_REVIEW',String(r.review_id),Number(r.review_id),{verifier_type:'REVIEW_ARTIFACT_VERIFIER',verification_source:'canonical-review'});
    attest(f,'PR_BRANCH_STATE','synthetic/repo#42@'+B,undefined,{verifier_type:'GIT_HOST',verification_source:'github'});
    assert.equal(result(f).provisional_ready,true);assert.equal(result(f).authoritative_merge_eligible,false);
    has(f,'AUTHORITATIVE_SOURCE_POLICY_UNACCEPTED');has(f,'FRESH_PREMERGE_CHECK_UNAVAILABLE');
    assert.ok(result(f).observed_gates.every(g=>g.authoritative_satisfied===false));
  }finally{f.cleanup();}
});
for(const risk of ['R3','R4'] as const) test(risk+' requires both streams even with security_required=false',()=>{
  const f=ready({security:false});try{sql(f,"UPDATE task_workflow SET risk_class='"+risk+"' WHERE task_id='B2-T'");recordedPolicy(f,{security_required:false});
    assert.equal(gate(f,'SECURITY_REVIEW').required,true);has(f,'MISSING_SECURITY_REVIEW');
  }finally{f.cleanup();}
});
for(const risk of ['R0','R1','R2'] as const) {
  test(risk+' explicitly optional Security is NOT_REQUIRED, never PASS',()=>{
    const f=ready({security:false});try{sql(f,"UPDATE task_workflow SET risk_class='"+risk+"' WHERE task_id='B2-T'");recordedPolicy(f,{security_required:false});
      assert.equal(result(f).provisional_ready,true);const g=gate(f,'SECURITY_REVIEW');assert.equal(g.requirement_status,'NOT_REQUIRED');assert.equal(g.recorded_satisfied,false);
      assert.equal(gate(f,'QUALITY_REVIEW').required,true);
    }finally{f.cleanup();}
  });
  test(risk+' unknown conditional Security requirement fails closed',()=>{
    const f=ready();try{sql(f,"UPDATE task_workflow SET risk_class='"+risk+"' WHERE task_id='B2-T'");recordedPolicy(f,{security_required:undefined});
      has(f,'SECURITY_REQUIREMENT_UNRESOLVED');assert.equal(result(f).provisional_ready,false);
    }finally{f.cleanup();}
  });
}
test('optional Security with unresolved blocking findings still blocks task readiness',()=>{
  const f=ready({security:false});try{sql(f,"UPDATE task_workflow SET risk_class='R1' WHERE task_id='B2-T'");recordedPolicy(f,{security_required:false});
    review(f,'SECURITY',{verdict:'REQUEST_CHANGES',blocking:1});has(f,'STOP_CONDITION_PRESENT');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
test('optional re-review in progress does not erase the preceding unresolved finding',()=>{
  const f=ready({security:false});try{sql(f,"UPDATE task_workflow SET risk_class='R1' WHERE task_id='B2-T'");recordedPolicy(f,{security_required:false});
    review(f,'SECURITY',{verdict:'REQUEST_CHANGES',blocking:1});
    const s=f.store.v2.getAssignments('B2-T').find(a=>a.role==='SECURITY_REVIEWER')!;
    f.store.v2.startReview(reviewStart(Number(s.id),'SECURITY'));
    has(f,'STOP_CONDITION_PRESENT');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
test('recorded Human reference without provenance does not satisfy task authorization',()=>{
  const f=ready();try{const prior=query(f,"SELECT id FROM evidence_verifications WHERE subject_key='AUTH-T' ORDER BY verification_version DESC")[0]!;
    f.store.v2.recordVerification(verification({expected_effective_verification_id:Number(prior.id),verification_source:undefined,verification_reference:undefined,metadata_json:JSON.stringify({merge_policy:policy})}));
    has(f,'HUMAN_AUTHORIZATION_PROVENANCE_MISSING');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
test('future task freeze and incomplete dependency are unresolved stop conditions',()=>{
  const f=ready();try{sql(f,"UPDATE tasks SET frozen_until=9999999999999 WHERE id='B2-T'");has(f,'STOP_CONDITION_PRESENT');
    sql(f,"UPDATE tasks SET frozen_until=NULL WHERE id='B2-T'; INSERT INTO tasks(id,title,priority,status) VALUES ('DEP-T','synthetic',2,'PLANNED'); INSERT INTO dependencies VALUES ('B2-T','DEP-T')");has(f,'STOP_CONDITION_PRESENT');
  }finally{f.cleanup();}
});
test('required Human exception must be recorded then verified separately',()=>{
  const f=ready();try{recordedPolicy(f,{required_human_exception_refs:['EXCEPTION-T']});has(f,'HUMAN_EXCEPTION_MISSING');
    attest(f,'HUMAN_AUTHORIZATION','EXCEPTION-T',undefined,{verification_level:'RECORDED'});
    assert.equal(result(f).provisional_ready,true);assert.equal(gate(f,'HUMAN_EXCEPTION:EXCEPTION-T').authoritative_satisfied,false);
  }finally{f.cleanup();}
});
test('revoked Human exception does not satisfy the explicit required list',()=>{
  const f=ready();try{recordedPolicy(f,{required_human_exception_refs:['EXCEPTION-T']});
    attest(f,'HUMAN_AUTHORIZATION','EXCEPTION-T',undefined,{decision:'REVOKE',verification_level:'UNVERIFIED'});
    has(f,'VERIFICATION_REVOKED');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
const boundaries:Array<[Partial<MergePolicy>,string]>=[[{stop_conditions:['synthetic stop']},'STOP_CONDITION_PRESENT'],[{scope_violation:true},'SCOPE_VIOLATION'],[{secret_or_confidential_exposure:true},'SECRET_OR_CONFIDENTIAL_EXPOSURE']];
for(const [change,code] of boundaries) {
  test('recorded boundary '+code+' stops readiness',()=>{const f=ready();try{recordedPolicy(f,change);has(f,code);assert.equal(result(f).provisional_ready,false);}finally{f.cleanup();}});
}
test('malformed or missing required policy is unresolved rather than guessed',()=>{
  const f=ready();try{const prior=query(f,"SELECT id FROM evidence_verifications WHERE subject_key='AUTH-T' ORDER BY verification_version DESC")[0]!;
    f.store.v2.recordVerification(verification({expected_effective_verification_id:Number(prior.id),metadata_json:JSON.stringify({merge_policy:{security_required:false}})}));
    has(f,'MERGE_POLICY_UNRESOLVED');assert.equal(result(f).provisional_ready,false);
  }finally{f.cleanup();}
});
test('old PR head verification is retained stale for new candidate',()=>{
  const f=ready();try{attest(f,'PR_BRANCH_STATE','synthetic/repo#42@'+B);f.store.v2.recordImplementation(implementation(f.implementer,C,Number(f.candidate.id)));
    const e=result(f).effective_verifications.find(e=>e.subject_type==='PR_BRANCH_STATE')!;assert.equal(e.stale,true);assert.equal(e.applicable,false);has(f,'PR_HEAD_NOT_VERIFIED');
  }finally{f.cleanup();}
});
test('wrong repository/PR verification cannot satisfy expected exact context',()=>{
  const f=ready();try{attest(f,'PR_BRANCH_STATE','other/repo#43@'+B);has(f,'PR_HEAD_NOT_VERIFIED');assert.equal(gate(f,'PR_BRANCH_STATE').evidence_present,false);}finally{f.cleanup();}
});
test('missing PR context and fresh checker block authority without blocking provisional readiness',()=>{
  const f=ready();try{recordedPolicy(f,{repository:undefined,pr_number:undefined});assert.equal(result(f).provisional_ready,true);has(f,'PR_CONTEXT_MISSING');has(f,'FRESH_PREMERGE_CHECK_UNAVAILABLE');}finally{f.cleanup();}
});
test('MERGE_RESULT is visible post-merge history and never a pre-merge requirement',()=>{
  const f=ready();try{assert.equal(result(f).observed_gates.some(g=>g.subject_type==='MERGE_RESULT'),false);
    attest(f,'MERGE_RESULT','synthetic/repo@'+C);const e=result(f).effective_verifications.find(e=>e.subject_type==='MERGE_RESULT')!;
    assert.equal(e.chain_valid,true);assert.equal(e.verification_level,'VERIFIED');assert.equal(e.authority_validated,false);assert.equal(result(f).provisional_ready,true);
  }finally{f.cleanup();}
});
test('restart reconstructs identical gate output without rewriting evidence',()=>{
  const f=ready();try{attest(f,'PR_BRANCH_STATE','synthetic/repo#42@'+B);const before=result(f);const data=dump(f);f.restart();assert.deepEqual(result(f),before);assert.equal(dump(f),data);}finally{f.cleanup();}
});
test('gate reads and V2 get_state are idempotent and do not expire leases or mutate any table',()=>{
  const f=ready();try{sql(f,"UPDATE tasks SET lease_expiry=1 WHERE id='B2-T'; UPDATE task_assignments SET lease_expiry=1 WHERE role='IMPLEMENTER'");
    f.store.setBudget(8);const before=dump(f);const first=result(f);assert.deepEqual(result(f),first);
    const state=f.store.getState('B2-T') as {tasks:Array<{merge_gate:Result}>};assert.deepEqual(state.tasks[0]!.merge_gate,first);
    f.store.getState();assert.equal(dump(f),before);assert.equal(f.store.budget().decision,'STOP_AND_CHECKPOINT');
  }finally{f.cleanup();}
});
test('one WAL read snapshot cannot combine candidate A with concurrently committed B',()=>{
  const f=ready();const db=new DatabaseSync(f.file);
  try{sql(f,`INSERT INTO implementation_evidence(task_id,spec_sha,base_sha,implementation_sha,evidence_ref,recorded_by_assignment_id,created_at) VALUES ('B2-T','${A}','${A}','${C}','synthetic',${f.implementer},1)`);
    db.exec('BEGIN');db.prepare("SELECT id FROM tasks WHERE id='B2-T'").get();
    sql(f,`UPDATE task_workflow SET current_implementation_evidence_id=(SELECT id FROM implementation_evidence WHERE implementation_sha='${C}') WHERE task_id='B2-T'`);
    const snapshot=computeMergeGate(db,'B2-T') as Result;assert.equal(snapshot.implementation_sha,B);assert.equal(snapshot.provisional_ready,true);
    db.exec('COMMIT');assert.equal(result(f).implementation_sha,C);assert.equal(result(f).provisional_ready,false);
    assert.throws(()=>computeMergeGate(db,'B2-T'),/snapshot/);
  }finally{db.close();f.cleanup();}
});
test('V1 gate is NOT_APPLICABLE and creates no synthetic V2 records or budget changes',()=>{
  const f=fixture(false);try{const before=dump(f);const g=f.store.v2.getMergeGate('B2-T') as {workflow_version:number;status:string};
    assert.equal(g.workflow_version,1);assert.equal(g.status,'NOT_APPLICABLE');assert.equal(dump(f),before);
    const state=f.store.getState('B2-T') as {tasks:Array<Record<string,unknown>>};assert.equal('merge_gate' in state.tasks[0]!,false);
  }finally{f.cleanup();}
});
test('unknown task remains an explicit error without inserts',()=>{
  const f=ready();try{const before=dump(f);assert.throws(()=>f.store.v2.getMergeGate('MISSING-T'),/Unknown task/);assert.equal(dump(f),before);}finally{f.cleanup();}
});
