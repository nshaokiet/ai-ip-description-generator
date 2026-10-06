import { DatabaseSync } from 'node:sqlite';

export const CURRENT_SCHEMA_VERSION = 3;

const REQUIRED_V2_COLUMNS: Record<string, string[]> = {
  task_workflow: [
    'task_id', 'workflow_version', 'risk_class', 'authorization_ref', 'activation_commit',
    'current_implementation_evidence_id', 'created_at'
  ],
  task_assignments: [
    'id', 'task_id', 'role', 'agent_id', 'status', 'assignment_version', 'assigned_at',
    'started_at', 'completed_at', 'branch', 'worktree', 'lease_start', 'lease_expiry'
  ],
  task_specs: [
    'id', 'task_id', 'spec_version', 'spec_sha', 'status', 'authorization_ref',
    'artifact_path', 'created_at', 'frozen_at', 'superseded_at'
  ],
  implementation_evidence: [
    'id', 'task_id', 'spec_sha', 'base_sha', 'implementation_sha', 'evidence_ref',
    'recorded_by_assignment_id', 'created_at'
  ],
  reviews: [
    'review_id', 'task_id', 'review_type', 'reviewer_assignment_id', 'spec_sha', 'base_sha',
    'implementation_sha', 'attempt', 'verdict', 'findings_ref', 'blocking_findings',
    'evidence_ref', 'artifact_path', 'reviewer', 'model_profile', 'created_at',
    'tracked_files_modified'
  ],
  ci_evidence: [
    'id', 'task_id', 'implementation_sha', 'status', 'reference', 'source', 'recorded_by',
    'created_at'
  ],
  evidence_verifications: [
    'id', 'task_id', 'subject_type', 'subject_key', 'task_spec_id',
    'implementation_evidence_id', 'ci_evidence_id', 'review_id', 'verification_version',
    'supersedes_verification_id', 'decision', 'verification_level', 'recorded_by',
    'verifier_type', 'verifier_id', 'verification_source', 'verification_reference',
    'verified_at', 'created_at', 'metadata_json'
  ]
};

const REQUIRED_V2_OBJECTS = [
  'idx_task_workflow_version_risk', 'idx_task_workflow_candidate',
  'idx_task_assignments_task_role_status', 'idx_task_assignments_implementer_lease',
  'uq_task_assignments_active_role', 'idx_task_specs_task_status', 'idx_task_specs_sha',
  'uq_task_specs_frozen', 'idx_implementation_evidence_task_created',
  'idx_implementation_evidence_spec_impl', 'idx_reviews_task_type_impl_verdict',
  'idx_reviews_spec_impl', 'idx_ci_evidence_task_impl_status', 'idx_ci_evidence_source_ref',
  'idx_evidence_verifications_subject', 'idx_evidence_verifications_level_decision',
  'idx_evidence_verifications_task_spec', 'idx_evidence_verifications_implementation',
  'idx_evidence_verifications_ci', 'idx_evidence_verifications_review',
  'idx_evidence_verifications_verified_at', 'uq_evidence_verifications_supersedes',
  'trg_implementation_evidence_no_update', 'trg_implementation_evidence_no_delete',
  'trg_reviews_no_update', 'trg_reviews_no_delete', 'trg_ci_evidence_no_update',
  'trg_ci_evidence_no_delete', 'trg_evidence_verifications_no_update',
  'trg_evidence_verifications_no_delete', 'trg_evidence_verifications_review_type',
  'trg_evidence_verifications_chain'
] as const;

function createLegacyV1(db: DatabaseSync): void {
  db.exec(
    'CREATE TABLE IF NOT EXISTS tasks (' +
    'id TEXT PRIMARY KEY, title TEXT NOT NULL, priority INTEGER NOT NULL, status TEXT NOT NULL, ' +
    'owner TEXT, branch TEXT, worktree TEXT, lease_start INTEGER, lease_expiry INTEGER, ' +
    'frozen_until INTEGER, blockers TEXT, approval_ref TEXT);' +
    'CREATE TABLE IF NOT EXISTS dependencies (task_id TEXT NOT NULL REFERENCES tasks(id), ' +
    'requires_id TEXT NOT NULL REFERENCES tasks(id), PRIMARY KEY(task_id,requires_id));' +
    'CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY CHECK(id=1), remaining REAL NOT NULL, ' +
    'threshold REAL NOT NULL, source TEXT NOT NULL, cycle TEXT NOT NULL, updated_at INTEGER NOT NULL);' +
    'CREATE TABLE IF NOT EXISTS progress (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL ' +
    'REFERENCES tasks(id), owner TEXT NOT NULL, payload TEXT NOT NULL, created_at INTEGER NOT NULL);' +
    'CREATE TABLE IF NOT EXISTS checkpoints (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL ' +
    'REFERENCES tasks(id), owner TEXT NOT NULL, branch TEXT, last_safe_commit TEXT, ' +
    'completed_work TEXT NOT NULL, tests TEXT NOT NULL, remaining_work TEXT NOT NULL, ' +
    'blockers TEXT NOT NULL, stop_reason TEXT NOT NULL, exact_next_action TEXT NOT NULL, created_at INTEGER NOT NULL)'
  );
}

function createV2(db: DatabaseSync): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS task_assignments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL REFERENCES tasks(id),
      role TEXT NOT NULL CHECK(role IN ('PLANNER','IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER')),
      agent_id TEXT NOT NULL,
      status TEXT NOT NULL CHECK(status IN ('ASSIGNED','ACTIVE','COMPLETED','BLOCKED','SUPERSEDED')),
      assignment_version INTEGER NOT NULL CHECK(assignment_version >= 1),
      assigned_at INTEGER NOT NULL,
      started_at INTEGER,
      completed_at INTEGER,
      branch TEXT,
      worktree TEXT,
      lease_start INTEGER,
      lease_expiry INTEGER,
      UNIQUE(task_id, role, assignment_version),
      UNIQUE(id, task_id),
      CHECK(role = 'IMPLEMENTER' OR
        (branch IS NULL AND worktree IS NULL AND lease_start IS NULL AND lease_expiry IS NULL))
    );
    CREATE INDEX IF NOT EXISTS idx_task_assignments_task_role_status
      ON task_assignments(task_id, role, status);
    CREATE INDEX IF NOT EXISTS idx_task_assignments_implementer_lease
      ON task_assignments(lease_expiry) WHERE role='IMPLEMENTER' AND status='ACTIVE';
    CREATE UNIQUE INDEX IF NOT EXISTS uq_task_assignments_active_role
      ON task_assignments(task_id, role) WHERE status IN ('ASSIGNED','ACTIVE');

    CREATE TABLE IF NOT EXISTS task_specs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL REFERENCES tasks(id),
      spec_version TEXT NOT NULL,
      spec_sha TEXT NOT NULL,
      status TEXT NOT NULL CHECK(status IN ('DRAFT','READY','FROZEN','SUPERSEDED')),
      authorization_ref TEXT NOT NULL,
      artifact_path TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      frozen_at INTEGER,
      superseded_at INTEGER,
      UNIQUE(task_id, spec_version),
      UNIQUE(task_id, spec_sha),
      UNIQUE(id, task_id)
    );
    CREATE INDEX IF NOT EXISTS idx_task_specs_task_status ON task_specs(task_id, status);
    CREATE INDEX IF NOT EXISTS idx_task_specs_sha ON task_specs(spec_sha);
    CREATE UNIQUE INDEX IF NOT EXISTS uq_task_specs_frozen
      ON task_specs(task_id) WHERE status='FROZEN';

    CREATE TABLE IF NOT EXISTS implementation_evidence (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL REFERENCES tasks(id),
      spec_sha TEXT NOT NULL,
      base_sha TEXT NOT NULL,
      implementation_sha TEXT NOT NULL,
      evidence_ref TEXT,
      recorded_by_assignment_id INTEGER,
      created_at INTEGER NOT NULL,
      UNIQUE(task_id, implementation_sha),
      UNIQUE(id, task_id),
      FOREIGN KEY(recorded_by_assignment_id, task_id) REFERENCES task_assignments(id, task_id)
    );
    CREATE INDEX IF NOT EXISTS idx_implementation_evidence_task_created
      ON implementation_evidence(task_id, created_at);
    CREATE INDEX IF NOT EXISTS idx_implementation_evidence_spec_impl
      ON implementation_evidence(spec_sha, implementation_sha);

    CREATE TABLE IF NOT EXISTS task_workflow (
      task_id TEXT PRIMARY KEY REFERENCES tasks(id),
      workflow_version TEXT NOT NULL,
      risk_class TEXT NOT NULL CHECK(risk_class IN ('R0','R1','R2','R3','R4')),
      authorization_ref TEXT NOT NULL,
      activation_commit TEXT NOT NULL,
      current_implementation_evidence_id INTEGER,
      created_at INTEGER NOT NULL,
      FOREIGN KEY(current_implementation_evidence_id) REFERENCES implementation_evidence(id),
      FOREIGN KEY(current_implementation_evidence_id, task_id)
        REFERENCES implementation_evidence(id, task_id)
    );
    CREATE INDEX IF NOT EXISTS idx_task_workflow_version_risk
      ON task_workflow(workflow_version, risk_class);
    CREATE INDEX IF NOT EXISTS idx_task_workflow_candidate
      ON task_workflow(current_implementation_evidence_id);

    CREATE TABLE IF NOT EXISTS reviews (
      review_id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL REFERENCES tasks(id),
      review_type TEXT NOT NULL CHECK(review_type IN ('SECURITY','QUALITY')),
      reviewer_assignment_id INTEGER NOT NULL,
      spec_sha TEXT NOT NULL,
      base_sha TEXT NOT NULL,
      implementation_sha TEXT NOT NULL,
      attempt INTEGER NOT NULL CHECK(attempt >= 1),
      verdict TEXT NOT NULL CHECK(verdict IN ('PASS','REQUEST_CHANGES','BLOCKED')),
      findings_ref TEXT NOT NULL,
      blocking_findings INTEGER NOT NULL DEFAULT 0 CHECK(blocking_findings >= 0),
      evidence_ref TEXT NOT NULL,
      artifact_path TEXT NOT NULL,
      reviewer TEXT NOT NULL,
      model_profile TEXT,
      created_at INTEGER NOT NULL,
      tracked_files_modified INTEGER NOT NULL CHECK(tracked_files_modified IN (0,1)),
      UNIQUE(task_id, review_type, implementation_sha, attempt),
      UNIQUE(review_id, task_id),
      FOREIGN KEY(reviewer_assignment_id, task_id) REFERENCES task_assignments(id, task_id)
    );
    CREATE INDEX IF NOT EXISTS idx_reviews_task_type_impl_verdict
      ON reviews(task_id, review_type, implementation_sha, verdict);
    CREATE INDEX IF NOT EXISTS idx_reviews_spec_impl ON reviews(spec_sha, implementation_sha);

    CREATE TABLE IF NOT EXISTS ci_evidence (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL REFERENCES tasks(id),
      implementation_sha TEXT NOT NULL,
      status TEXT NOT NULL CHECK(status IN ('PENDING','SUCCESS','FAILURE','CANCELLED','UNKNOWN')),
      reference TEXT NOT NULL,
      source TEXT NOT NULL,
      recorded_by TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      UNIQUE(task_id, reference),
      UNIQUE(id, task_id)
    );
    CREATE INDEX IF NOT EXISTS idx_ci_evidence_task_impl_status
      ON ci_evidence(task_id, implementation_sha, status);
    CREATE INDEX IF NOT EXISTS idx_ci_evidence_source_ref ON ci_evidence(source, reference);

    CREATE TABLE IF NOT EXISTS evidence_verifications (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL REFERENCES tasks(id),
      subject_type TEXT NOT NULL CHECK(subject_type IN (
        'HUMAN_AUTHORIZATION','SPECIFICATION','IMPLEMENTATION','CI','SECURITY_REVIEW',
        'QUALITY_REVIEW','PR_BRANCH_STATE','MERGE_RESULT'
      )),
      subject_key TEXT NOT NULL CHECK(length(subject_key) > 0),
      task_spec_id INTEGER,
      implementation_evidence_id INTEGER,
      ci_evidence_id INTEGER,
      review_id INTEGER,
      verification_version INTEGER NOT NULL CHECK(verification_version >= 1),
      supersedes_verification_id INTEGER REFERENCES evidence_verifications(id),
      decision TEXT NOT NULL CHECK(decision IN ('ATTEST','REVOKE')),
      verification_level TEXT NOT NULL CHECK(verification_level IN ('UNVERIFIED','RECORDED','VERIFIED')),
      recorded_by TEXT NOT NULL,
      verifier_type TEXT,
      verifier_id TEXT,
      verification_source TEXT,
      verification_reference TEXT,
      verified_at INTEGER,
      created_at INTEGER NOT NULL,
      metadata_json TEXT,
      UNIQUE(task_id, subject_type, subject_key, verification_version),
      UNIQUE(id, task_id, subject_type, subject_key),
      CHECK(decision <> 'REVOKE' OR verification_level = 'UNVERIFIED'),
      CHECK(verification_level <> 'VERIFIED' OR (
        decision = 'ATTEST' AND verifier_type IS NOT NULL AND length(verifier_type) > 0 AND
        verifier_id IS NOT NULL AND length(verifier_id) > 0 AND
        verification_source IS NOT NULL AND length(verification_source) > 0 AND
        verification_reference IS NOT NULL AND length(verification_reference) > 0 AND
        verified_at IS NOT NULL
      )),
      CHECK(
        (subject_type='SPECIFICATION' AND task_spec_id IS NOT NULL AND
          subject_key=CAST(task_spec_id AS TEXT) AND implementation_evidence_id IS NULL AND
          ci_evidence_id IS NULL AND review_id IS NULL) OR
        (subject_type='IMPLEMENTATION' AND implementation_evidence_id IS NOT NULL AND
          subject_key=CAST(implementation_evidence_id AS TEXT) AND task_spec_id IS NULL AND
          ci_evidence_id IS NULL AND review_id IS NULL) OR
        (subject_type='CI' AND ci_evidence_id IS NOT NULL AND
          subject_key=CAST(ci_evidence_id AS TEXT) AND task_spec_id IS NULL AND
          implementation_evidence_id IS NULL AND review_id IS NULL) OR
        (subject_type IN ('SECURITY_REVIEW','QUALITY_REVIEW') AND review_id IS NOT NULL AND
          subject_key=CAST(review_id AS TEXT) AND task_spec_id IS NULL AND
          implementation_evidence_id IS NULL AND ci_evidence_id IS NULL) OR
        (subject_type IN ('HUMAN_AUTHORIZATION','PR_BRANCH_STATE','MERGE_RESULT') AND
          task_spec_id IS NULL AND implementation_evidence_id IS NULL AND
          ci_evidence_id IS NULL AND review_id IS NULL)
      ),
      FOREIGN KEY(task_spec_id, task_id) REFERENCES task_specs(id, task_id),
      FOREIGN KEY(implementation_evidence_id, task_id) REFERENCES implementation_evidence(id, task_id),
      FOREIGN KEY(ci_evidence_id, task_id) REFERENCES ci_evidence(id, task_id),
      FOREIGN KEY(review_id, task_id) REFERENCES reviews(review_id, task_id),
      FOREIGN KEY(supersedes_verification_id, task_id, subject_type, subject_key)
        REFERENCES evidence_verifications(id, task_id, subject_type, subject_key)
    );
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_subject
      ON evidence_verifications(task_id, subject_type, subject_key, verification_version);
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_level_decision
      ON evidence_verifications(task_id, verification_level, decision);
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_task_spec ON evidence_verifications(task_spec_id);
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_implementation ON evidence_verifications(implementation_evidence_id);
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_ci ON evidence_verifications(ci_evidence_id);
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_review ON evidence_verifications(review_id);
    CREATE INDEX IF NOT EXISTS idx_evidence_verifications_verified_at ON evidence_verifications(verified_at);
    CREATE UNIQUE INDEX IF NOT EXISTS uq_evidence_verifications_supersedes
      ON evidence_verifications(supersedes_verification_id) WHERE supersedes_verification_id IS NOT NULL;

    CREATE TRIGGER IF NOT EXISTS trg_implementation_evidence_no_update
      BEFORE UPDATE ON implementation_evidence BEGIN SELECT RAISE(ABORT, 'implementation_evidence is append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_implementation_evidence_no_delete
      BEFORE DELETE ON implementation_evidence BEGIN SELECT RAISE(ABORT, 'implementation_evidence is append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_reviews_no_update
      BEFORE UPDATE ON reviews BEGIN SELECT RAISE(ABORT, 'reviews are append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_reviews_no_delete
      BEFORE DELETE ON reviews BEGIN SELECT RAISE(ABORT, 'reviews are append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_ci_evidence_no_update
      BEFORE UPDATE ON ci_evidence BEGIN SELECT RAISE(ABORT, 'ci_evidence is append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_ci_evidence_no_delete
      BEFORE DELETE ON ci_evidence BEGIN SELECT RAISE(ABORT, 'ci_evidence is append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_evidence_verifications_no_update
      BEFORE UPDATE ON evidence_verifications BEGIN SELECT RAISE(ABORT, 'evidence_verifications is append-only'); END;
    CREATE TRIGGER IF NOT EXISTS trg_evidence_verifications_no_delete
      BEFORE DELETE ON evidence_verifications BEGIN SELECT RAISE(ABORT, 'evidence_verifications is append-only'); END;

    CREATE TRIGGER IF NOT EXISTS trg_evidence_verifications_review_type
      BEFORE INSERT ON evidence_verifications
      WHEN NEW.review_id IS NOT NULL
      BEGIN
        SELECT CASE
          WHEN NEW.subject_type='SECURITY_REVIEW' AND NOT EXISTS (
            SELECT 1 FROM reviews WHERE review_id=NEW.review_id AND task_id=NEW.task_id AND review_type='SECURITY'
          ) THEN RAISE(ABORT, 'SECURITY_REVIEW subject must reference a SECURITY review')
          WHEN NEW.subject_type='QUALITY_REVIEW' AND NOT EXISTS (
            SELECT 1 FROM reviews WHERE review_id=NEW.review_id AND task_id=NEW.task_id AND review_type='QUALITY'
          ) THEN RAISE(ABORT, 'QUALITY_REVIEW subject must reference a QUALITY review')
        END;
      END;

    CREATE TRIGGER IF NOT EXISTS trg_evidence_verifications_chain
      BEFORE INSERT ON evidence_verifications
      BEGIN
        SELECT CASE
          WHEN NEW.verification_version=1 AND NEW.supersedes_verification_id IS NOT NULL
            THEN RAISE(ABORT, 'verification version 1 cannot supersede another row')
          WHEN NEW.verification_version>1 AND NEW.supersedes_verification_id IS NULL
            THEN RAISE(ABORT, 'verification version >1 must supersede the previous version')
          WHEN NEW.verification_version>1 AND NOT EXISTS (
            SELECT 1 FROM evidence_verifications prior
            WHERE prior.id=NEW.supersedes_verification_id
              AND prior.task_id=NEW.task_id
              AND prior.subject_type=NEW.subject_type
              AND prior.subject_key=NEW.subject_key
              AND prior.verification_version=NEW.verification_version-1
          ) THEN RAISE(ABORT, 'verification supersession must reference previous version of same subject')
        END;
      END;
  `);
}

function validateV2(db: DatabaseSync): void {
  for (const [table, required] of Object.entries(REQUIRED_V2_COLUMNS)) {
    const columns = new Set((db.prepare(`PRAGMA table_info(${table})`).all() as Array<{ name: string }>).map(row => row.name));
    if (columns.size === 0 || required.some(column => !columns.has(column))) {
      throw new Error(`Schema version 2 is incompatible: ${table} columns do not match the required contract`);
    }
  }
  const objects = new Set((db.prepare(
    "SELECT name FROM sqlite_master WHERE type IN ('index','trigger') AND name IS NOT NULL"
  ).all() as Array<{ name: string }>).map(row => row.name));
  for (const name of REQUIRED_V2_OBJECTS) {
    if (!objects.has(name)) throw new Error(`Schema version 2 is incompatible: missing ${name}`);
  }
}

export function migrateDatabase(db: DatabaseSync): void {
  db.exec('BEGIN IMMEDIATE');
  try {
    createLegacyV1(db);
    db.exec(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        applied_at INTEGER NOT NULL
      )
    `);
    const future = db.prepare('SELECT MAX(version) AS version FROM schema_migrations').get() as { version: number | null };
    if (future.version !== null && future.version > CURRENT_SCHEMA_VERSION) {
      throw new Error(`Database schema version ${future.version} is newer than supported version ${CURRENT_SCHEMA_VERSION}`);
    }
    const v2 = db.prepare('SELECT 1 AS present FROM schema_migrations WHERE version=2').get() as { present: number } | undefined;
    if (v2) {
      validateV2(db);
    } else {
      db.prepare('INSERT OR IGNORE INTO schema_migrations(version,description,applied_at) VALUES (1,?,?)')
        .run('Legacy Workflow V1 schema baseline', Date.now());
      createV2(db);
      validateV2(db);
      db.prepare('INSERT INTO schema_migrations(version,description,applied_at) VALUES (2,?,?)')
        .run('Workflow V2 data foundation; workflow activation remains disabled', Date.now());
    }
    // §17.5 permits durable in-progress attempts separate from immutable verdicts.
    // §18 permits additive role metadata without rewriting legacy checkpoints.
    const v3 = db.prepare('SELECT 1 FROM schema_migrations WHERE version=3').get();
    if (!v3) {
      db.exec(`
        CREATE TABLE IF NOT EXISTS review_attempts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          task_id TEXT NOT NULL REFERENCES tasks(id),
          review_type TEXT NOT NULL CHECK(review_type IN ('SECURITY','QUALITY')),
          assignment_id INTEGER NOT NULL,
          implementation_evidence_id INTEGER NOT NULL,
          spec_sha TEXT NOT NULL, base_sha TEXT NOT NULL, implementation_sha TEXT NOT NULL,
          attempt INTEGER NOT NULL CHECK(attempt>=1),
          started_at INTEGER NOT NULL,
          submitted_review_id INTEGER REFERENCES reviews(review_id),
          UNIQUE(task_id,review_type,implementation_sha,attempt),
          FOREIGN KEY(assignment_id,task_id) REFERENCES task_assignments(id,task_id),
          FOREIGN KEY(implementation_evidence_id,task_id) REFERENCES implementation_evidence(id,task_id)
        );
        CREATE INDEX IF NOT EXISTS idx_review_attempts_target ON review_attempts(task_id,review_type,implementation_sha);
        CREATE TABLE IF NOT EXISTS checkpoint_assignments (
          checkpoint_id INTEGER PRIMARY KEY REFERENCES checkpoints(id),
          task_id TEXT NOT NULL REFERENCES tasks(id),
          role TEXT NOT NULL CHECK(role IN ('PLANNER','IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER')),
          assignment_id INTEGER NOT NULL,
          FOREIGN KEY(assignment_id,task_id) REFERENCES task_assignments(id,task_id)
        );
      `);
      db.prepare('INSERT INTO schema_migrations VALUES (3,?,?)')
        .run('B2 durable review attempts and additive checkpoint role metadata; no activation', Date.now());
    }
    for (const [table, fields] of Object.entries({
      review_attempts: ['id','task_id','review_type','assignment_id','implementation_evidence_id','spec_sha','base_sha','implementation_sha','attempt','started_at','submitted_review_id'],
      checkpoint_assignments: ['checkpoint_id','task_id','role','assignment_id']
    })) {
      const columns = new Set((db.prepare(`PRAGMA table_info(${table})`).all() as Array<{name:string}>).map(r=>r.name));
      if (fields.some(field=>!columns.has(field))) throw new Error('Schema version 3 is incompatible: '+table);
    }
    if (!db.prepare("SELECT 1 FROM sqlite_master WHERE type='index' AND name='idx_review_attempts_target'").get())
      throw new Error('Schema version 3 is incompatible: missing review attempt index');
    db.exec('COMMIT');
  } catch (error) {
    db.exec('ROLLBACK');
    throw error;
  }
}
