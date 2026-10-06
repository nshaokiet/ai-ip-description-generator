import { Store } from '../src/store.js';

const file = process.argv[2];
if (!file) throw new Error('database path required');

const store = new Store(file);
store.close();
process.stdout.write('READY');
