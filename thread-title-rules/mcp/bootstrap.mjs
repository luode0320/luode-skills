import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, appendFileSync, copyFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

// 本脚本负责 thread-title-rules MCP 的本机自举：确保依赖已安装、确保
// rename_current_thread 已注册进 Codex config.toml。全部动作幂等，可重复运行。

const TABLE_HEADER = "[mcp_servers.thread_session]";

/**
 * 解析当前 Codex 主目录（CODEX_HOME 优先，否则回退到 ~/.codex）。
 * [参数] env：环境变量对象，默认 process.env。
 * [返回] Codex 主目录绝对路径。
 * 最近修改时间：2026-07-24，用于定位需要注册的 config.toml。
 */
export function resolveCodexHome(env = process.env) {
  const fromEnv = typeof env.CODEX_HOME === "string" ? env.CODEX_HOME.trim() : "";
  return fromEnv ? resolve(fromEnv) : join(homedir(), ".codex");
}

/**
 * 判断 mcp 目录依赖是否已安装。
 * [参数] mcpDir：mcp 目录绝对路径。
 * [返回] node_modules 存在返回 true。
 * 最近修改时间：2026-07-24，作为跳过 npm 安装的判断依据。
 */
export function depsInstalled(mcpDir) {
  return existsSync(join(mcpDir, "node_modules"));
}

/**
 * 生成写入 config.toml 的注册片段（TOML 字面量字符串，避免路径转义问题）。
 * [参数] nodePath：Node 可执行文件路径；serverPath：index.mjs 绝对路径。
 * [返回] 以换行开头的注册块文本。
 * 最近修改时间：2026-07-24，固定统一工具注册格式。
 */
export function registrationBlock(nodePath, serverPath) {
  return [
    "",
    TABLE_HEADER,
    `command = '${nodePath}'`,
    `args = ['${serverPath}']`,
    "startup_timeout_sec = 30",
    "",
  ].join("\n");
}

/**
 * 确保 config.toml 已注册 thread_session；缺失时先备份再追加。
 * [参数] configPath：config.toml 路径；nodePath：Node 路径；serverPath：index.mjs 路径。
 * [返回] { registered: 'added'|'already', backupPath: string|null }。
 * 最近修改时间：2026-07-24，幂等注册并保留备份。
 */
export function ensureRegistered({ configPath, nodePath, serverPath }) {
  const existing = existsSync(configPath) ? readFileSync(configPath, "utf8") : "";
  // 1. 已存在注册表头时不重复写入。
  if (existing.includes(TABLE_HEADER)) {
    return { registered: "already", backupPath: null };
  }

  // 2. 写入前对既有配置做时间戳备份，避免误写破坏全局配置。
  let backupPath = null;
  if (existing) {
    const stamp = new Date().toISOString().replace(/[:.]/g, "").replace("T", "").slice(0, 14);
    backupPath = `${configPath}.bak-${stamp}`;
    copyFileSync(configPath, backupPath);
  }

  // 3. UTF-8 无 BOM 追加统一工具注册块。
  appendFileSync(configPath, registrationBlock(nodePath, serverPath), { encoding: "utf8" });
  return { registered: "added", backupPath };
}

/**
 * 只读探测 config.toml 是否已注册 thread_session，绝不写入 / 备份。
 * [参数] configPath：config.toml 路径。
 * [返回] 已含注册表头返回 true。
 * 最近修改时间：2026-07-24，供 --check 只读检测子 agent 使用。
 */
export function probeRegistered(configPath) {
  const existing = existsSync(configPath) ? readFileSync(configPath, "utf8") : "";
  return existing.includes(TABLE_HEADER);
}

/**
 * 在 mcp 目录安装锁定依赖；node_modules 已存在时直接跳过。
 * [参数] mcpDir：mcp 目录绝对路径。
 * [返回] 'already' | 'installed' | 'failed'。
 * 最近修改时间：2026-07-24，容错处理 npm 缺失与安装失败。
 */
export function ensureDeps(mcpDir) {
  if (depsInstalled(mcpDir)) {
    return "already";
  }
  const npm = process.platform === "win32" ? "npm.cmd" : "npm";
  const result = spawnSync(npm, ["ci", "--omit=dev"], {
    cwd: mcpDir,
    stdio: "ignore",
    shell: false,
  });
  if (result.status === 0 && depsInstalled(mcpDir)) {
    return "installed";
  }
  return "failed";
}

/**
 * 自举主流程：确保依赖与注册，并打印稳定 JSON 状态。
 * [参数] 无。
 * [返回] Promise<void>。
 * 最近修改时间：2026-07-24，输出机器可读状态并标注是否需要重载。
 */
async function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const serverPath = join(here, "index.mjs");
  const codexHome = resolveCodexHome();
  const configPath = join(codexHome, "config.toml");

  // --check：只读探测现状，不装依赖、不写 config、不备份，供检测子 agent 并行调用。
  if (process.argv.slice(2).includes("--check")) {
    const checkStatus = {
      ok: true,
      mode: "check",
      deps: depsInstalled(here) ? "already" : "missing",
      registered: probeRegistered(configPath) ? "already" : "missing",
      reloadRequired: false,
      configPath,
      serverPath,
      backupPath: null,
    };
    console.log(JSON.stringify(checkStatus));
    return;
  }

  const deps = ensureDeps(here);
  const reg = ensureRegistered({
    configPath,
    nodePath: process.execPath,
    serverPath,
  });

  // 注册只在宿主重载 / 新任务后生效；本轮无法热加载工具。
  const reloadRequired = reg.registered === "added";
  const status = {
    ok: deps !== "failed",
    deps,
    registered: reg.registered,
    reloadRequired,
    configPath,
    serverPath,
    backupPath: reg.backupPath,
  };
  console.log(JSON.stringify(status));
}

// 仅在作为入口脚本直接运行时执行自举，被 import 时只暴露纯函数。
if (import.meta.url === pathToFileURL(resolve(process.argv[1] ?? "")).href) {
  main().catch((error) => {
    console.log(JSON.stringify({ ok: false, error: String(error && error.message ? error.message : error) }));
    process.exitCode = 1;
  });
}