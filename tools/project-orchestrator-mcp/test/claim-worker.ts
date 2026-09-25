import { Store } from '../src/store.js';
const [file, owner] = process.argv.slice(2);
if (!file || !owner) process.exit(2);
const store = new Store(file);
try {
  store.claim('TEST-RACE', owner, 'task/' + owner, '/tmp/' + owner);
  process.stdout.write('CLAIMED');
} catch {
  process.stdout.write('REJECTED');
} finally {
  store.close();
}
