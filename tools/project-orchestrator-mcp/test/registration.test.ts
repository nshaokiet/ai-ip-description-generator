import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';
import { Store } from '../src/store.js';
import { readRegistrationManifest, validateRegistration, type RegistrationManifest } from '../src/registration.js';

const receipt = 'https://github.com/nshaokiet/ai-ip-description-generator/issues/999#issuecomment-123';
const admin = join(dirname(fileURLToPath(import.meta.url)), '../src/admin.js');
const manifest = (task_id = 'SYNTH-REG-001', other: Partial<RegistrationManifest> = {}): RegistrationManifest => ({
  manifest_version:1, task_id, title:'Synthetic task', priority:5, dependencies:[],
  authorization_ref:receipt, frozen_until_epoch_ms:null, ...other
});
function fixture() {
  const dir = mkdtempSync(join(tmpdir(), 'gov-reg-'));
  const file = join(dir,'test.sqlite');
  const store = new Store(file);
  return {dir,file,store, cleanup() { store.close(); rmSync(dir,{recursive:true,force:true}); }};
}
const db = (file:string) => { const d = new DatabaseSync(file); d.exec('PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000'); return d; };
const rows = (file:string) => {
  const d=db(file);
  try {
    return {
      tasks:d.prepare('SELECT * FROM tasks ORDER BY id').all(),
      deps:d.prepare('SELECT * FROM dependencies ORDER BY task_id,requires_id').all(),
      regs:d.prepare('SELECT * FROM task_registrations ORDER BY task_id').all(),
      progress:d.prepare('SELECT * FROM progress ORDER BY id').all(),
      checkpoints:d.prepare('SELECT * FROM checkpoints ORDER BY id').all(),
      budget:d.prepare('SELECT * FROM budget').all()
    };
  } finally { d.close(); }
};
function cli(dir:string,file:string,m:unknown,filename='manifest.json') {
  const path=join(dir,filename);
  writeFileSync(path,JSON.stringify(m));
  return runCli(file,path);
}
function runCli(file:string,...args:string[]) {
  return spawnSync(process.execPath,[admin,'register-task',...args],{
    env:{...process.env,PROJECT_ORCH_DB:file},encoding:'utf8',timeout:15000
  });
}
function asyncCli(file:string,path:string):Promise<{code:number|null;stdout:string;stderr:string}> {
  return new Promise((resolve,reject) => {
    const p=spawn(process.execPath,[admin,'register-task',path],{env:{...process.env,PROJECT_ORCH_DB:file}});
    let stdout='';let stderr='';
    p.stdout.on('data',s=>stdout+=String(s));p.stderr.on('data',s=>stderr+=String(s));
    p.on('error',reject);p.on('exit',code=>resolve({code,stdout,stderr}));
  });
}

test('AC-01/02/07: PLANNED exact lookup, unknown read, and no implicit approval or claim',()=>{
  const f=fixture();
  try {
    const before=rows(f.file);
    assert.throws(()=>f.store.getState('SYNTH-ABSENT'),/Unknown task/);
    assert.deepEqual(rows(f.file),before);
    assert.deepEqual(f.store.registerTask(manifest()),{outcome:'CREATED',task_id:'SYNTH-REG-001',status:'PLANNED'});
    const state=(f.store.getState('SYNTH-REG-001') as {tasks:Array<Record<string,unknown>>}).tasks[0]!;
    for (const key of ['approval_ref','owner','branch','worktree','lease_start','lease_expiry','blockers']) assert.equal(state[key],null);
    assert.equal(state.status,'PLANNED');assert.equal(state.workflow_version,1);
    assert.throws(()=>f.store.claim('SYNTH-REG-001','a','feat/a','/tmp/a'),/eligible/);
    assert.throws(()=>f.store.transition('SYNTH-REG-001','COMPLETED','fake'),/invalid/);
    assert.throws(()=>f.store.checkpoint('SYNTH-REG-001','a',{
      last_safe_commit:null,completed_work:'x',tests:[],remaining_work:'x',blockers:[],stop_reason:'x',exact_next_action:'x'
    }),/lease/);
    assert.equal(rows(f.file).regs.length,1);
  } finally { f.cleanup(); }
});

test('AC-03/05: normalized dependency order is idempotent after approval, lease, and restart',()=>{
  const f=fixture();let closed=false;
  try {
    const a=manifest('SYNTH-REG-002',{dependencies:['P1-002','P1-001']});
    assert.equal(f.store.registerTask(a).outcome,'CREATED');
    f.store.approveTask(a.task_id,'synthetic separate Human approval');
    const before=rows(f.file);
    assert.equal(f.store.registerTask(manifest(a.task_id,{dependencies:['P1-001','P1-002']})).outcome,'ALREADY_REGISTERED');
    assert.deepEqual(rows(f.file),before);
    f.store.close();closed=true;
    const again=new Store(f.file);
    try {
      assert.equal(again.registerTask(a).outcome,'ALREADY_REGISTERED');
      assert.deepEqual(rows(f.file),before);
    } finally { again.close(); }
  } finally { if(!closed) f.store.close();rmSync(f.dir,{recursive:true,force:true}); }
});

test('AC-04: legacy seed collision and all canonical/static drifts fail closed',()=>{
  const f=fixture();
  try {
    assert.throws(()=>f.store.registerTask(manifest('P1-001')),/REGISTRATION_CONFLICT/);
    const id='SYNTH-CONFLICT';const base=manifest(id);
    f.store.registerTask(base);
    const baseline=rows(f.file);
    for(const variation of [
      {title:'Different'}, {priority:6}, {dependencies:['P1-001']},
      {frozen_until_epoch_ms:0},
      {authorization_ref:'https://github.com/nshaokiet/ai-ip-description-generator/pull/999#discussion_r99'}
    ]) {
      assert.throws(()=>f.store.registerTask(manifest(id,variation)),/REGISTRATION_CONFLICT/);
      assert.deepEqual(rows(f.file),baseline);
    }
    const d=db(f.file);
    try { d.prepare('UPDATE tasks SET title=? WHERE id=?').run('drift',id); } finally {d.close();}
    const drift=rows(f.file);
    assert.throws(()=>f.store.registerTask(base),/REGISTRATION_CONFLICT/);
    assert.deepEqual(rows(f.file),drift);
  } finally {f.cleanup();}
});

test('AC-06: invalid fields, path, duplicate escaped JSON keys and unsafe URLs are rejected',()=>{
  const f=fixture();
  try {
    const invalid:unknown[]=[
      {...manifest(),extra:true}, {...manifest(),manifest_version:2},
      {...manifest(),task_id:'lower-case'}, {...manifest(),title:' bad'},
      {...manifest(),title:'\u0000'}, {...manifest(),priority:101},
      {...manifest(),dependencies:['P1-001','P1-001']},
      {...manifest(),dependencies:['SYNTH-REG-001']},
      {...manifest(),frozen_until_epoch_ms:-1},
      {...manifest(),authorization_ref:'https://github.com:443/nshaokiet/ai-ip-description-generator/issues/1#issuecomment-1'},
      {...manifest(),authorization_ref:'https://github.com/nshaokiet/ai-ip-description-generator/issues/%31#issuecomment-1'},
      {...manifest(),authorization_ref:'https://github.com/nshaokiet/ai-ip-description-generator/issues/1?token=123#issuecomment-1'},
      {...manifest(),authorization_ref:'https://github.com@evil.test/nshaokiet/ai-ip-description-generator/issues/1#issuecomment-1'},
      {...manifest(),authorization_ref:'https://github.com/other/repo/issues/1#issuecomment-1'},
      {...manifest(),authorization_ref:'https://github.com/nshaokiet/ai-ip-description-generator/issues/1'},
      {...manifest(),title:'a'.repeat(201)}
    ];
    for(const m of invalid) assert.throws(()=>validateRegistration(m),/REGISTRATION_INVALID_MANIFEST/);
    const before=rows(f.file);
    assert.notEqual(runCli(f.file,'relative.json').status,0);
    const path=join(f.dir,'duplicate.json');
    writeFileSync(path,JSON.stringify(manifest()).replace('"task_id"','"task_id" : "SYNTH-REG-001", "task\\u005fid"'));
    assert.throws(()=>readRegistrationManifest(path),/REGISTRATION_INVALID_MANIFEST/);
    assert.notEqual(runCli(f.file,path).status,0);
    writeFileSync(path,Buffer.from([0xff,0xfe,0x7b]));
    assert.notEqual(runCli(f.file,path).status,0);
    writeFileSync(path,'x'.repeat(65537));
    assert.notEqual(runCli(f.file,path).status,0);
    assert.deepEqual(rows(f.file),before);
  } finally {f.cleanup();}
});

test('AC-06: missing edges and existing reachable cycle reject without partial writes',()=>{
  const f=fixture();
  try {
    assert.throws(()=>f.store.registerTask(manifest('SYNTH-MISSING',{dependencies:['MISSING-01']})),/REGISTRATION_DEPENDENCY/);
    f.store.addTask('SYNTH-CYCLE-A','A',1);
    f.store.addTask('SYNTH-CYCLE-B','B',1,['SYNTH-CYCLE-A']);
    const d=db(f.file);
    try { d.prepare('INSERT INTO dependencies(task_id,requires_id) VALUES (?,?)').run('SYNTH-CYCLE-A','SYNTH-CYCLE-B'); }
    finally { d.close(); }
    const before=rows(f.file);
    assert.throws(()=>f.store.registerTask(manifest('SYNTH-NEW',{dependencies:['SYNTH-CYCLE-A']})),/REGISTRATION_DEPENDENCY/);
    assert.deepEqual(rows(f.file),before);
  } finally {f.cleanup();}
});

test('AC-05/10: schema v3 migration preserves legacy snapshots, provenance is immutable, restart idempotent',()=>{
  const f=fixture();let closed=false;
  try {
    f.store.approveTask('P1-001','synthetic-approval');
    f.store.setBudget(12,'synthetic-budget');
    f.store.close();closed=true;
    const d=db(f.file);
    try {
      d.exec('DROP TRIGGER trg_task_registrations_no_update; DROP TRIGGER trg_task_registrations_no_delete; DROP TABLE task_registrations; DELETE FROM schema_migrations WHERE version=4');
    } finally {d.close();}
    const baseline=new DatabaseSync(f.file);
    const prior={
      tasks:baseline.prepare('SELECT * FROM tasks ORDER BY id').all(),
      deps:baseline.prepare('SELECT * FROM dependencies ORDER BY task_id,requires_id').all(),
      budget:baseline.prepare('SELECT * FROM budget').all(),
      v2:baseline.prepare('SELECT * FROM evidence_verifications').all()
    };
    baseline.close();
    const upgraded=new Store(f.file);
    try {
      const now=rows(f.file);
      assert.deepEqual(now.tasks,prior.tasks);assert.deepEqual(now.deps,prior.deps);
      assert.deepEqual(now.budget,prior.budget);assert.equal(now.regs.length,0);
      upgraded.registerTask(manifest());
      const persisted=rows(f.file);
      upgraded.close();
      const restart=new Store(f.file);
      try { assert.deepEqual(rows(f.file),persisted); } finally {restart.close();}
    } catch (e) {try {upgraded.close();} catch {} throw e;}
    const check=db(f.file);
    try {
      assert.throws(()=>check.prepare('UPDATE task_registrations SET registered_at=0').run(),/immutable/);
      assert.throws(()=>check.prepare('DELETE FROM task_registrations').run(),/immutable/);
      assert.equal(check.prepare('PRAGMA foreign_key_check').get(),undefined);
      assert.equal((check.prepare('PRAGMA integrity_check').get() as {integrity_check:string}).integrity_check,'ok');
    } finally {check.close();}
  } finally {if(!closed)f.store.close();rmSync(f.dir,{recursive:true,force:true});}
});

test('AC-10: corrupted v4 triggers and future schema markers fail closed',()=>{
  const f=fixture();let closed=false;
  try {
    f.store.close();closed=true;
    const d=db(f.file);
    d.exec('DROP TRIGGER trg_task_registrations_no_delete');d.close();
    assert.throws(()=>new Store(f.file),/Schema version 4 is incompatible/);
    const other=join(f.dir,'future.sqlite');
    const s=new Store(other);s.close();
    const future=db(other);
    future.prepare('INSERT INTO schema_migrations(version,description,applied_at) VALUES (5,?,?)').run('synthetic future',Date.now());future.close();
    assert.throws(()=>new Store(other),/newer than supported/);
  } finally {if(!closed)f.store.close();rmSync(f.dir,{recursive:true,force:true});}
});

test('AC-08: registered task retains owner, lease, branch and handoff protections',()=>{
  const f=fixture();
  try {
    f.store.registerTask(manifest());f.store.approveTask('SYNTH-REG-001','synthetic separate approval');
    f.store.claim('SYNTH-REG-001','right-owner','feat/registered','/tmp/register');
    const snapshot=rows(f.file);
    assert.equal(f.store.registerTask(manifest()).outcome,'ALREADY_REGISTERED');
    assert.deepEqual(rows(f.file),snapshot);
    assert.throws(()=>f.store.renew('SYNTH-REG-001','wrong-owner'),/lease/);
    assert.throws(()=>f.store.release('SYNTH-REG-001','wrong-owner'),/lease/);
    assert.throws(()=>f.store.claim('SYNTH-REG-001','another','feat/registered','/tmp/register'),/eligible/);
    assert.throws(()=>f.store.stopAndHandoff('SYNTH-REG-001','wrong-owner',{
      last_safe_commit:null,completed_work:'x',tests:[],remaining_work:'x',blockers:[],stop_reason:'x',exact_next_action:'x'
    }),/lease/);
    assert.equal((f.store.getState('SYNTH-REG-001') as {tasks:Array<{owner:string}>}).tasks[0]!.owner,'right-owner');
  } finally {f.cleanup();}
});

test('AC-09: independent simultaneous CLI writers create exactly one record',async()=>{
  const f=fixture();
  try {
    const path=join(f.dir,'concurrent.json');writeFileSync(path,JSON.stringify(manifest()));
    const results=await Promise.all([asyncCli(f.file,path),asyncCli(f.file,path)]);
    for(const r of results) assert.equal(r.code,0,r.stderr);
    assert.deepEqual(results.map(r=>JSON.parse(r.stdout).outcome).sort(),['ALREADY_REGISTERED','CREATED']);
    const before=rows(f.file);
    const changed=cli(f.dir,f.file,manifest('SYNTH-REG-001',{title:'conflict'}),'conflict.json');
    assert.notEqual(changed.status,0);assert.match(changed.stderr,/REGISTRATION_CONFLICT/);
    assert.deepEqual(rows(f.file),before);
  } finally {f.cleanup();}
});

test('AC-09/10: lock contention times out without writes and CLI leaks no receipt',()=>{
  const f=fixture();
  try {
    const path=join(f.dir,'locked.json');writeFileSync(path,JSON.stringify(manifest()));
    const d=db(f.file);
    try {
      d.exec('BEGIN IMMEDIATE');
      const outcome=runCli(f.file,path);
      assert.notEqual(outcome.status,0);assert.match(outcome.stderr,/REGISTRATION_DB_BUSY/);
      assert.doesNotMatch(outcome.stderr,/github\.com|manifest\.json/);
    } finally {d.exec('ROLLBACK');d.close();}
    assert.equal(rows(f.file).regs.length,0);
    const done=runCli(f.file,path);
    assert.equal(done.status,0,done.stderr);
    assert.equal(JSON.parse(done.stdout).outcome,'CREATED');
  } finally {f.cleanup();}
});
