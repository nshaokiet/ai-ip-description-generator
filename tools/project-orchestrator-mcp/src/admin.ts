import { Store, STATES, type Status } from './store.js';
import { readFileSync } from 'node:fs';
import { enrollSchema,verificationSchema } from './v2-contracts.js';

// Local Human operator CLI. This is deliberately absent from the MCP tool list.
const [action, id, value, evidence] = process.argv.slice(2);
const store = new Store();
try {
  if (action === 'enroll-v2' && id) {
    process.stdout.write(JSON.stringify(store.v2.enroll(enrollSchema.parse(JSON.parse(readFileSync(id,'utf8')))))+'\n');
  } else if (action === 'record-verification' && id) {
    process.stdout.write(JSON.stringify(store.v2.recordVerification(verificationSchema.parse(JSON.parse(readFileSync(id,'utf8')))))+'\n');
  } else if (action === 'approve' && id && value) {
    process.stdout.write(JSON.stringify(store.approveTask(id, value)) + '\n');
  } else if (action === 'transition' && id && value && evidence && STATES.includes(value as Status)) {
    process.stdout.write(JSON.stringify(store.transition(id, value as Status, evidence)) + '\n');
  } else {
    throw new Error('Usage: admin approve TASK_ID HUMAN_DECISION_REF | admin transition TASK_ID STATE EVIDENCE_REF | admin enroll-v2 JSON_FILE | admin record-verification JSON_FILE');
  }
} catch (error) {
  process.stderr.write((error instanceof Error ? error.message : String(error)) + '\n');
  process.exitCode = 1;
} finally {
  store.close();
}
