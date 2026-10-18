import { Store, STATES, type Status } from './store.js';
import { readFileSync } from 'node:fs';
import { enrollSchema,verificationSchema } from './v2-contracts.js';
import { RegistrationError, readRegistrationManifest } from './registration.js';

// Local Human operator CLI. This is deliberately absent from the MCP tool list.
const args = process.argv.slice(2);
const [action, id, value, evidence] = args;
let store: Store | undefined;
try {
  if (action === 'register-task') {
    if (args.length !== 2 || !id) throw new RegistrationError('REGISTRATION_INVALID_MANIFEST');
    const manifest = readRegistrationManifest(id);
    store = new Store();
    process.stdout.write(JSON.stringify(store.registerTask(manifest))+'\n');
  } else if (action === 'enroll-v2' && id) {
    store = new Store();
    process.stdout.write(JSON.stringify(store.v2.enroll(enrollSchema.parse(JSON.parse(readFileSync(id,'utf8')))))+'\n');
  } else if (action === 'record-verification' && id) {
    store = new Store();
    process.stdout.write(JSON.stringify(store.v2.recordVerification(verificationSchema.parse(JSON.parse(readFileSync(id,'utf8')))))+'\n');
  } else if (action === 'approve' && id && value) {
    store = new Store();
    process.stdout.write(JSON.stringify(store.approveTask(id, value)) + '\n');
  } else if (action === 'transition' && id && value && evidence && STATES.includes(value as Status)) {
    store = new Store();
    process.stdout.write(JSON.stringify(store.transition(id, value as Status, evidence)) + '\n');
  } else {
    throw new Error('Usage: admin register-task ABSOLUTE_JSON_FILE | admin approve TASK_ID HUMAN_DECISION_REF | admin transition TASK_ID STATE EVIDENCE_REF | admin enroll-v2 JSON_FILE | admin record-verification JSON_FILE');
  }
} catch (error) {
  const registerError = error instanceof RegistrationError ? error.code :
    error instanceof Error && /SQLITE_BUSY|database is locked/i.test(error.message) ? 'REGISTRATION_DB_BUSY' :
    'REGISTRATION_DB_ERROR';
  process.stderr.write((action === 'register-task' ?
    registerError :
    (error instanceof Error ? error.message : String(error))) + '\n');
  process.exitCode = 1;
} finally {
  store?.close();
}
