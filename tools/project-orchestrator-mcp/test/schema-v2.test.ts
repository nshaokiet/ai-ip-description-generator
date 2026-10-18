import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { CURRENT_SCHEMA_VERSION, migrateDatabase } from '../src/migrations.js';
import { Store } from '../src/store.js';

const SHA_A = 'a'.repeat(40);
const SHA_B = 'b'.repeat(40);
const SHA_C = 'c'.repeat(40);

function tempDatabase(prefix = 'orchestrator-v2-') {
  const dir = mkdtempSync(join(tmpdir(), prefix));
  const file = join(dir, 'state.sqlite');
  return { dir, file, cleanup: () => rmSync(dir, { recursive: true, force: true }) };
}

function db(file: string): DatabaseSync {
  const conn = new DatabaseSync(file);
  conn.exec('PRAGMA foreign_keys=ON');
  return conn;
}

function createLegacy(file: string): void {
  const conn = db(file);
  try {
    conn.exec(`
      CREATE TABLE tasks (
        id TEXT PRIMARY KEY, title TEXT NOT NULL, priority INTEGER NOT NULL, status TEXT NOT NULL,
        owner TEXT, branch TEXT, worktree TEXT, lease_start INTEGER, lease_expiry INTEGER,
        frozen_until INTEGER, blockers TEXT, approval_ref TEXT
      );
      CREATE TABLE dependencies (
        task_id TEXT NOT NULL REFERENCES tasks(id), requires_id TEXT NOT NULL REFERENCES tasks(id),
        PRIMARY KEY(task_id,requires_id)
      );
      CREATE TABLE budget (
        id INTEGER PRIMARY KEY CHECK(id=1), remaining REAL NOT NULL, threshold REAL NOT NULL,
        source TEXT NOT NULL, cycle TEXT NOT NULL, updated_at INTEGER NOT NULL
      );
      CREATE TABLE progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL REFERENCES tasks(id),
        owner TEXT NOT NULL, payload TEXT NOT NULL, created_at INTEGER NOT NULL
      );
      CREATE TABLE checkpoints (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL REFERENCES tasks(id),
        owner TEXT NOT NULL, branch TEXT, last_safe_commit TEXT, completed_work TEXT NOT NULL,
        tests TEXT NOT NULL, remaining_work TEXT NOT NULL, blockers TEXT NOT NULL,
        stop_reason TEXT NOT NULL, exact_next_action TEXT NOT NULL, created_at INTEGER NOT NULL
      );
    `);
    conn.prepare('INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)').run(
      'LEGACY-A', 'legacy a', 1, 'IN_PROGRESS', 'legacy-owner', 'feat/legacy-a', '/w/legacy-a',
      100, 200, null, null, 'legacy-approval'
    );
    conn.prepare('INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)').run(
      'LEGACY-B', 'legacy b', 2, 'PLANNED', null, null, null, null, null, null, null, null
    );
    conn.prepare('INSERT INTO dependencies VALUES (?,?)').run('LEGACY-B', 'LEGACY-A');
    conn.prepare('INSERT INTO budget VALUES (1,?,?,?,?,?)').run(6.5, 8, 'manual', 'legacy-cycle', 123);
    conn.prepare('INSERT INTO progress(task_id,owner,payload,created_at) VALUES (?,?,?,?)')
      .run('LEGACY-A', 'legacy-owner', JSON.stringify({ milestone: 'legacy-progress' }), 124);
    conn.prepare(`INSERT INTO checkpoints(
      task_id,owner,branch,last_safe_commit,completed_work,tests,remaining_work,blockers,
      stop_reason,exact_next_action,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)`).run(
      'LEGACY-A', 'legacy-owner', 'feat/legacy-a', SHA_A, 'legacy checkpoint', '["legacy pass"]',
      'legacy remaining', '[]', 'legacy stop', 'legacy next', 125
    );
  } finally { conn.close(); }
}

type EvidenceFixture = {
  implId: number; specId: number; ciId: number; securityReviewId: number; qualityReviewId: number;
};

function createEvidenceFixture(file: string): EvidenceFixture {
  const store = new Store(file);
  try {
    store.addTask('V2-A', 'v2 a', 1);
    store.addTask('V2-B', 'v2 b', 2);
  } finally { store.close(); }
  const conn = db(file);
  try {
    const implementer = Number(conn.prepare(`INSERT INTO task_assignments(
      task_id,role,agent_id,status,assignment_version,assigned_at,branch,worktree,lease_start,lease_expiry
    ) VALUES (?,?,?,?,?,?,?,?,?,?)`).run(
      'V2-A', 'IMPLEMENTER', 'impl-agent', 'ACTIVE', 1, 1, 'feat/v2-a', '/w/v2-a', 1, 1000
    ).lastInsertRowid);
    const security = Number(conn.prepare(`INSERT INTO task_assignments(
      task_id,role,agent_id,status,assignment_version,assigned_at,started_at,completed_at
    ) VALUES (?,?,?,?,?,?,?,?)`).run(
      'V2-A', 'SECURITY_REVIEWER', 'security-agent', 'COMPLETED', 1, 1, 2, 3
    ).lastInsertRowid);
    const quality = Number(conn.prepare(`INSERT INTO task_assignments(
      task_id,role,agent_id,status,assignment_version,assigned_at,started_at,completed_at
    ) VALUES (?,?,?,?,?,?,?,?)`).run(
      'V2-A', 'QUALITY_REVIEWER', 'quality-agent', 'COMPLETED', 1, 1, 2, 3
    ).lastInsertRowid);
    const specId = Number(conn.prepare(`INSERT INTO task_specs(
      task_id,spec_version,spec_sha,status,authorization_ref,artifact_path,created_at,frozen_at
    ) VALUES (?,?,?,?,?,?,?,?)`).run(
      'V2-A', '1.0.0', SHA_A, 'FROZEN', 'AUTH-V2-A', 'docs/tasks/v2-a.md', 1, 2
    ).lastInsertRowid);
    const implId = Number(conn.prepare(`INSERT INTO implementation_evidence(
      task_id,spec_sha,base_sha,implementation_sha,evidence_ref,recorded_by_assignment_id,created_at
    ) VALUES (?,?,?,?,?,?,?)`).run(
      'V2-A', SHA_A, SHA_B, SHA_C, 'git:impl-c', implementer, 3
    ).lastInsertRowid);
    conn.prepare(`INSERT INTO task_workflow(
      task_id,workflow_version,risk_class,authorization_ref,activation_commit,current_implementation_evidence_id,created_at
    ) VALUES (?,?,?,?,?,?,?)`).run('V2-A', '2', 'R2', 'AUTH-V2-A', SHA_A, implId, 4);
    conn.prepare(`INSERT INTO task_workflow(
      task_id,workflow_version,risk_class,authorization_ref,activation_commit,current_implementation_evidence_id,created_at
    ) VALUES (?,?,?,?,?,?,?)`).run('V2-B', '2', 'R1', 'AUTH-V2-B', SHA_A, null, 4);
    const ciId = Number(conn.prepare(`INSERT INTO ci_evidence(
      task_id,implementation_sha,status,reference,source,recorded_by,created_at
    ) VALUES (?,?,?,?,?,?,?)`).run(
      'V2-A', SHA_C, 'SUCCESS', 'run-1', 'github-actions', 'impl-agent', 5
    ).lastInsertRowid);
    const securityReviewId = Number(conn.prepare(`INSERT INTO reviews(
      task_id,review_type,reviewer_assignment_id,spec_sha,base_sha,implementation_sha,attempt,
      verdict,findings_ref,blocking_findings,evidence_ref,artifact_path,reviewer,model_profile,
      created_at,tracked_files_modified
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`).run(
      'V2-A', 'SECURITY', security, SHA_A, SHA_B, SHA_C, 1, 'PASS', 'findings:none', 0,
      'review:security', 'docs/reviews/V2-A/security.md', 'security-agent', 'profile', 6, 0
    ).lastInsertRowid);
    const qualityReviewId = Number(conn.prepare(`INSERT INTO reviews(
      task_id,review_type,reviewer_assignment_id,spec_sha,base_sha,implementation_sha,attempt,
      verdict,findings_ref,blocking_findings,evidence_ref,artifact_path,reviewer,model_profile,
      created_at,tracked_files_modified
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`).run(
      'V2-A', 'QUALITY', quality, SHA_A, SHA_B, SHA_C, 1, 'PASS', 'findings:none', 0,
      'review:quality', 'docs/reviews/V2-A/quality.md', 'quality-agent', 'profile', 6, 0
    ).lastInsertRowid);
    return { implId, specId, ciId, securityReviewId, qualityReviewId };
  } finally { conn.close(); }
}

function insertVerification(
  conn: DatabaseSync,
  data: {
    subjectType: string; subjectKey: string; version?: number; supersedes?: number | null;
    taskSpecId?: number | null; implId?: number | null; ciId?: number | null; reviewId?: number | null;
    decision?: 'ATTEST' | 'REVOKE'; level?: 'UNVERIFIED' | 'RECORDED' | 'VERIFIED'; verified?: boolean;
  }
): number {
  const verified = data.verified ?? false;
  return Number(conn.prepare(`INSERT INTO evidence_verifications(
    task_id,subject_type,subject_key,task_spec_id,implementation_evidence_id,ci_evidence_id,review_id,
    verification_version,supersedes_verification_id,decision,verification_level,recorded_by,
    verifier_type,verifier_id,verification_source,verification_reference,verified_at,created_at,metadata_json
  ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`).run(
    'V2-A', data.subjectType, data.subjectKey, data.taskSpecId ?? null, data.implId ?? null,
    data.ciId ?? null, data.reviewId ?? null, data.version ?? 1, data.supersedes ?? null,
    data.decision ?? 'ATTEST', data.level ?? 'RECORDED', 'recorder',
    verified ? 'GIT_HOST' : null, verified ? 'github' : null, verified ? 'github' : null,
    verified ? 'ref-verified' : null, verified ? 10 : null, 10, null
  ).lastInsertRowid);
}

test('fresh database initializes V1 plus B1 and B2 additive schemas without enrolling V2 tasks', () => {
  const f = tempDatabase();
  try {
    const store = new Store(f.file); store.close();
    const conn = db(f.file);
    try {
      const versions = conn.prepare('SELECT version FROM schema_migrations ORDER BY version').all() as Array<{ version: number }>;
      assert.deepEqual(versions.map(row => row.version), [1, 2, 3, CURRENT_SCHEMA_VERSION]);
      const tables = new Set((conn.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>).map(row => row.name));
      for (const name of ['tasks','dependencies','budget','progress','checkpoints','task_workflow','task_assignments','task_specs','implementation_evidence','reviews','ci_evidence','evidence_verifications']) assert.ok(tables.has(name));
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM task_workflow').get() as { n: number }).n, 0);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('legacy V1 database migrates additively and preserves rows, owner/lease, progress, checkpoints, dependencies and budget', () => {
  const f = tempDatabase();
  try {
    createLegacy(f.file);
    const store = new Store(f.file); store.close();
    const conn = db(f.file);
    try {
      const task = conn.prepare('SELECT * FROM tasks WHERE id=?').get('LEGACY-A') as Record<string, unknown>;
      assert.equal(task.owner, 'legacy-owner');
      assert.equal(task.branch, 'feat/legacy-a');
      assert.equal(task.worktree, '/w/legacy-a');
      assert.equal(task.lease_start, 100);
      assert.equal(task.lease_expiry, 200);
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM dependencies WHERE task_id=? AND requires_id=?').get('LEGACY-B','LEGACY-A') as { n: number }).n, 1);
      assert.equal((conn.prepare('SELECT payload FROM progress WHERE task_id=?').get('LEGACY-A') as { payload: string }).payload, JSON.stringify({ milestone: 'legacy-progress' }));
      assert.equal((conn.prepare('SELECT exact_next_action FROM checkpoints WHERE task_id=?').get('LEGACY-A') as { exact_next_action: string }).exact_next_action, 'legacy next');
      const budget = conn.prepare('SELECT remaining,threshold,source,cycle,updated_at FROM budget WHERE id=1').get() as Record<string, unknown>;
      assert.deepEqual({ ...budget }, { remaining: 6.5, threshold: 8, source: 'manual', cycle: 'legacy-cycle', updated_at: 123 });
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM task_workflow').get() as { n: number }).n, 0);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('migration is idempotent and schema/version state survives restart', () => {
  const f = tempDatabase();
  try {
    createLegacy(f.file);
    for (let i = 0; i < 3; i++) { const store = new Store(f.file); store.close(); }
    const conn = db(f.file);
    try {
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM schema_migrations').get() as { n: number }).n, CURRENT_SCHEMA_VERSION);
      assert.equal((conn.prepare('SELECT MAX(version) AS v FROM schema_migrations').get() as { v: number }).v, CURRENT_SCHEMA_VERSION);
      assert.equal((conn.prepare("SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name='evidence_verifications'").get() as { n: number }).n, 1);
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM tasks WHERE id=?').get('LEGACY-A') as { n: number }).n, 1);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('failed incompatible migration rolls back all migration-created objects and preserves prior V1 data', () => {
  const f = tempDatabase();
  try {
    createLegacy(f.file);
    const conn = db(f.file);
    conn.exec('CREATE TABLE task_workflow(task_id TEXT PRIMARY KEY)');
    conn.close();
    assert.throws(() => new Store(f.file), /task_workflow|no such column|incompatible/i);
    const after = db(f.file);
    try {
      assert.equal((after.prepare('SELECT owner FROM tasks WHERE id=?').get('LEGACY-A') as { owner: string }).owner, 'legacy-owner');
      assert.equal((after.prepare("SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name='schema_migrations'").get() as { n: number }).n, 0);
      assert.equal((after.prepare("SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name='task_assignments'").get() as { n: number }).n, 0);
    } finally { after.close(); }
  } finally { f.cleanup(); }
});

test('version-2 metadata with incompatible objects fails closed instead of resetting or repairing silently', () => {
  const f = tempDatabase();
  try {
    createLegacy(f.file);
    const conn = db(f.file);
    conn.exec('CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY,description TEXT NOT NULL,applied_at INTEGER NOT NULL)');
    conn.prepare('INSERT INTO schema_migrations VALUES (2,?,?)').run('bad metadata', 1);
    conn.close();
    assert.throws(() => new Store(f.file), /Schema version 2 is incompatible/);
    const after = db(f.file);
    try { assert.equal((after.prepare('SELECT title FROM tasks WHERE id=?').get('LEGACY-A') as { title: string }).title, 'legacy a'); }
    finally { after.close(); }
  } finally { f.cleanup(); }
});

test('future schema version is rejected without resetting the database', () => {
  const f = tempDatabase();
  try {
    createLegacy(f.file);
    const conn = db(f.file);
    conn.exec('CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY,description TEXT NOT NULL,applied_at INTEGER NOT NULL)');
    conn.prepare('INSERT INTO schema_migrations VALUES (99,?,?)').run('future', 1);
    conn.close();
    assert.throws(() => new Store(f.file), /newer than supported version 4/);
    const after = db(f.file);
    try { assert.equal((after.prepare('SELECT COUNT(*) AS n FROM tasks WHERE id=?').get('LEGACY-A') as { n: number }).n, 1); }
    finally { after.close(); }
  } finally { f.cleanup(); }
});

test('V2 indexes and core assignment/spec constraints are installed', () => {
  const f = tempDatabase();
  try {
    const store = new Store(f.file); store.addTask('V2-T', 'v2 t', 1); store.close();
    const conn = db(f.file);
    try {
      const indexes = new Set((conn.prepare("SELECT name FROM sqlite_master WHERE type='index' AND name IS NOT NULL").all() as Array<{ name: string }>).map(row => row.name));
      for (const name of ['uq_task_assignments_active_role','uq_task_specs_frozen','uq_evidence_verifications_supersedes','idx_task_workflow_candidate']) assert.ok(indexes.has(name));
      conn.prepare('INSERT INTO task_assignments(task_id,role,agent_id,status,assignment_version,assigned_at) VALUES (?,?,?,?,?,?)')
        .run('V2-T','PLANNER','p','ACTIVE',1,1);
      assert.throws(() => conn.prepare('INSERT INTO task_assignments(task_id,role,agent_id,status,assignment_version,assigned_at) VALUES (?,?,?,?,?,?)')
        .run('V2-T','PLANNER','p2','ASSIGNED',2,2));
      assert.throws(() => conn.prepare('INSERT INTO task_assignments(task_id,role,agent_id,status,assignment_version,assigned_at,branch) VALUES (?,?,?,?,?,?,?)')
        .run('V2-T','QUALITY_REVIEWER','q','COMPLETED',1,1,'forbidden'));
      conn.prepare('INSERT INTO task_specs(task_id,spec_version,spec_sha,status,authorization_ref,artifact_path,created_at) VALUES (?,?,?,?,?,?,?)')
        .run('V2-T','1',SHA_A,'FROZEN','a','x',1);
      assert.throws(() => conn.prepare('INSERT INTO task_specs(task_id,spec_version,spec_sha,status,authorization_ref,artifact_path,created_at) VALUES (?,?,?,?,?,?,?)')
        .run('V2-T','2',SHA_B,'FROZEN','b','y',2));
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-07 implementation evidence is unique per task/SHA and duplicate SHA cannot fork identity', () => {
  const f = tempDatabase();
  try {
    const ids = createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      assert.throws(() => conn.prepare(`INSERT INTO implementation_evidence(
        task_id,spec_sha,base_sha,implementation_sha,evidence_ref,created_at
      ) VALUES (?,?,?,?,?,?)`).run('V2-A', SHA_A, SHA_A, SHA_C, 'conflicting duplicate', 99));
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM implementation_evidence WHERE task_id=? AND implementation_sha=?').get('V2-A',SHA_C) as { n: number }).n, 1);
      assert.equal((conn.prepare('SELECT current_implementation_evidence_id AS id FROM task_workflow WHERE task_id=?').get('V2-A') as { id: number }).id, ids.implId);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-07 current candidate pointer persists across restart and rejects cross-task pointer misuse', () => {
  const f = tempDatabase();
  try {
    const ids = createEvidenceFixture(f.file);
    let store = new Store(f.file); store.close();
    store = new Store(f.file); store.close();
    const conn = db(f.file);
    try {
      assert.equal((conn.prepare('SELECT current_implementation_evidence_id AS id FROM task_workflow WHERE task_id=?').get('V2-A') as { id: number }).id, ids.implId);
      assert.throws(() => conn.prepare('UPDATE task_workflow SET current_implementation_evidence_id=? WHERE task_id=?').run(ids.implId, 'V2-B'));
      assert.equal((conn.prepare('SELECT current_implementation_evidence_id AS id FROM task_workflow WHERE task_id=?').get('V2-B') as { id: number | null }).id, null);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-07 schema supports expected-current compare-and-swap candidate transitions', () => {
  const f = tempDatabase();
  try {
    const ids = createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      const implementer = Number((conn.prepare("SELECT id FROM task_assignments WHERE task_id='V2-A' AND role='IMPLEMENTER'").get() as { id: number }).id);
      const nextId = Number(conn.prepare(`INSERT INTO implementation_evidence(
        task_id,spec_sha,base_sha,implementation_sha,evidence_ref,recorded_by_assignment_id,created_at
      ) VALUES (?,?,?,?,?,?,?)`).run('V2-A',SHA_A,SHA_B,SHA_B,'git:impl-b',implementer,20).lastInsertRowid);
      const won = conn.prepare(`UPDATE task_workflow SET current_implementation_evidence_id=?
        WHERE task_id=? AND current_implementation_evidence_id=?`).run(nextId,'V2-A',ids.implId);
      assert.equal(Number(won.changes), 1);
      const stale = conn.prepare(`UPDATE task_workflow SET current_implementation_evidence_id=?
        WHERE task_id=? AND current_implementation_evidence_id=?`).run(ids.implId,'V2-A',ids.implId);
      assert.equal(Number(stale.changes), 0);
      assert.equal((conn.prepare('SELECT current_implementation_evidence_id AS id FROM task_workflow WHERE task_id=?').get('V2-A') as { id: number }).id, nextId);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-07/F-08 use one candidate pointer and one verification persistence model', () => {
  const f = tempDatabase();
  try {
    const store = new Store(f.file); store.close();
    const conn = db(f.file);
    try {
      const columns = (table: string) => new Set((conn.prepare(`PRAGMA table_info(${table})`).all() as Array<{ name: string }>).map(row => row.name));
      const workflow = columns('task_workflow');
      const implementation = columns('implementation_evidence');
      const ci = columns('ci_evidence');
      const reviews = columns('reviews');
      assert.ok(workflow.has('current_implementation_evidence_id'));
      for (const forbidden of ['is_current','current','latest','verification_level','verified']) assert.equal(implementation.has(forbidden), false);
      for (const forbidden of ['verification_level','verification_status','verified']) assert.equal(ci.has(forbidden), false);
      for (const forbidden of ['verification_level','verification_status','verified']) assert.equal(reviews.has(forbidden), false);
      assert.ok(columns('evidence_verifications').has('verification_level'));
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-08 typed internal subjects accept canonical IDs and reject wrong subject keys or cross-task IDs', () => {
  const f = tempDatabase();
  try {
    const ids = createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      insertVerification(conn, { subjectType: 'SPECIFICATION', subjectKey: String(ids.specId), taskSpecId: ids.specId });
      insertVerification(conn, { subjectType: 'IMPLEMENTATION', subjectKey: String(ids.implId), implId: ids.implId });
      insertVerification(conn, { subjectType: 'CI', subjectKey: String(ids.ciId), ciId: ids.ciId });
      assert.throws(() => insertVerification(conn, { subjectType: 'IMPLEMENTATION', subjectKey: 'wrong', implId: ids.implId }));
      const foreignSpec = Number(conn.prepare(`INSERT INTO task_specs(
        task_id,spec_version,spec_sha,status,authorization_ref,artifact_path,created_at
      ) VALUES (?,?,?,?,?,?,?)`).run('V2-B','1',SHA_B,'READY','AUTH-B','b.md',1).lastInsertRowid);
      assert.throws(() => insertVerification(conn, { subjectType: 'SPECIFICATION', subjectKey: String(foreignSpec), taskSpecId: foreignSpec }));
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-08 Security and Quality verification subjects must match stored review type', () => {
  const f = tempDatabase();
  try {
    const ids = createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      insertVerification(conn, { subjectType: 'SECURITY_REVIEW', subjectKey: String(ids.securityReviewId), reviewId: ids.securityReviewId });
      insertVerification(conn, { subjectType: 'QUALITY_REVIEW', subjectKey: String(ids.qualityReviewId), reviewId: ids.qualityReviewId });
      assert.throws(() => insertVerification(conn, { subjectType: 'SECURITY_REVIEW', subjectKey: String(ids.qualityReviewId), reviewId: ids.qualityReviewId }), /SECURITY_REVIEW/);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-08 external subjects require no internal FK and unsupported subject types fail', () => {
  const f = tempDatabase();
  try {
    createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-V2-A' });
      insertVerification(conn, { subjectType: 'PR_BRANCH_STATE', subjectKey: 'repo#42@' + SHA_A });
      insertVerification(conn, { subjectType: 'MERGE_RESULT', subjectKey: 'repo@' + SHA_B });
      assert.throws(() => insertVerification(conn, { subjectType: 'OTHER', subjectKey: 'x' }));
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-08 verification chain enforces versions, immediate supersession, no gaps and no forks', () => {
  const f = tempDatabase();
  try {
    createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      const v1 = insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-V2-A' });
      const v2 = insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-V2-A', version: 2, supersedes: v1 });
      assert.ok(v2 > v1);
      assert.throws(() => insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-V2-A', version: 2, supersedes: v1 }));
      assert.throws(() => insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-V2-A', version: 4, supersedes: v2 }), /previous version/);
      assert.throws(() => insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-V2-A', version: 3, supersedes: v1 }), /previous version/);
      assert.throws(() => insertVerification(conn, { subjectType: 'PR_BRANCH_STATE', subjectKey: 'pr', version: 1, supersedes: v1 }), /version 1/);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-08 VERIFIED attestation requires verifier provenance and REVOKE is only UNVERIFIED', () => {
  const f = tempDatabase();
  try {
    createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      assert.throws(() => insertVerification(conn, {
        subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-VERIFIED', level: 'VERIFIED'
      }));
      const v1 = insertVerification(conn, {
        subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-VERIFIED', level: 'VERIFIED', verified: true
      });
      assert.throws(() => insertVerification(conn, {
        subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-VERIFIED', version: 2, supersedes: v1,
        decision: 'REVOKE', level: 'RECORDED'
      }));
      const v2 = insertVerification(conn, {
        subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-VERIFIED', version: 2, supersedes: v1,
        decision: 'REVOKE', level: 'UNVERIFIED'
      });
      assert.ok(v2 > v1);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('implementation, review, CI and verification evidence are append-only', () => {
  const f = tempDatabase();
  try {
    const ids = createEvidenceFixture(f.file);
    const conn = db(f.file);
    try {
      const verificationId = insertVerification(conn, { subjectType: 'CI', subjectKey: String(ids.ciId), ciId: ids.ciId });
      assert.throws(() => conn.prepare('UPDATE implementation_evidence SET evidence_ref=? WHERE id=?').run('changed',ids.implId), /append-only/);
      assert.throws(() => conn.prepare('DELETE FROM reviews WHERE review_id=?').run(ids.securityReviewId), /append-only/);
      assert.throws(() => conn.prepare('UPDATE ci_evidence SET status=? WHERE id=?').run('FAILURE',ids.ciId), /append-only/);
      assert.throws(() => conn.prepare('DELETE FROM evidence_verifications WHERE id=?').run(verificationId), /append-only/);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('F-08 verification history remains deterministic after Store restart', () => {
  const f = tempDatabase();
  try {
    createEvidenceFixture(f.file);
    let conn = db(f.file);
    const v1 = insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-HISTORY' });
    insertVerification(conn, { subjectType: 'HUMAN_AUTHORIZATION', subjectKey: 'AUTH-HISTORY', version: 2, supersedes: v1, level: 'VERIFIED', verified: true });
    const before = conn.prepare(`SELECT id,verification_version,supersedes_verification_id,decision,verification_level
      FROM evidence_verifications WHERE subject_key=? ORDER BY verification_version`).all('AUTH-HISTORY');
    conn.close();
    const store = new Store(f.file); store.close();
    conn = db(f.file);
    try {
      const after = conn.prepare(`SELECT id,verification_version,supersedes_verification_id,decision,verification_level
        FROM evidence_verifications WHERE subject_key=? ORDER BY verification_version`).all('AUTH-HISTORY');
      assert.deepEqual(after, before);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('SQLite safety pragmas remain foreign_keys ON, WAL and busy_timeout 5000', () => {
  const f = tempDatabase();
  try {
    const conn = new DatabaseSync(f.file);
    try {
      conn.exec('PRAGMA busy_timeout=5000; PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON');
      migrateDatabase(conn);
      assert.equal((conn.prepare('PRAGMA foreign_keys').get() as { foreign_keys: number }).foreign_keys, 1);
      assert.equal((conn.prepare('PRAGMA journal_mode').get() as { journal_mode: string }).journal_mode.toLowerCase(), 'wal');
      assert.equal((conn.prepare('PRAGMA busy_timeout').get() as { timeout: number }).timeout, 5000);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});

test('concurrent legacy initialization deterministically reaches schema version 2 once', async () => {
  const f = tempDatabase('orchestrator-v2-race-');
  try {
    createLegacy(f.file);
    const worker = join(dirname(fileURLToPath(import.meta.url)), 'migration-worker.js');
    const start = () => new Promise<string>((resolve, reject) => {
      const child = spawn(process.execPath, [worker, f.file], { stdio: ['ignore','pipe','pipe'] });
      let output = ''; let error = '';
      child.stdout.on('data', chunk => { output += String(chunk); });
      child.stderr.on('data', chunk => { error += String(chunk); });
      child.on('error', reject);
      child.on('close', code => code === 0 ? resolve(output) : reject(new Error(error)));
    });
    assert.deepEqual((await Promise.all([start(), start()])).sort(), ['READY','READY']);
    const conn = db(f.file);
    try {
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM schema_migrations WHERE version=2').get() as { n: number }).n, 1);
      assert.equal((conn.prepare('SELECT COUNT(*) AS n FROM tasks WHERE id=?').get('LEGACY-A') as { n: number }).n, 1);
    } finally { conn.close(); }
  } finally { f.cleanup(); }
});
