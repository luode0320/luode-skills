import { realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  APP_SERVER_CODES,
  AppServerError,
  renameThreadWithAppServer,
} from "./app-server-client.mjs";

export const RESULT_CODES = Object.freeze({
  RENAMED: "RENAMED",
  INVALID_TITLE: "INVALID_TITLE",
  THREAD_CONTEXT_MISSING: "THREAD_CONTEXT_MISSING",
  APP_SERVER_UNAVAILABLE: APP_SERVER_CODES.UNAVAILABLE,
  APP_SERVER_REJECTED: APP_SERVER_CODES.REJECTED,
  TIMEOUT: APP_SERVER_CODES.TIMEOUT,
});

const THREAD_ID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const PUBLIC_FAILURE_CODES = new Set([
  RESULT_CODES.APP_SERVER_UNAVAILABLE,
  RESULT_CODES.APP_SERVER_REJECTED,
  RESULT_CODES.TIMEOUT,
]);

/**
 * 校验宿主线程 ID 是否为标准 UUID 字符串。
 * [参数] value：待校验值。
 * [返回] 合法 UUID 返回 true。
 * 最近修改时间：2026-07-23 01:45:52，限定可信元数据格式。
 */
function validThreadId(value) {
  return typeof value === "string" && THREAD_ID_PATTERN.test(value);
}

/**
 * 从 Codex App 宿主注入元数据中解析唯一当前任务 ID。
 * [参数] meta：MCP 请求 `_meta`。
 * [返回] 唯一合法 threadId；缺失、错误或冲突时返回 null。
 * 最近修改时间：2026-07-23 01:45:52，移除未声明别名并禁止从业务参数猜测。
 */
export function extractThreadId(meta) {
  // 1. 非对象元数据不能提供可信当前任务身份。
  if (!meta || typeof meta !== "object") {
    return null;
  }

  // 2. 仅采纳契约声明的直接字段和 turn metadata snake_case 字段。
  const turnMetadata = meta["x-codex-turn-metadata"];
  const candidates = [
    meta.threadId,
    turnMetadata && typeof turnMetadata === "object" ? turnMetadata.thread_id : undefined,
  ].filter((value) => value !== undefined);

  // 3. 任一候选非法或多个来源冲突时拒绝执行改名。
  if (candidates.length === 0 || candidates.some((value) => !validThreadId(value))) {
    return null;
  }

  const unique = new Set(candidates);
  return unique.size === 1 ? candidates[0] : null;
}

/**
 * 清理并校验模型生成的标题。
 * [参数] title：原始标题。
 * [返回] 1-24 个 Unicode 字符的标题；否则返回 null。
 * 最近修改时间：2026-07-23 01:45:52，固定统一工具标题边界。
 */
function normalizeTitle(title) {
  if (typeof title !== "string") {
    return null;
  }

  const normalized = title.trim();
  const length = Array.from(normalized).length;
  return length >= 1 && length <= 24 ? normalized : null;
}

/**
 * 生成稳定、最小化的公开工具结果。
 * [参数] ok：是否成功；code：稳定结果码；title：可选成功标题。
 * [返回] 不含底层路径或原始响应的结果对象。
 * 最近修改时间：2026-07-23 01:45:52，保持公开返回契约最小化。
 */
function result(ok, code, title) {
  return title === undefined ? { ok, code } : { ok, code, title };
}

/**
 * 校验输入和宿主上下文后执行当前任务改名。
 * [参数] title：模型标题；meta：宿主元数据；signal：取消信号；renameThread：App Server 适配器。
 * [返回] Promise，结果为统一工具公开结构。
 * 最近修改时间：2026-07-23 01:45:52，明确宿主信任边界和稳定错误映射。
 */
export async function executeRenameCurrentThread({
  title,
  meta,
  signal,
  renameThread = renameThreadWithAppServer,
} = {}) {
  // 1. 标题不合法时在接触任务上下文前直接返回稳定错误码。
  const normalizedTitle = normalizeTitle(title);
  if (!normalizedTitle) {
    return result(false, RESULT_CODES.INVALID_TITLE);
  }

  // 2. 当前任务身份缺失或冲突时拒绝猜测。
  const threadId = extractThreadId(meta);
  if (!threadId) {
    return result(false, RESULT_CODES.THREAD_CONTEXT_MISSING);
  }

  // 3. 调用宿主适配器，并将内部异常收敛为公开错误码。
  try {
    await renameThread({
      threadId,
      name: normalizedTitle,
      signal,
    });
    return result(true, RESULT_CODES.RENAMED, normalizedTitle);
  } catch (error) {
    const code = error instanceof AppServerError && PUBLIC_FAILURE_CODES.has(error.code)
      ? error.code
      : RESULT_CODES.APP_SERVER_REJECTED;
    return result(false, code);
  }
}

const inputSchema = z.strictObject({
  title: z.string().describe("新的当前任务标题，去除首尾空白后长度为 1 到 24 个字符"),
});

const outputSchema = z.strictObject({
  ok: z.boolean(),
  code: z.enum(Object.values(RESULT_CODES)),
  title: z.string().optional(),
});

/**
 * 将公开结果包装为 MCP structuredContent 和文本内容。
 * [参数] value：统一工具公开结果。
 * [返回] MCP tool result，失败结果设置 isError。
 * 最近修改时间：2026-07-23 01:45:52，确保模型和结构化客户端获得同一结果。
 */
function toToolResult(value) {
  return {
    content: [{ type: "text", text: JSON.stringify(value) }],
    structuredContent: value,
    isError: !value.ok,
  };
}

/**
 * 创建只公开当前任务重命名工具的 MCP Server。
 * [参数] renameThread：可注入的 App Server 适配器。
 * [返回] 已注册 `rename_current_thread` 的 McpServer。
 * 最近修改时间：2026-07-23 01:45:52，固定单工具和严格 title schema。
 */
export function createRenameServer({ renameThread = renameThreadWithAppServer } = {}) {
  // 1. 创建本地 stdio MCP Server。
  const server = new McpServer({
    name: "thread-title-rules-mcp",
    version: "1.0.0",
  });

  // 2. 注册严格输入输出 schema，并把宿主 `_meta` 交给执行函数。
  server.registerTool(
    "rename_current_thread",
    {
      title: "重命名当前任务",
      description: "信任 Codex App 宿主注入的 MCP 请求元数据识别当前 threadId，并修改当前任务名称。",
      inputSchema,
      outputSchema,
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ title }, extra) => {
      const value = await executeRenameCurrentThread({
        title,
        meta: extra._meta,
        signal: extra.signal,
        renameThread,
      });
      return toToolResult(value);
    },
  );

  return server;
}

/**
 * 连接 stdio transport 并启动本地 MCP Server。
 * [参数] 无。
 * [返回] Promise<void>。
 * 最近修改时间：2026-07-23 01:45:52，补齐 MCP 进程入口说明。
 */
async function main() {
  const server = createRenameServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// Codex 的 Skill 目录可能通过联接路径指向真实仓库，比较入口前必须统一为真实路径。
const currentFile = realpathSync(fileURLToPath(import.meta.url));
const entryFile = process.argv[1] ? realpathSync(resolve(process.argv[1])) : "";
if (currentFile === entryFile) {
  main().catch(() => {
    process.exitCode = 1;
  });
}
