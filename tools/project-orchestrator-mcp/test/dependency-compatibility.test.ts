import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtempSync, rmSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { ReadBuffer, STDIO_DEFAULT_MAX_BUFFER_SIZE } from '@modelcontextprotocol/sdk/shared/stdio.js';
import { z } from 'zod';
import { assignmentSchema, mergePolicySchema } from '../src/v2-contracts.js';

// Small, bounded upstream regression probes. These schemas are test-only and do
// not add collection limits to any project tool. Uncapped inputs stay unchanged.
for (const kind of ['array', 'set', 'map'] as const) {
  test(`patched Zod rejects an oversized bounded ${kind} before parsing its elements`, () => {
    let parsed = 0;
    const item = z.string().transform(value => { parsed++; return value; });
    const schema = kind === 'array' ? z.array(item).max(2)
      : kind === 'set' ? z.set(item).max(2)
      : z.map(z.string(), item).max(2);
    const input = (values: string[]) => kind === 'array' ? values
      : kind === 'set' ? new Set(values)
      : new Map(values.map(value => [value, value]));
    const rejected = schema.safeParse(input(['a', 'b', 'c']));
    assert.equal(rejected.success, false);
    assert.equal(parsed, 0, 'oversize rejection must precede element work');
    assert.equal(schema.safeParse(input(['a', 'b'])).success, true);
    assert.equal(parsed, 2);
  });
}

test('SDK stdio retains its existing 10 MiB default, overflow refusal and framing recovery', () => {
  assert.equal(STDIO_DEFAULT_MAX_BUFFER_SIZE, 10 * 1024 * 1024);
  const buffer = new ReadBuffer();
  buffer.append(Buffer.alloc(STDIO_DEFAULT_MAX_BUFFER_SIZE, 0x20));
  assert.throws(() => buffer.append(Buffer.from(' ')), /exceeded maximum size/);
  assert.equal(buffer.readMessage(), null, 'overflow clears the unparsed frame');
  buffer.append(Buffer.from('{"jsonrpc":"2.0","id":1,"method":"ping"}\n'));
  assert.deepEqual(buffer.readMessage(), { jsonrpc: '2.0', id: 1, method: 'ping' });
  assert.equal(buffer.readMessage(), null);
});

test('Zod keeps existing role defaults, nullable assignments, strict policy and uniqueness checks', () => {
  const base = { task_id: 'SYNTH-COMPAT', actor_id: 'synthetic-admin', actor_type: 'ADMIN',
    role: 'IMPLEMENTER', agent_id: 'synthetic-agent', authorization_ref: 'synthetic:scope' };
  const result = assignmentSchema.parse(base);
  assert.equal(result.status, 'ACTIVE');
  assert.equal(result.expected_assignment_id, null);
  assert.equal(assignmentSchema.safeParse({ ...base, role: 'SUPERUSER' }).success, false);
  const policy = { required_human_exception_refs: ['synthetic:one'], stop_conditions: [],
    scope_violation: false, secret_or_confidential_exposure: false,
    repository: 'NSHAOKIET/AI-IP-DESCRIPTION-GENERATOR' };
  assert.equal(mergePolicySchema.parse(policy).repository, 'nshaokiet/ai-ip-description-generator');
  assert.equal(mergePolicySchema.safeParse({ ...policy, approve: true }).success, false);
  assert.equal(mergePolicySchema.safeParse({ ...policy,
    required_human_exception_refs: ['synthetic:one', 'synthetic:one'] }).success, false);
});

function canonical(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonical);
  if (value !== null && typeof value === 'object') {
    const object = value as Record<string, unknown>;
    return Object.fromEntries(Object.keys(object).sort().map(key => [key, canonical(object[key])]));
  }
  return value;
}

test('real stdio preserves all 25 tool schemas and does not introduce proposed input caps',
  { timeout: 30_000 }, async () => {
    const dir = mkdtempSync(join(tmpdir(), 'mcp-dependency-compat-'));
    const server = join(dirname(fileURLToPath(import.meta.url)), '../src/server.js');
    const env = Object.fromEntries(Object.entries(process.env)
      .filter(([key, value]) => key !== 'OPENAI_API_KEY' && value !== undefined)) as Record<string, string>;
    env.PROJECT_ORCH_DB = join(dir, 'state.sqlite');
    const client = new Client({ name: 'dependency-compatibility', version: '1.0.0' });
    const transport = new StdioClientTransport({ command: process.execPath, args: [server], env, stderr: 'pipe' });
    try {
      await client.connect(transport);
      const tools = (await client.listTools()).tools
        .map(({ name, inputSchema, outputSchema }) => ({ name, inputSchema,
          ...(outputSchema === undefined ? {} : { outputSchema }) }))
        .sort((a, b) => a.name.localeCompare(b.name));
      assert.equal(tools.length, 25);
      // Independently captured from accepted main 2f5366d2056f43442bb97f566c26065f93d1f569
      // using its SDK 1.30.0 / Zod 4.6.0 and an isolated empty test database.
      assert.equal(createHash('sha256').update(JSON.stringify(canonical(tools))).digest('hex'),
        'e39609a577837a150a6e57f6320aa194ae8aeabd6d5fe2274efc74f3289d9ef0');
      for (const args of [
        { milestone: 'synthetic', tests: Array<string>(10_001).fill('synthetic') },
        { milestone: 's'.repeat(1024 * 1024 + 1), tests: [] as string[] },
      ]) {
        const result = await client.callTool({ name: 'project.report_progress', arguments: {
          task_id: 'SYNTH-NOT-REGISTERED', owner: 'synthetic-owner', ...args,
          files_changed: [], commit_sha: null, remaining_work: 'none', blockers: [],
        } });
        assert.equal(result.isError, true);
        // Schema/transport accept these historically permitted sizes; the
        // unchanged store refuses unknown task authority. No task is created.
        assert.match(JSON.stringify(result.content), /Unknown task: SYNTH-NOT-REGISTERED/);
      }
      const denied = await client.callTool({ name: 'project.assign_role', arguments: {
        task_id: 'SYNTH-NOT-REGISTERED', actor_type: 'IMPLEMENTER', actor_id: 'synthetic',
        role: 'IMPLEMENTER', agent_id: 'synthetic', authorization_ref: 'synthetic:scope',
      } });
      assert.equal(denied.isError, true);
    } finally {
      await client.close();
      assert.equal(dirname(resolve(dir)), resolve(tmpdir()));
      assert.match(basename(dir), /^mcp-dependency-compat-/);
      rmSync(dir, { recursive: true, force: true });
    }
  });
