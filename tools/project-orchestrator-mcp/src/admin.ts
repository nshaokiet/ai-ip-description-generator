import { Store, STATES, type Status } from './store.js';

// Local Human operator CLI. This is deliberately absent from the MCP tool list.
const [action, id, value, evidence] = process.argv.slice(2);
const store = new Store();
try {
  if (action === 'approve' && id && value) {
    process.stdout.write(JSON.stringify(store.approveTask(id, value)) + '\n');
  } else if (action === 'transition' && id && value && evidence && STATES.includes(value as Status)) {
    process.stdout.write(JSON.stringify(store.transition(id, value as Status, evidence)) + '\n');
  } else {
    throw new Error('Usage: admin approve TASK_ID HUMAN_DECISION_REF | admin transition TASK_ID STATE EVIDENCE_REF');
  }
} catch (error) {
  process.stderr.write((error instanceof Error ? error.message : String(error)) + '\n');
  process.exitCode = 1;
} finally {
  store.close();
}
