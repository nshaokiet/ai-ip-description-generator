import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, isAbsolute, join } from 'node:path';
import { migrateDatabase } from './migrations.js';
import { V2Store } from './v2-store.js';

export const STATES = [
  'PLANNED', 'APPROVED', 'CLAIMED', 'IN_PROGRESS', 'IMPLEMENTED',
  'AWAITING_REVIEW', 'REVIEW_CHANGES_REQUIRED', 'REVIEW_PASS',
  'AWAITING_HUMAN_APPROVAL', 'MERGED', 'COMPLETED', 'BLOCKED'
] as const;
export type Status = typeof STATES[number];

export type Task = {
  id: string; title: string; priority: number; status: Status;
  owner: string | null; branch: string | null; worktree: string | null;
  lease_start: number | null; lease_expiry: number | null;
  frozen_until: number | null; blockers: string | null; approval_ref: string | null;
};
export type Progress = {
  milestone: string; tests: string[]; files_changed: string[];
  commit_sha: string | null; remaining_work: string; blockers: string[];
};
type Budget = { remaining: number; threshold: number; source: string; cycle: string; updated_at: number };
type Checkpoint = {
  id: number; task_id: string; owner: string; branch: string | null;
  last_safe_commit: string | null; completed_work: string; tests: string[];
  remaining_work: string; blockers: string[]; stop_reason: string;
  exact_next_action: string; created_at: number;
};
const FREEZE = Date.parse('2026-09-25T17:00:00Z'); // 26/09/2026 00:00 in Vietnam
const SEED: Array<[string, string, string | null]> = [
  ['P0-001', 'APP-003 implementation', null],
  ['P0-002', 'APP-003 regression/fixes', 'P0-001'],
  ['P0-003', 'DOCX integration', 'P0-002'],
  ['P0-004', 'Public orchestration API', 'P0-003'],
  ['P0-005', 'Frontend MVP', 'P0-004'],
  ['P0-006', 'Frontend/backend integration', 'P0-005'],
  ['P0-007', 'Full offline E2E', 'P0-006'],
  ['P0-008', 'Final hardening', 'P0-007'],
  ['P1-001', 'Frontend accessibility and type-safety hardening', null],
  ['P1-002', 'Offline adversarial regression expansion', null],
  ['P1-003', 'Local security hardening', null],
  ['P1-004', 'Developer experience and one-command local run', null],
  ['P1-005', 'Offline performance baseline', null],
  ['P1-006', 'UX polish, responsive behavior and error recovery', null],
  ['DEPLOY-001', 'Zero-cost demo/staging deployment', null]
];
const SHA = /^[a-f0-9]{40}$/i;

export function defaultDatabasePath(): string {
  return process.env.PROJECT_ORCH_DB || join(homedir(), '.ai-ip-description-generator', 'project-orchestrator.sqlite');
}

export class Store {
  private readonly db: DatabaseSync;
  readonly v2: V2Store;
  constructor(file = defaultDatabasePath()) {
    if (!isAbsolute(file)) throw new Error('SQLite path must be absolute');
    mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
    this.db = new DatabaseSync(file);
    this.v2 = new V2Store(this.db, () => this.guard());
    try {
      this.db.exec('PRAGMA busy_timeout=5000; PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON');
      migrateDatabase(this.db);
      this.tx(() => {
        this.db.prepare('INSERT OR IGNORE INTO budget VALUES (1, 14, 8, ?, ?, ?)').run('manual', 'initial-weekly-2026-09-25', Date.now());
        for (let i = 0; i < SEED.length; i++) {
          const [id, title, dependency] = SEED[i]!;
          this.db.prepare('INSERT OR IGNORE INTO tasks (id,title,priority,status,frozen_until) VALUES (?,?,?,?,?)')
            .run(id, title, i + 1, 'PLANNED', id === 'P0-001' ? FREEZE : null);
          if (dependency) this.db.prepare('INSERT OR IGNORE INTO dependencies VALUES (?,?)').run(id, dependency);
        }
      });
    } catch (error) {
      this.db.close();
      throw error;
    }
  }
  close(): void { this.db.close(); }
  private tx<T>(body: () => T): T {
    this.db.exec('BEGIN IMMEDIATE');
    try { const result = body(); this.db.exec('COMMIT'); return result; }
    catch (error) { this.db.exec('ROLLBACK'); throw error; }
  }
  private task(id: string): Task {
    const task = this.db.prepare('SELECT * FROM tasks WHERE id=?').get(id) as Task | undefined;
    if (!task) throw new Error('Unknown task: ' + id);
    return task;
  }
  private dependenciesDone(id: string): boolean {
    const pending = this.db.prepare('SELECT COUNT(*) AS n FROM dependencies d JOIN tasks t ON t.id=d.requires_id ' +
      "WHERE d.task_id=? AND t.status!='COMPLETED'").get(id) as { n: number };
    return pending.n === 0;
  }
  private recoverExpired(): void {
    this.v2.recoverExpired();
    this.db.prepare("UPDATE tasks SET status='APPROVED', owner=NULL, branch=NULL, worktree=NULL, " +
      'lease_start=NULL, lease_expiry=NULL WHERE status IN (\'CLAIMED\',\'IN_PROGRESS\') AND lease_expiry<=?')
      .run(Date.now());
  }
  private budgetRow(): Budget { return this.db.prepare('SELECT remaining,threshold,source,cycle,updated_at FROM budget WHERE id=1').get() as Budget; }
  budget(): Budget & { decision: 'CONTINUE' | 'STOP_AND_CHECKPOINT' } {
    const b = this.budgetRow();
    return { ...b, decision: b.remaining > b.threshold ? 'CONTINUE' : 'STOP_AND_CHECKPOINT' };
  }
  setBudget(remaining: number, cycle?: string): ReturnType<Store['budget']> {
    if (!Number.isFinite(remaining) || remaining < 0 || remaining > 100) throw new Error('remaining must be between 0 and 100');
    if (cycle !== undefined && (!cycle.trim() || cycle.length > 120)) throw new Error('cycle must be a short nonempty label');
    this.tx(() => {
      this.db.prepare('UPDATE budget SET remaining=?, source=?, cycle=COALESCE(?,cycle),updated_at=? WHERE id=1')
        .run(remaining, 'manual', cycle ?? null, Date.now());
    });
    return this.budget();
  }
  private guard(): void {
    if (this.budgetRow().remaining <= this.budgetRow().threshold) throw new Error('STOP_AND_CHECKPOINT: quota at or below threshold');
  }
  getState(taskId?: string): object {
    return this.tx(() => {
      this.recoverExpired();
      const tasks = taskId ? [this.task(taskId)] : this.db.prepare(
        "SELECT * FROM tasks WHERE status IN ('CLAIMED','IN_PROGRESS','BLOCKED') ORDER BY priority,id"
      ).all() as Task[];
      return {
        tasks: tasks.map(t => ({ ...t, ...(this.v2.workflow(t.id) ? this.v2.state(t.id) : {workflow_version:1}), latest_checkpoint: this.latestCheckpoint(t.id), next_action:
          t.status === 'BLOCKED' ? 'Human resolves blocker and records approval' :
          t.status === 'CLAIMED' ? 'Start work and report progress' :
          t.status === 'IN_PROGRESS' ? 'Continue work or checkpoint' : 'Review approved task' })),
        budget: this.budget(), next_task: this.findNext()
      };
    });
  }
  private findNext(): Task | null {
    const candidates = this.db.prepare("SELECT * FROM tasks WHERE status='APPROVED' ORDER BY priority,id").all() as Task[];
    return candidates.find(t => (!t.frozen_until || Date.now() >= t.frozen_until) &&
      !t.blockers && this.dependenciesDone(t.id)) || null;
  }
  nextTask(): Task | null {
    return this.tx(() => {
      this.recoverExpired();
      if (this.budgetRow().remaining <= this.budgetRow().threshold) return null;
      return this.findNext();
    });
  }
  addTask(id: string, title: string, priority: number, dependencies: string[] = [], frozenUntil?: number): void {
    if (!/^[A-Z0-9-]{3,50}$/.test(id) || !title.trim() || !Number.isSafeInteger(priority) ||
      priority < 0 || dependencies.includes(id)) throw new Error('Invalid task');
    this.tx(() => {
      this.db.prepare('INSERT INTO tasks (id,title,priority,status,frozen_until) VALUES (?,?,?,?,?)')
        .run(id, title, priority, 'PLANNED', frozenUntil ?? null);
      for (const dep of dependencies) this.db.prepare('INSERT INTO dependencies VALUES (?,?)').run(id, dep);
    });
  }
  // Local administrative operation; intentionally NOT exposed as an MCP tool.
  approveTask(id: string, reference: string): Task {
    if (!reference.trim()) throw new Error('Human approval reference required');
    return this.tx(() => {
      const task = this.task(id);
      if (!['PLANNED','BLOCKED','REVIEW_CHANGES_REQUIRED'].includes(task.status))
        throw new Error('Task cannot be approved from ' + task.status);
      if (task.frozen_until && Date.now() < task.frozen_until) throw new Error('Task is frozen until 26/09/2026 (Vietnam time)');
      this.db.prepare("UPDATE tasks SET status='APPROVED', blockers=NULL, approval_ref=? WHERE id=?").run(reference, id);
      return this.task(id);
    });
  }
  // Administrative evidence transition; no merge or Git action exists here.
  transition(id: string, target: Status, evidence: string): Task {
    if (this.v2.workflow(id)) throw new Error('V2 lifecycle approval/merge transitions deferred to B3');
    const allowed: Partial<Record<Status, Status[]>> = {
      IMPLEMENTED: ['AWAITING_REVIEW'], AWAITING_REVIEW: ['REVIEW_CHANGES_REQUIRED','REVIEW_PASS'],
      REVIEW_PASS: ['AWAITING_HUMAN_APPROVAL'], AWAITING_HUMAN_APPROVAL: ['MERGED'],
      MERGED: ['COMPLETED'], REVIEW_CHANGES_REQUIRED: ['APPROVED']
    };
    if (!evidence.trim() || !(allowed[this.task(id).status] || []).includes(target))
      throw new Error('Evidence or lifecycle transition invalid');
    return this.tx(() => {
      const t = this.task(id);
      if (!(allowed[t.status] || []).includes(target)) throw new Error('Lifecycle changed concurrently');
      this.db.prepare('UPDATE tasks SET status=?,approval_ref=? WHERE id=?').run(target, evidence, id);
      return this.task(id);
    });
  }
  claim(id: string, owner: string, branch: string, worktree: string, leaseMinutes = 60): Task {
    if (!owner.trim() || owner.length > 120 || !branch.trim() || branch === 'main' ||
      branch.startsWith('refs/heads/main') || !worktree.trim() ||
      !Number.isInteger(leaseMinutes) || leaseMinutes < 1 || leaseMinutes > 1440)
      throw new Error('Invalid claim metadata, branch, or lease duration');
    return this.tx(() => {
      this.recoverExpired(); this.guard();
      if (this.v2.workflow(id)) throw new Error('V2 requires project.start_implementation');
      const t = this.task(id);
      if (t.status !== 'APPROVED' || !this.dependenciesDone(id) || t.blockers ||
        (t.frozen_until && Date.now() < t.frozen_until)) throw new Error('Task is not eligible to claim');
      const conflict = this.db.prepare("SELECT id FROM tasks WHERE id!=? AND status IN ('CLAIMED','IN_PROGRESS') " +
        'AND (branch=? OR worktree=?)').get(id, branch, worktree);
      if (conflict) throw new Error('Branch or worktree already leased');
      const now = Date.now();
      this.db.prepare("UPDATE tasks SET status='CLAIMED',owner=?,branch=?,worktree=?,lease_start=?,lease_expiry=? WHERE id=?")
        .run(owner, branch, worktree, now, now + leaseMinutes * 60_000, id);
      return this.task(id);
    });
  }
  private active(id: string, owner: string): Task {
    const t = this.task(id);
    if (!['CLAIMED','IN_PROGRESS'].includes(t.status) || t.owner !== owner ||
      !t.lease_expiry || t.lease_expiry <= Date.now()) throw new Error('Active lease owner required');
    if (this.v2.workflow(id)) this.v2.validateOwner(id, owner);
    return t;
  }
  renew(id: string, owner: string, leaseMinutes = 60): Task {
    if (!Number.isInteger(leaseMinutes) || leaseMinutes < 1 || leaseMinutes > 1440) throw new Error('Invalid lease');
    return this.tx(() => {
      this.guard(); this.active(id, owner);
      this.db.prepare('UPDATE tasks SET lease_expiry=? WHERE id=?').run(Date.now() + leaseMinutes * 60_000, id);
      if (this.v2.workflow(id)) this.v2.syncLease(id, this.task(id).lease_expiry);
      return this.task(id);
    });
  }
  release(id: string, owner: string): Task {
    return this.tx(() => {
      this.active(id, owner);
      this.db.prepare("UPDATE tasks SET status='APPROVED',owner=NULL,branch=NULL,worktree=NULL,lease_start=NULL,lease_expiry=NULL WHERE id=?").run(id);
      if (this.v2.workflow(id)) this.v2.syncLease(id, null);
      return this.task(id);
    });
  }
  report(id: string, owner: string, p: Progress): Task {
    if (!p.milestone.trim() || !p.remaining_work.trim() ||
      (p.commit_sha !== null && !SHA.test(p.commit_sha))) throw new Error('Invalid progress evidence');
    return this.tx(() => {
      this.guard(); this.active(id, owner);
      this.db.prepare('INSERT INTO progress (task_id,owner,payload,created_at) VALUES (?,?,?,?)')
        .run(id, owner, JSON.stringify(p), Date.now());
      this.db.prepare("UPDATE tasks SET status='IN_PROGRESS', blockers=?,lease_expiry=? WHERE id=?")
        .run(p.blockers.length ? JSON.stringify(p.blockers) : null, Date.now() + 60 * 60_000, id);
      if (this.v2.workflow(id)) this.v2.syncLease(id, this.task(id).lease_expiry);
      return this.task(id);
    });
  }
  finish(id: string, owner: string, tests: string[], commitSha: string): Task {
    if (!SHA.test(commitSha) || tests.length === 0) throw new Error('Commit SHA and test evidence required');
    return this.tx(() => {
      this.guard(); this.active(id, owner);
      if (this.v2.workflow(id)) {
        const candidate=this.v2.candidate(id);
        const spec=this.db.prepare("SELECT spec_sha FROM task_specs WHERE task_id=? AND status='FROZEN'").get(id);
        if (!candidate || candidate.implementation_sha!==commitSha.toLowerCase() || candidate.spec_sha!==spec?.spec_sha)
          throw new Error('Finish requires recorded current candidate for frozen spec');
      }
      this.db.prepare("UPDATE tasks SET status='IMPLEMENTED',lease_start=NULL,lease_expiry=NULL WHERE id=?").run(id);
      if (this.v2.workflow(id)) this.v2.syncLease(id, null);
      this.db.prepare('INSERT INTO progress (task_id,owner,payload,created_at) VALUES (?,?,?,?)')
        .run(id, owner, JSON.stringify({ milestone: 'Implementation complete', tests, commit_sha: commitSha }), Date.now());
      return this.task(id);
    });
  }
  latestCheckpoint(id?: string, role?: string): Checkpoint | null {
    if (role && !id) throw new Error('Role checkpoint query requires task ID');
    const row = (role ? this.db.prepare('SELECT c.* FROM checkpoints c JOIN checkpoint_assignments a ON a.checkpoint_id=c.id WHERE c.task_id=? AND a.role=? ORDER BY c.id DESC LIMIT 1').get(id!,role) : id ? this.db.prepare('SELECT * FROM checkpoints WHERE task_id=? ORDER BY id DESC LIMIT 1').get(id) :
      this.db.prepare('SELECT * FROM checkpoints ORDER BY id DESC LIMIT 1').get()) as
      (Omit<Checkpoint,'tests'|'blockers'> & { tests: string; blockers: string }) | undefined;
    const metadata=row ? this.db.prepare('SELECT role,assignment_id FROM checkpoint_assignments WHERE checkpoint_id=?').get(row.id) : undefined;
    return row ? { ...row, ...metadata, tests: JSON.parse(row.tests) as string[], blockers: JSON.parse(row.blockers) as string[] } : null;
  }
  checkpoint(id: string, owner: string, data: Omit<Checkpoint,'id'|'task_id'|'owner'|'branch'|'created_at'>, role?:string, assignmentId?:number): Checkpoint {
    if (!owner.trim() || !data.completed_work.trim() || !data.remaining_work.trim() ||
      !data.stop_reason.trim() || !data.exact_next_action.trim() ||
      (data.last_safe_commit !== null && !SHA.test(data.last_safe_commit))) throw new Error('Incomplete handoff');
    return this.tx(() => {
      const isV2=!!this.v2.workflow(id);
      if (isV2 && (!role || assignmentId===undefined)) throw new Error('V2 checkpoint requires role and assignment ID');
      if (!isV2 && (role || assignmentId!==undefined)) throw new Error('V1 checkpoint does not accept V2 role metadata');
      if (isV2) this.v2.checkpointAssignment(id,owner,role!,assignmentId!);
      const t = isV2 && role!=='IMPLEMENTER' ? this.task(id) : this.active(id, owner);
      const result = this.db.prepare('INSERT INTO checkpoints (task_id,owner,branch,last_safe_commit,completed_work,tests,' +
        'remaining_work,blockers,stop_reason,exact_next_action,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)')
        .run(id, owner, isV2 && role!=='IMPLEMENTER'?null:t.branch, data.last_safe_commit, data.completed_work,
          JSON.stringify(data.tests), data.remaining_work, JSON.stringify(data.blockers),
          data.stop_reason, data.exact_next_action, Date.now());
      if (isV2) this.db.prepare('INSERT INTO checkpoint_assignments(checkpoint_id,task_id,role,assignment_id) VALUES (?,?,?,?)')
        .run(Number(result.lastInsertRowid),id,role!,assignmentId!);
      return this.latestCheckpoint(id,role)!;
    });
  }
  stopAndHandoff(id: string, owner: string, data: Omit<Checkpoint,'id'|'task_id'|'owner'|'branch'|'created_at'>, role?:string,assignmentId?:number): Checkpoint {
    return this.tx(() => {
      this.active(id, owner);
      if (this.v2.workflow(id)) {
        if (role!=='IMPLEMENTER' || assignmentId===undefined) throw new Error('V2 task-blocking handoff requires Implementer metadata');
        this.v2.checkpointAssignment(id,owner,role,assignmentId);
      } else if (role || assignmentId!==undefined) throw new Error('V1 handoff does not accept V2 role metadata');
      const cp = this.checkpointUnsafe(id, owner, data);
      if (this.v2.workflow(id)) this.db.prepare('INSERT INTO checkpoint_assignments(checkpoint_id,task_id,role,assignment_id) VALUES (?,?,?,?)').run(cp.id,id,role!,assignmentId!);
      this.db.prepare("UPDATE tasks SET status='BLOCKED',owner=NULL,lease_start=NULL,lease_expiry=NULL,blockers=? WHERE id=?")
        .run(JSON.stringify([...data.blockers, data.stop_reason]), id);
      if (this.v2.workflow(id)) this.v2.syncLease(id,null,'BLOCKED');
      return this.latestCheckpoint(id)!;
    });
  }
  private checkpointUnsafe(id: string, owner: string, data: Omit<Checkpoint,'id'|'task_id'|'owner'|'branch'|'created_at'>): Checkpoint {
    if (!data.completed_work.trim() || !data.remaining_work.trim() || !data.stop_reason.trim() ||
      !data.exact_next_action.trim() || (data.last_safe_commit !== null && !SHA.test(data.last_safe_commit)))
      throw new Error('Incomplete handoff');
    const t = this.task(id);
    this.db.prepare('INSERT INTO checkpoints (task_id,owner,branch,last_safe_commit,completed_work,tests,' +
      'remaining_work,blockers,stop_reason,exact_next_action,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)')
      .run(id, owner, t.branch, data.last_safe_commit, data.completed_work,
        JSON.stringify(data.tests), data.remaining_work, JSON.stringify(data.blockers),
        data.stop_reason, data.exact_next_action, Date.now());
    return this.latestCheckpoint(id)!;
  }
}
