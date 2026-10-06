import { mkdtempSync,rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Store } from '../src/store.js';
import type { VerificationInput,ImplementationInput,ReviewStartInput } from '../src/v2-contracts.js';

export const A='a'.repeat(40), B='b'.repeat(40), C='c'.repeat(40), D='d'.repeat(40);
export const governance={actor_type:'ADMIN' as const,actor_id:'human-operator'};
export function fixture(enroll=true) {
  const dir=mkdtempSync(join(tmpdir(),'orch-b2-')),file=join(dir,'state.sqlite');
  let store=new Store(file);
  store.addTask('B2-T','Synthetic B2',1); store.approveTask('B2-T','AUTH-T');
  if (enroll) store.v2.enroll({task_id:'B2-T',risk_class:'R3',authorization_ref:'AUTH-T',activation_commit:A});
  return {dir,file,get store(){return store;},restart(){store.close();store=new Store(file);},cleanup(){store.close();rmSync(dir,{recursive:true,force:true});}};
}
export function assign(store:Store,role:'PLANNER'|'IMPLEMENTER'|'SECURITY_REVIEWER'|'QUALITY_REVIEWER',agent=role.toLowerCase()) {
  return store.v2.assignRole({task_id:'B2-T',...governance,role,agent_id:agent,authorization_ref:'ASSIGN-T'});
}
export function verification(extra:Partial<VerificationInput>={}):VerificationInput {
  return {task_id:'B2-T',...governance,subject_type:'HUMAN_AUTHORIZATION',subject_key:'AUTH-T',decision:'ATTEST',verification_level:'RECORDED',expected_effective_verification_id:null,recorded_by:'human-operator',verification_source:'human-controlled-record',verification_reference:'synthetic:AUTH-T',...extra};
}
export function frozen(store:Store,version='1.0.0',specSha=A,expected:number|null=null) {
  const planner=store.v2.getAssignments('B2-T').find(r=>r.role==='PLANNER' && r.status==='ACTIVE')??assign(store,'PLANNER');
  const spec=store.v2.submitSpec({task_id:'B2-T',assignment_id:Number(planner.id),spec_version:version,spec_sha:specSha,artifact_path:'synthetic/spec.md',authorization_ref:'AUTH-'+version,status:'READY'});
  const approval=store.v2.recordVerification(verification({subject_key:'AUTH-'+version,metadata_json:JSON.stringify({human_authorized:true,committed_artifact_exists:true,spec_version:version,spec_sha:specSha,artifact_path:'synthetic/spec.md'})}));
  return store.v2.freezeSpec({task_id:'B2-T',...governance,spec_version:version,spec_sha:specSha,approval_ref:'AUTH-'+version,approval_verification_id:Number(approval.id),expected_frozen_spec_id:expected});
}
export function started(store:Store) {
  frozen(store);
  const implementer=assign(store,'IMPLEMENTER');
  store.v2.startImplementation({task_id:'B2-T',implementer_assignment_id:Number(implementer.id),spec_sha:A,branch:'feat/synthetic-b2',worktree:'/synthetic/b2'});
  return Number(implementer.id);
}
export function implementation(assignment:number,sha=B,expected:number|null=null,specSha=A):ImplementationInput {
  return {task_id:'B2-T',assignment_id:assignment,spec_sha:specSha,base_sha:A,implementation_sha:sha,evidence_ref:'git:'+sha,expected_current_implementation_evidence_id:expected};
}
export function reviewStart(assignment:number,type:'SECURITY'|'QUALITY',sha=B):ReviewStartInput {
  return {task_id:'B2-T',assignment_id:assignment,review_type:type,spec_sha:A,base_sha:A,implementation_sha:sha};
}
export const checkpoint={last_safe_commit:B,completed_work:'Synthetic milestone',tests:['offline PASS'],remaining_work:'review',blockers:[],stop_reason:'checkpoint',exact_next_action:'resume'};
