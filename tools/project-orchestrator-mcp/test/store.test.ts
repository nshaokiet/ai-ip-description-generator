import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { Store } from '../src/store.js';

const SHA = 'a'.repeat(40);
function fixture() {
  const dir = mkdtempSync(join(tmpdir(), 'orchestrator-'));
  const file = join(dir, 'state.sqlite');
  const store = new Store(file);
  return { file, store, cleanup() { store.close(); rmSync(dir, { recursive: true, force: true }); } };
}
function approved(s: Store, id = 'TEST-001', deps: string[] = []) {
  s.addTask(id, id, 0, deps);
  s.approveTask(id, 'human-decision-test');
}
const details = {
  last_safe_commit: SHA, completed_work: 'service done', tests: ['offline pass'],
  remaining_work: 'review code', blockers: [], stop_reason: 'quota threshold',
  exact_next_action: 'review the safe commit'
};

test('budget is seeded manually at 14/8 and strict boundary is observed', () => {
  const f = fixture();
  try {
    assert.equal(f.store.budget().source, 'manual');
    assert.equal(f.store.budget().decision, 'CONTINUE');
    f.store.setBudget(8.01); assert.equal(f.store.budget().decision, 'CONTINUE');
    f.store.setBudget(8); assert.equal(f.store.budget().decision, 'STOP_AND_CHECKPOINT');
    f.store.setBudget(100, 'weekly-2026-09-26'); assert.equal(f.store.budget().decision, 'CONTINUE');
    assert.equal(f.store.budget().cycle, 'weekly-2026-09-26');
    f.store.setBudget(0); assert.equal(f.store.budget().decision, 'STOP_AND_CHECKPOINT');
  } finally { f.cleanup(); }
});
test('invalid manual remaining budget is rejected', () => {
  const f = fixture();
  try {
    for (const n of [-1, 101, NaN, Infinity]) assert.throws(() => f.store.setBudget(n));
    assert.equal(f.store.budget().remaining, 14);
  } finally { f.cleanup(); }
});
test('future work is only seeded as PLANNED and never claimed automatically', () => {
  const f = fixture();
  try {
    assert.equal(f.store.nextTask(), null);
    assert.equal((f.store.getState('P0-001') as { tasks: Array<{ status: string }> }).tasks[0]!.status, 'PLANNED');
    assert.equal((f.store.getState('P1-001') as { tasks: Array<{ status: string }> }).tasks[0]!.status, 'PLANNED');
    assert.equal((f.store.getState('P1-006') as { tasks: Array<{ status: string }> }).tasks[0]!.status, 'PLANNED');
    assert.throws(() => f.store.claim('P0-001','a','task/app003','/worktree/a'));
    assert.throws(() => f.store.claim('P1-001','a','feat/p1-001','/worktree/p1-001'));
  } finally { f.cleanup(); }
});

test('P1 roadmap is seeded in order and dependency-gated', () => {
  const f = fixture();
  try {
    f.store.approveTask('P1-002','human-approve-p1-002');
    assert.equal(f.store.nextTask(), null);

    f.store.approveTask('P1-001','human-approve-p1-001');
    assert.equal(f.store.nextTask()?.id, 'P1-001');

    f.store.claim('P1-001','agent','feat/p1-001','/w/p1-001');
    f.store.finish('P1-001','agent',['offline pass'],SHA);
    for (const [state,evidence] of [
      ['AWAITING_REVIEW','review opened'], ['REVIEW_PASS','review pass'],
      ['AWAITING_HUMAN_APPROVAL','human gate'], ['MERGED','human merge evidence'],
      ['COMPLETED','closeout evidence']
    ] as const) f.store.transition('P1-001',state,evidence);

    assert.equal(f.store.nextTask()?.id, 'P1-002');
  } finally { f.cleanup(); }
});
test('active task can only be claimed once across two SQLite connections', () => {
  const f = fixture();
  const second = new Store(f.file);
  try {
    approved(f.store);
    f.store.claim('TEST-001','antigravity','task/one','/worktree/one');
    assert.throws(() => second.claim('TEST-001','vscode','task/two','/worktree/two'));
    f.store.release('TEST-001','antigravity');
    assert.equal(second.claim('TEST-001','vscode','task/two','/worktree/two').owner,'vscode');
  } finally { second.close(); f.cleanup(); }
});
test('expired lease is recovered atomically and new owner can claim', () => {
  const f = fixture();
  const original = Date.now;
  try {
    approved(f.store);
    const time = original();
    Date.now = () => time;
    f.store.claim('TEST-001','agent-a','task/one','/w/one',1);
    Date.now = () => time + 60_001;
    assert.equal(f.store.claim('TEST-001','agent-b','task/two','/w/two').owner,'agent-b');
    assert.throws(() => f.store.report('TEST-001','agent-a',{
      milestone:'bad',tests:[],files_changed:[],commit_sha:null,remaining_work:'more',blockers:[]
    }));
  } finally { Date.now = original; f.cleanup(); }
});
test('blocked and completed tasks never return and dependencies require COMPLETED', () => {
  const f = fixture();
  try {
    approved(f.store,'TEST-A');
    approved(f.store,'TEST-B',['TEST-A']);
    assert.equal(f.store.nextTask()?.id,'TEST-A');
    f.store.claim('TEST-A','agent','task/a','/w/a');
    f.store.stopAndHandoff('TEST-A','agent',details);
    assert.equal(f.store.nextTask(),null);
    f.store.approveTask('TEST-A','human-resolve-blocker');
    f.store.claim('TEST-A','agent','task/a2','/w/a2');
    f.store.finish('TEST-A','agent',['unit pass'],SHA);
    assert.equal(f.store.nextTask(),null);
    for (const [state,evidence] of [
      ['AWAITING_REVIEW','review opened'], ['REVIEW_PASS','review pass'],
      ['AWAITING_HUMAN_APPROVAL','human gate'], ['MERGED','human merge evidence'],
      ['COMPLETED','closeout evidence']
    ] as const) f.store.transition('TEST-A',state,evidence);
    assert.equal(f.store.nextTask()?.id,'TEST-B');
  } finally { f.cleanup(); }
});
test('quota stops claim/progress/finish but permits checkpoint and handoff', () => {
  const f = fixture();
  try {
    approved(f.store);
    f.store.claim('TEST-001','agent','task/one','/w/one');
    f.store.setBudget(8);
    assert.equal(f.store.nextTask(),null);
    assert.throws(() => f.store.report('TEST-001','agent',{
      milestone:'step',tests:[],files_changed:[],commit_sha:null,remaining_work:'more',blockers:[]
    }));
    assert.throws(() => f.store.finish('TEST-001','agent',['pass'],SHA));
    const cp = f.store.stopAndHandoff('TEST-001','agent',details);
    assert.equal(cp.branch,'task/one');
    assert.equal(cp.last_safe_commit,SHA);
    assert.deepEqual(cp.tests,['offline pass']);
    assert.equal(cp.stop_reason,'quota threshold');
    assert.equal(cp.exact_next_action,'review the safe commit');
    assert.equal((f.store.getState('TEST-001') as { tasks: Array<{ status: string }> }).tasks[0]!.status,'BLOCKED');
  } finally { f.cleanup(); }
});
test('checkpoints and budget persist after process restart', () => {
  const f = fixture();
  try {
    approved(f.store);
    f.store.claim('TEST-001','agent','task/one','/w/one');
    f.store.checkpoint('TEST-001','agent',details);
    f.store.setBudget(7);
    const reopened = new Store(f.file);
    try {
      assert.equal(reopened.latestCheckpoint('TEST-001')?.exact_next_action,details.exact_next_action);
      assert.equal(reopened.budget().remaining,7);
      assert.equal((reopened.getState('TEST-001') as { tasks: Array<{ owner: string }> }).tasks[0]!.owner,'agent');
    } finally { reopened.close(); }
  } finally { f.cleanup(); }
});
test('branch/worktree collision and main claim rejected', () => {
  const f = fixture();
  try {
    approved(f.store,'TEST-A'); approved(f.store,'TEST-B');
    assert.throws(() => f.store.claim('TEST-A','x','main','/w/a'));
    f.store.claim('TEST-A','x','task/a','/w/a');
    assert.throws(() => f.store.claim('TEST-B','y','task/a','/w/b'));
    assert.throws(() => f.store.claim('TEST-B','y','task/b','/w/a'));
  } finally { f.cleanup(); }
});
test('concurrent process race permits precisely one claim', async () => {
  const f = fixture();
  try {
    approved(f.store,'TEST-RACE');
    const worker = join(dirname(fileURLToPath(import.meta.url)), 'claim-worker.js');
    const start = (name: string) => new Promise<string>((resolve,reject) => {
      const child = spawn(process.execPath,[worker,f.file,name],{stdio:['ignore','pipe','pipe']});
      let output = ''; let error = '';
      child.stdout.on('data',chunk => {output += String(chunk);});
      child.stderr.on('data',chunk => {error += String(chunk);});
      child.on('error',reject);
      child.on('close',code => code === 0 ? resolve(output) : reject(new Error(error)));
    });
    const results = await Promise.all([start('a'),start('b')]);
    assert.deepEqual(results.sort(),['CLAIMED','REJECTED']);
  } finally { f.cleanup(); }
});
test('server exposes no merge or quota reset tool and has no API credentials', () => {
  const path = join(dirname(fileURLToPath(import.meta.url)),'../../src/server.ts');
  // Source is available when test runs from the repository after build.
  const source = readFileSync(path,'utf8');
  const names = [...source.matchAll(/registerTool\('([^']+)'/g)].map(m => m[1]);
  assert.equal(names.length,13);
  assert.equal(names.some(n => /merge|reset|activate/.test(n || '')),false);
  assert.equal(/OPENAI_API_KEY|fetch\(|api\.openai/.test(source),false);
});
