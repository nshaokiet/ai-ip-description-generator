import { Store } from '../src/store.js';
import { setTimeout } from 'node:timers/promises';

const file = process.argv[2];
if (!file) throw new Error('database path required');

// Two workers may race while SQLite switches a legacy database to WAL mode.
// Retry only that transient lock; any other startup or migration failure must
// remain visible to the concurrency regression test.
for (let attempt = 1; attempt <= 5; attempt++) {
  try {
    const store = new Store(file);
    store.close();
    process.stdout.write('READY');
    break;
  } catch (error) {
    const sqliteError = error as Error & { errcode?: number };
    if (sqliteError.errcode !== 5 || attempt === 5) throw error;
    await setTimeout(attempt * 100);
  }
}
