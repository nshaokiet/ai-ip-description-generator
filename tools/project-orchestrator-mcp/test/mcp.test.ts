import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

test('real stdio MCP launches offline with no API key and exposes 13 tools', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'orchestrator-mcp-'));
  const server = join(dirname(fileURLToPath(import.meta.url)), '../src/server.js');
  const env = Object.fromEntries(
    Object.entries(process.env).filter(([key,value]) => key !== 'OPENAI_API_KEY' && value !== undefined)
  ) as Record<string,string>;
  env.PROJECT_ORCH_DB = join(dir,'state.sqlite');
  const transport = new StdioClientTransport({ command: process.execPath, args: [server], env, stderr: 'pipe' });
  const client = new Client({ name: 'offline-test-client', version: '0.1.0' });
  try {
    await client.connect(transport);
    const names = (await client.listTools()).tools.map(tool => tool.name);
    assert.equal(names.length,13);
    assert.equal(names.includes('project.claim_task'),true);
    assert.equal(names.some(name => /merge|reset|activate/.test(name)),false);
    const result = await client.callTool({ name: 'budget.should_continue', arguments: {} });
    assert.equal(result.isError,undefined);
    assert.equal((result.structuredContent as { result: { decision: string } }).result.decision,'CONTINUE');
  } finally {
    await client.close();
    rmSync(dir,{ recursive: true, force: true });
  }
});
