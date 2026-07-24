import assert from "node:assert/strict";
import test from "node:test";
import { mkdtempSync, writeFileSync, readFileSync, readdirSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  resolveCodexHome,
  registrationBlock,
  ensureRegistered,
  probeRegistered,
  depsInstalled,
} from "../bootstrap.mjs";

// 构造隔离临时目录，避免测试触碰真实 config.toml。
function tempConfig(initial) {
  const dir = mkdtempSync(join(tmpdir(), "ttr-boot-"));
  const configPath = join(dir, "config.toml");
  writeFileSync(configPath, initial, { encoding: "utf8" });
  return { dir, configPath };
}

test("registrationBlock 生成含 node 与 server 路径的 TOML 表", () => {
  const block = registrationBlock("C:/node.exe", "C:/index.mjs");
  assert.match(block, /\[mcp_servers\.thread_session\]/);
  assert.match(block, /command = 'C:\/node\.exe'/);
  assert.match(block, /args = \['C:\/index\.mjs'\]/);
  assert.match(block, /startup_timeout_sec = 30/);
});

test("resolveCodexHome 优先取 CODEX_HOME", () => {
  assert.equal(resolveCodexHome({ CODEX_HOME: "C:/custom/.codex" }).replace(/\\/g, "/"), "C:/custom/.codex");
});

test("ensureRegistered 缺失时追加并备份，重复运行幂等", () => {
  const { configPath } = tempConfig("[mcp_servers]\n\n[mcp_servers.node_repl]\ncommand = 'x'\n");

  const first = ensureRegistered({ configPath, nodePath: "C:/node.exe", serverPath: "C:/index.mjs" });
  assert.equal(first.registered, "added");
  assert.ok(first.backupPath, "首次写入应生成备份");
  const afterFirst = readFileSync(configPath, "utf8");
  assert.match(afterFirst, /\[mcp_servers\.thread_session\]/);
  // 原有内容保留。
  assert.match(afterFirst, /\[mcp_servers\.node_repl\]/);

  const second = ensureRegistered({ configPath, nodePath: "C:/node.exe", serverPath: "C:/index.mjs" });
  assert.equal(second.registered, "already");
  assert.equal(second.backupPath, null);
  // 幂等：表头只出现一次。
  const occurrences = readFileSync(configPath, "utf8").split("[mcp_servers.thread_session]").length - 1;
  assert.equal(occurrences, 1);
});

test("depsInstalled 依据 node_modules 是否存在判断", () => {
  const dir = mkdtempSync(join(tmpdir(), "ttr-deps-"));
  assert.equal(depsInstalled(dir), false);
});
test("probeRegistered 只读判断注册状态，不写文件", () => {
  const { configPath } = tempConfig("# empty\n");
  const before = readFileSync(configPath, "utf8");
  assert.equal(probeRegistered(configPath), false);
  // 只读：文件内容零变化。
  assert.equal(readFileSync(configPath, "utf8"), before);

  const withReg = tempConfig("[mcp_servers.thread_session]\ncommand = 'x'\n");
  assert.equal(probeRegistered(withReg.configPath), true);
});

test("bootstrap --check 只读探测：config 零变化、不建 node_modules、输出含 mode:check", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const bootstrapPath = join(here, "..", "bootstrap.mjs");
  const home = mkdtempSync(join(tmpdir(), "ttr-check-"));
  const configPath = join(home, "config.toml");
  writeFileSync(configPath, "# empty\n", { encoding: "utf8" });
  const before = readFileSync(configPath, "utf8");

  const result = spawnSync(process.execPath, [bootstrapPath, "--check"], {
    env: { ...process.env, CODEX_HOME: home },
    encoding: "utf8",
  });

  assert.equal(result.status, 0);
  const status = JSON.parse(result.stdout.trim());
  assert.equal(status.mode, "check");
  assert.equal(status.ok, true);
  assert.equal(status.reloadRequired, false);
  assert.equal(status.backupPath, null);
  // registered 反映真实现状：临时 config 未注册。
  assert.equal(status.registered, "missing");
  // 只读：config 内容零变化、临时 CODEX_HOME 下不创建 node_modules。
  assert.equal(readFileSync(configPath, "utf8"), before);
  assert.equal(existsSync(join(home, "node_modules")), false);
});
