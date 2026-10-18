import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { A,B,governance,fixture,verification,checkpoint } from './v2-fixture.js';

test('real stdio MCP launches offline with no API key and preserves 13 V1 tools plus 11 B2 tools and one B3 read', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'orchestrator-mcp-'));
  const server = join(dirname(fileURLToPath(import.meta.url)), '../src/server.js');
  const env = Object.fromEntries(
    Object.entries(process.env).filter(([key,value]) => key !== 'OPENAI_API_KEY' && value !== undefined)
  ) as Record<string,string>;
  env.PROJECT_ORCH_DB = join(dir,'state.sqlite');
  // AC-01/02/10: local CLI registration is visible through exact-ID lookup,
  // while the public MCP registration tool surface remains unchanged.
  const input=join(dir,'synthetic-register.json');
  writeFileSync(input,JSON.stringify({
    manifest_version:1,task_id:'SYNTH-STDIO-01',title:'Synthetic stdio registration',priority:3,
    dependencies:[],authorization_ref:'https://github.com/nshaokiet/ai-ip-description-generator/issues/999#issuecomment-123',
    frozen_until_epoch_ms:null
  }));
  const register=spawnSync(process.execPath,[join(dirname(server),'admin.js'),'register-task',input],{env,encoding:'utf8'});
  assert.equal(register.status,0,register.stderr);
  assert.equal(JSON.parse(register.stdout).outcome,'CREATED');
  const transport = new StdioClientTransport({ command: process.execPath, args: [server], env, stderr: 'pipe' });
  const client = new Client({ name: 'offline-test-client', version: '0.1.0' });
  try {
    await client.connect(transport);
    const names = (await client.listTools()).tools.map(tool => tool.name);
    assert.equal(names.length,25);
    for (const name of ['project.get_state','project.next_task','project.claim_task','project.renew_lease','project.release_task','project.report_progress','project.finish_task','budget.get','budget.set_remaining','budget.should_continue','checkpoint.create','checkpoint.get_latest','project.stop_and_handoff']) assert.ok(names.includes(name));
    for (const name of ['project.assign_role','project.get_assignments','project.submit_spec','project.freeze_spec','project.get_spec','project.start_implementation','project.record_implementation','project.record_ci','review.start','review.submit','review.get_status']) assert.ok(names.includes(name));
    assert.equal(names.includes('project.record_verification'),false); // Admin recording path only in B2.
    assert.equal(names.includes('project.claim_task'),true);
    assert.ok(names.includes('project.get_merge_gate'));
    assert.equal(names.some(name=>/register[-_]?task/.test(name)),false);
    assert.equal(names.some(name => /merge|reset|activate/.test(name) && name!=='project.get_merge_gate'),false);
    const result = await client.callTool({ name: 'budget.should_continue', arguments: {} });
    assert.equal(result.isError,undefined);
    assert.equal((result.structuredContent as { result: { decision: string } }).result.decision,'CONTINUE');
    const registered=await client.callTool({name:'project.get_state',arguments:{task_id:'SYNTH-STDIO-01'}});
    assert.equal(registered.isError,undefined);
    const item=(registered.structuredContent as {result:{tasks:Array<{status:string;approval_ref:string|null;owner:string|null}>}}).result.tasks[0]!;
    assert.equal(item.status,'PLANNED');assert.equal(item.approval_ref,null);assert.equal(item.owner,null);
    const missing=await client.callTool({name:'project.get_state',arguments:{task_id:'SYNTH-UNKNOWN'}});
    assert.equal(missing.isError,true);
  } finally {
    await client.close();
    rmSync(dir,{ recursive: true, force: true });
  }
});

test('real stdio B2 tools and isolated admin enrollment/verification execute a complete recorded-evidence flow',async()=>{
  const f=fixture(false);
  const server=join(dirname(fileURLToPath(import.meta.url)),'../src/server.js');
  const admin=join(dirname(server),'admin.js');
  const env=Object.fromEntries(Object.entries(process.env).filter(([key,value])=>key!=='OPENAI_API_KEY'&&value!==undefined)) as Record<string,string>;
  env.PROJECT_ORCH_DB=f.file;
  const runAdmin=(action:string,p:unknown)=>{
    const file=join(f.dir,'admin-input.json');writeFileSync(file,JSON.stringify(p));
    const result=spawnSync(process.execPath,[admin,action,file],{env,encoding:'utf8'});
    assert.equal(result.status,0,result.stderr);return JSON.parse(result.stdout) as {id:number};
  };
  const enrollment=runAdmin('enroll-v2',{task_id:'B2-T',risk_class:'R3',authorization_ref:'AUTH-T',activation_commit:A});
  assert.ok(enrollment);
  const client=new Client({name:'offline-b2-test',version:'0.2.0'});
  const transport=new StdioClientTransport({command:process.execPath,args:[server],env,stderr:'pipe'});
  try {
    await client.connect(transport);
    const call=async(name:string,p:Record<string,unknown>)=>{
      const r=await client.callTool({name,arguments:p});assert.equal(r.isError,undefined,JSON.stringify(r.content));
      return (r.structuredContent as {result:Record<string,unknown>}).result;
    };
    const planner=await call('project.assign_role',{task_id:'B2-T',...governance,role:'PLANNER',agent_id:'planner',authorization_ref:'ASSIGN-T'});
    const implementer=await call('project.assign_role',{task_id:'B2-T',...governance,role:'IMPLEMENTER',agent_id:'implementer',authorization_ref:'ASSIGN-T'});
    const security=await call('project.assign_role',{task_id:'B2-T',...governance,role:'SECURITY_REVIEWER',agent_id:'security',authorization_ref:'ASSIGN-T'});
    const quality=await call('project.assign_role',{task_id:'B2-T',...governance,role:'QUALITY_REVIEWER',agent_id:'quality',authorization_ref:'ASSIGN-T'});
    const spec={task_id:'B2-T',assignment_id:planner.id,spec_version:'1',spec_sha:A,artifact_path:'synthetic/spec.md',authorization_ref:'AUTH-T'};
    await call('project.submit_spec',{...spec,status:'DRAFT'});await call('project.submit_spec',{...spec,status:'READY'});
    const approval=runAdmin('record-verification',verification({metadata_json:JSON.stringify({human_authorized:true,committed_artifact_exists:true,spec_version:'1',spec_sha:A,artifact_path:'synthetic/spec.md'})}));
    await call('project.freeze_spec',{task_id:'B2-T',...governance,spec_version:'1',spec_sha:A,approval_ref:'AUTH-T',approval_verification_id:approval.id,expected_frozen_spec_id:null});
    await call('project.start_implementation',{task_id:'B2-T',implementer_assignment_id:implementer.id,spec_sha:A,branch:'feat/mcp-b2',worktree:'/synthetic/mcp'});
    const candidate=await call('project.record_implementation',{task_id:'B2-T',assignment_id:implementer.id,spec_sha:A,base_sha:A,implementation_sha:B,evidence_ref:'git:synthetic',expected_current_implementation_evidence_id:null});
    await call('project.record_ci',{task_id:'B2-T',implementation_sha:B,status:'SUCCESS',reference:'synthetic:run',source:'synthetic',recorded_by:'automation'});
    for(const [type,a,reviewer] of [['SECURITY',security,'security'],['QUALITY',quality,'quality']] as const) {
      const start=await call('review.start',{task_id:'B2-T',review_type:type,assignment_id:a.id,spec_sha:A,base_sha:A,implementation_sha:B});
      await call('review.submit',{review_id:start.id,assignment_id:a.id,verdict:'PASS',findings_ref:'synthetic:NONE',blocking_findings:0,evidence_ref:'synthetic:review',artifact_path:'synthetic/review.md',reviewer,tracked_files_modified:false});
    }
    assert.equal(((await call('review.get_status',{task_id:'B2-T'})).security as {status:string}).status,'PASS');
    await call('checkpoint.create',{task_id:'B2-T',owner:'security',role:'SECURITY_REVIEWER',assignment_id:security.id,...checkpoint});
    assert.equal((await call('checkpoint.get_latest',{task_id:'B2-T',role:'SECURITY_REVIEWER'})).assignment_id,security.id);
    const state=await call('project.get_state',{task_id:'B2-T'});
    const task=(state.tasks as Array<{current_implementation:{id:number};workflow_v2_governance:string}>)[0]!;
    assert.equal(task.current_implementation.id,candidate.id);assert.equal(task.workflow_v2_governance,'NOT ACTIVATED');
    assert.ok(await call('project.get_assignments',{task_id:'B2-T'}));assert.ok(await call('project.get_spec',{task_id:'B2-T'}));
    assert.equal((await client.callTool({name:'project.claim_task',arguments:{task_id:'B2-T',owner:'impostor',branch:'feat/bypass',worktree:'/bypass'}})).isError,true);
    assert.equal((await client.callTool({name:'project.freeze_spec',arguments:{task_id:'B2-T',actor_type:'PLANNER'}})).isError,true);
    assert.equal((await client.listTools()).tools.some(t=>/record_verification|enroll/.test(t.name)),false);
    const gate=await call('project.get_merge_gate',{task_id:'B2-T'});
    assert.equal(gate.authoritative_merge_eligible,false);
    assert.equal(gate.implementation_sha,B);
    assert.deepEqual((task as unknown as {merge_gate:unknown}).merge_gate,gate);
    assert.equal((await call('project.get_merge_gate',{task_id:'P1-006'})).status,'NOT_APPLICABLE');
  } finally { await client.close();f.cleanup(); }
});
