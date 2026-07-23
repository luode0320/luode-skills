import assert from "node:assert/strict";
import test from "node:test";
import { resolve } from "node:path";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import {
  RESULT_CODES,
  createRenameServer,
  executeRenameCurrentThread,
  extractThreadId,
} from "../index.mjs";
import { APP_SERVER_CODES, AppServerError } from "../app-server-client.mjs";

const THREAD_ID = "019f8a9d-8618-7602-bdfa-e526f25d83aa";
const OTHER_THREAD_ID = "019f8a89-cdf3-78a1-b8ac-23cc05bd51f0";

/**
 * 构造 Codex App 宿主一致的测试元数据。
 * [参数] threadId：当前测试任务 ID。
 * [返回] 同时包含直接字段和 turn metadata 的 `_meta` 对象。
 * 最近修改时间：2026-07-23 01:45:52，固定可信元数据测试样本。
 */
function metadata(threadId = THREAD_ID) {
  return {
    threadId,
    "x-codex-turn-metadata": {
      thread_id: threadId,
    },
  };
}

test("从直接字段或 Codex turn metadata 解析当前 threadId", () => {
  assert.equal(extractThreadId({ threadId: THREAD_ID }), THREAD_ID);
  assert.equal(extractThreadId({
    "x-codex-turn-metadata": { thread_id: THREAD_ID },
  }), THREAD_ID);
  assert.equal(extractThreadId(metadata()), THREAD_ID);
});

test("缺失、格式错误或冲突的 threadId 均拒绝猜测", () => {
  assert.equal(extractThreadId(undefined), null);
  assert.equal(extractThreadId({ threadId: "not-a-thread" }), null);
  assert.equal(extractThreadId({
    cwd: THREAD_ID,
    preview: THREAD_ID,
    arguments: { threadId: THREAD_ID },
  }), null);
  assert.equal(extractThreadId({
    "x-codex-turn-metadata": { threadId: THREAD_ID },
  }), null);
  assert.equal(extractThreadId({
    threadId: THREAD_ID,
    "x-codex-turn-metadata": { thread_id: OTHER_THREAD_ID },
  }), null);
});

test("标题校验使用稳定错误码，并在成功时仅传递当前 threadId", async () => {
  assert.deepEqual(
    await executeRenameCurrentThread({ title: "   ", meta: metadata() }),
    { ok: false, code: RESULT_CODES.INVALID_TITLE },
  );
  assert.deepEqual(
    await executeRenameCurrentThread({ title: "a".repeat(25), meta: metadata() }),
    { ok: false, code: RESULT_CODES.INVALID_TITLE },
  );
  assert.deepEqual(
    await executeRenameCurrentThread({ title: "标题", meta: {} }),
    { ok: false, code: RESULT_CODES.THREAD_CONTEXT_MISSING },
  );

  let received;
  const success = await executeRenameCurrentThread({
    title: "  模型无关会话重命名  ",
    meta: metadata(),
    renameThread: async (input) => {
      received = input;
    },
  });

  assert.equal(received.threadId, THREAD_ID);
  assert.equal(received.name, "模型无关会话重命名");
  assert.deepEqual(success, {
    ok: true,
    code: RESULT_CODES.RENAMED,
    title: "模型无关会话重命名",
  });
});

test("App Server 异常映射为公开稳定错误码", async () => {
  for (const code of Object.values(APP_SERVER_CODES)) {
    const value = await executeRenameCurrentThread({
      title: "标题",
      meta: metadata(),
      renameThread: async () => {
        throw new AppServerError(code);
      },
    });
    assert.deepEqual(value, { ok: false, code });
  }
});

test("MCP 只公开 rename_current_thread，输入 schema 仅包含 title", async () => {
  const server = createRenameServer({ renameThread: async () => undefined });
  const client = new Client({ name: "test-client", version: "1.0.0" });
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();

  await Promise.all([
    server.connect(serverTransport),
    client.connect(clientTransport),
  ]);

  try {
    const tools = await client.listTools();
    assert.equal(tools.tools.length, 1);
    assert.equal(tools.tools[0].name, "rename_current_thread");
    assert.deepEqual(Object.keys(tools.tools[0].inputSchema.properties), ["title"]);
    assert.deepEqual(tools.tools[0].inputSchema.required, ["title"]);
    assert.equal(tools.tools[0].inputSchema.additionalProperties, false);

    const response = await client.callTool({
      name: "rename_current_thread",
      arguments: { title: "模型无关会话重命名" },
      _meta: metadata(),
    });
    assert.equal(response.isError, false);
    assert.deepEqual(response.structuredContent, {
      ok: true,
      code: RESULT_CODES.RENAMED,
      title: "模型无关会话重命名",
    });

    const extraInput = await client.callTool({
      name: "rename_current_thread",
      arguments: { title: "标题", threadId: OTHER_THREAD_ID },
      _meta: metadata(),
    });
    assert.equal(extraInput.isError, true);
    assert.match(extraInput.content[0].text, /Input validation error/);
  } finally {
    await client.close();
    await server.close();
  }
});

test("MCP 缺失请求元数据时返回 THREAD_CONTEXT_MISSING", async () => {
  const server = createRenameServer({ renameThread: async () => undefined });
  const client = new Client({ name: "test-client", version: "1.0.0" });
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();

  await Promise.all([
    server.connect(serverTransport),
    client.connect(clientTransport),
  ]);

  try {
    const response = await client.callTool({
      name: "rename_current_thread",
      arguments: { title: "标题" },
    });
    assert.equal(response.isError, true);
    assert.deepEqual(response.structuredContent, {
      ok: false,
      code: RESULT_CODES.THREAD_CONTEXT_MISSING,
    });
  } finally {
    await client.close();
    await server.close();
  }
});

test("MCP stdio 入口通过联接目录启动时仍可完成握手", async () => {
  const client = new Client({ name: "stdio-entry-test", version: "1.0.0" });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [resolve(process.cwd(), "index.mjs")],
    stderr: "pipe",
  });

  await client.connect(transport);
  try {
    const tools = await client.listTools();
    assert.deepEqual(tools.tools.map((tool) => tool.name), ["rename_current_thread"]);
  } finally {
    await client.close();
  }
});
