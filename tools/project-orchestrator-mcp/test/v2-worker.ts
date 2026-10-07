import { Store } from '../src/store.js';
const [file,operation,payload]=process.argv.slice(2);
const store=new Store(file!);
try {
  const p=JSON.parse(payload!);
  const result=operation==='candidate'?store.v2.recordImplementation(p):operation==='assignment'?store.v2.assignRole(p):store.v2.recordVerification(p);
  process.stdout.write(JSON.stringify({ok:true,result}));
} catch(error) { process.stdout.write(JSON.stringify({ok:false,error:error instanceof Error?error.message:String(error)})); }
finally { store.close(); }
