import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { Store } from './store.js';

const store = new Store();
const server = new McpServer({ name: 'project-orchestrator', version: '0.1.0' });
const reply = (value: unknown) => ({
  content: [{ type: 'text' as const, text: JSON.stringify(value) }],
  structuredContent: { result: value }
});
function safe<T>(fn: () => T) {
  try { return reply(fn()); }
  catch (error) {
    return { content: [{ type: 'text' as const, text: error instanceof Error ? error.message : String(error) }], isError: true };
  }
}
const taskId = z.string().min(3).max(50);
const owner = z.string().min(1).max(120);
const nonempty = z.string().min(1);
const sha = z.string().regex(/^[a-f0-9]{40}$/i);
const handoff = {
  task_id: taskId, owner, last_safe_commit: sha.nullable(),
  completed_work: nonempty, tests: z.array(z.string()),
  remaining_work: nonempty, blockers: z.array(z.string()),
  stop_reason: nonempty, exact_next_action: nonempty
};

server.registerTool('project.get_state', {
  description: 'Read active task(s), ownership, worktree, blockers, checkpoint, next action, and quota',
  inputSchema: { task_id: taskId.optional() }
}, ({ task_id }) => safe(() => store.getState(task_id)));

server.registerTool('project.next_task', {
  description: 'Read highest-priority approved, unfrozen, unblocked task with completed dependencies and sufficient budget',
  inputSchema: {}
}, () => safe(() => store.nextTask()));

server.registerTool('project.claim_task', {
  description: 'Atomically lease an approved task to one agent and distinct non-main branch/worktree',
  inputSchema: {
    task_id: taskId, owner, branch: nonempty, worktree: nonempty,
    lease_minutes: z.number().int().min(1).max(1440).optional()
  }
}, ({ task_id, owner, branch, worktree, lease_minutes }) =>
  safe(() => store.claim(task_id, owner, branch, worktree, lease_minutes)));

server.registerTool('project.renew_lease', {
  description: 'Renew a task lease for the same owner before it expires',
  inputSchema: { task_id: taskId, owner, lease_minutes: z.number().int().min(1).max(1440).optional() }
}, ({ task_id, owner, lease_minutes }) => safe(() => store.renew(task_id, owner, lease_minutes)));

server.registerTool('project.release_task', {
  description: 'Release an active task lease to the approved queue',
  inputSchema: { task_id: taskId, owner }
}, ({ task_id, owner }) => safe(() => store.release(task_id, owner)));

server.registerTool('project.report_progress', {
  description: 'Persist task milestone, offline test evidence, changed paths, last safe commit, remaining work, and blockers',
  inputSchema: {
    task_id: taskId, owner, milestone: nonempty, tests: z.array(z.string()),
    files_changed: z.array(z.string()), commit_sha: sha.nullable(),
    remaining_work: nonempty, blockers: z.array(z.string())
  }
}, ({ task_id, owner, ...progress }) => safe(() => store.report(task_id, owner, progress)));

server.registerTool('project.finish_task', {
  description: 'Mark implementation IMPLEMENTED with test and commit evidence; review, approval, merge and completion remain separate',
  inputSchema: { task_id: taskId, owner, tests: z.array(z.string()).min(1), commit_sha: sha }
}, ({ task_id, owner, tests, commit_sha }) =>
  safe(() => store.finish(task_id, owner, tests, commit_sha)));

server.registerTool('budget.get', {
  description: 'Read manually recorded remaining percentage, threshold, cycle, and decision',
  inputSchema: {}
}, () => safe(() => store.budget()));

server.registerTool('budget.set_remaining', {
  description: 'Human manually records remaining Codex percentage; optionally names a separate quota cycle',
  inputSchema: { remaining: z.number().finite().min(0).max(100), cycle: z.string().min(1).max(120).optional() }
}, ({ remaining, cycle }) => safe(() => store.setBudget(remaining, cycle)));

server.registerTool('budget.should_continue', {
  description: 'CONTINUE only if remaining > threshold; otherwise STOP_AND_CHECKPOINT',
  inputSchema: {}
}, () => safe(() => store.budget()));

server.registerTool('checkpoint.create', {
  description: 'Persist an explicit safe checkpoint even when quota guard has stopped work',
  inputSchema: handoff
}, ({ task_id, owner, ...data }) => safe(() => store.checkpoint(task_id, owner, data)));

server.registerTool('checkpoint.get_latest', {
  description: 'Read last persisted checkpoint across client or server restarts',
  inputSchema: { task_id: taskId.optional() }
}, ({ task_id }) => safe(() => store.latestCheckpoint(task_id)));

server.registerTool('project.stop_and_handoff', {
  description: 'Atomically record complete handoff and block task pending Human review; works at quota threshold',
  inputSchema: handoff
}, ({ task_id, owner, ...data }) => safe(() => store.stopAndHandoff(task_id, owner, data)));

await server.connect(new StdioServerTransport());
process.on('SIGINT', () => { store.close(); process.exit(0); });
process.on('SIGTERM', () => { store.close(); process.exit(0); });
