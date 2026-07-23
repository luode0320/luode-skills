import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import { EventEmitter } from "node:events";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { PassThrough, Writable } from "node:stream";
import test from "node:test";
import {
  APP_SERVER_CODES,
  AppServerError,
  renameThreadWithAppServer,
} from "../app-server-client.mjs";

const THREAD_ID = "019f8a9d-8618-7602-bdfa-e526f25d83aa";

/**
 * 创建可控的 App Server 假子进程。
 * [参数] onMessage：协议消息回调；options：退出、kill 延迟和 PID 配置。
 * [返回] 具备 stdin/stdout/kill 的 EventEmitter 假进程。
 * 最近修改时间：2026-07-23 01:45:52，支持真实退出状态和进程清理回归。
 */
function createFakeChild(onMessage, {
  exitOnEnd = true,
  initiallyKilled = false,
  killExitDelayMs = 0,
  pid,
} = {}) {
  // 1. 初始化与 Node ChildProcess 一致的最小状态和流。
  const child = new EventEmitter();
  child.stdout = new PassThrough();
  child.stderr = new PassThrough();
  child.pid = pid;
  child.exitCode = null;
  child.signalCode = null;
  child.killed = initiallyKilled;
  child.messages = [];
  child.killCalls = 0;
  child.killSignals = [];

  child.finishExit = (code, signal) => {
    if (child.exitCode !== null || child.signalCode !== null) {
      return;
    }
    child.exitCode = code;
    child.signalCode = signal;
    child.emit("exit", code, signal);
  };

  // 2. 标准输入按行解析 JSON-RPC，并按测试配置控制自然退出。
  let buffer = "";
  child.stdin = new Writable({
    write(chunk, _encoding, callback) {
      buffer += chunk.toString("utf8");
      while (buffer.includes("\n")) {
        const index = buffer.indexOf("\n");
        const line = buffer.slice(0, index);
        buffer = buffer.slice(index + 1);
        if (line.trim()) {
          const message = JSON.parse(line);
          child.messages.push(message);
          onMessage?.(message, child);
        }
      }
      callback();
    },
    final(callback) {
      if (exitOnEnd && child.exitCode === null && child.signalCode === null) {
        queueMicrotask(() => child.finishExit(0, null));
      }
      callback();
    },
  });

  // 3. kill 只先设置发送标记，再按延迟产生真实退出状态。
  child.kill = (signal = "SIGTERM") => {
    child.killCalls += 1;
    child.killSignals.push(signal);
    child.killed = true;
    if (killExitDelayMs > 0) {
      setTimeout(() => child.finishExit(null, signal), killExitDelayMs);
    } else {
      queueMicrotask(() => child.finishExit(null, signal));
    }
    return true;
  };

  return child;
}

/**
 * 向假进程写入完整或拆分的 JSON-RPC 响应。
 * [参数] child：假进程；message：响应对象；split：是否拆分输出片段。
 * [返回] 无。
 * 最近修改时间：2026-07-23 01:45:52，覆盖流分片解析路径。
 */
function writeResponse(child, message, { split = false } = {}) {
  const payload = `${JSON.stringify(message)}\n`;
  if (!split) {
    queueMicrotask(() => child.stdout.write(payload));
    return;
  }

  const middle = Math.floor(payload.length / 2);
  queueMicrotask(() => {
    child.stdout.write(payload.slice(0, middle));
    child.stdout.write(payload.slice(middle));
  });
}

/**
 * 检查真实 Windows 测试后代 PID 是否仍存在。
 * [参数] pid：目标进程 ID。
 * [返回] 进程存在时返回 true。
 * 最近修改时间：2026-07-23 01:45:52，为真实进程树回收提供结果断言。
 */
function processIsAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

test("初始化后调用 thread/name/set，并在成功后关闭进程", async () => {
  let child;
  const spawnProcess = (command, args, options) => {
    assert.equal(command, "cmd.exe");
    assert.deepEqual(args, ["/d", "/s", "/c", "codex.cmd app-server --stdio"]);
    assert.equal(options.shell, false);

    child = createFakeChild((message, currentChild) => {
      if (message.method === "initialize") {
        writeResponse(currentChild, { id: message.id, result: {} }, { split: true });
      } else if (message.method === "thread/name/set") {
        writeResponse(currentChild, { id: message.id, result: {} });
      }
    });
    return child;
  };

  await renameThreadWithAppServer({
    threadId: THREAD_ID,
    name: "模型无关会话重命名",
    spawnProcess,
    platform: "win32",
    commandProcessor: "cmd.exe",
    cleanupGraceMs: 5,
  });

  assert.deepEqual(child.messages, [
    {
      id: 1,
      method: "initialize",
      params: {
        clientInfo: { name: "thread-title-rules-mcp", version: "1.0.0" },
        capabilities: { experimentalApi: true },
      },
    },
    { method: "initialized" },
    {
      id: 2,
      method: "thread/name/set",
      params: { threadId: THREAD_ID, name: "模型无关会话重命名" },
    },
  ]);
  assert.equal(child.exitCode, 0);
  assert.equal(child.killCalls, 0);
});

test("App Server 返回错误时映射为稳定拒绝码并清理进程", async () => {
  let child;
  const spawnProcess = () => {
    child = createFakeChild((message, currentChild) => {
      if (message.method === "initialize") {
        writeResponse(currentChild, { id: message.id, result: {} });
      } else if (message.method === "thread/name/set") {
        writeResponse(currentChild, {
          id: message.id,
          error: { code: -32602, message: "internal detail must not escape" },
        });
      }
    });
    return child;
  };

  await assert.rejects(
    renameThreadWithAppServer({
      threadId: THREAD_ID,
      name: "标题",
      spawnProcess,
      cleanupGraceMs: 5,
    }),
    (error) => error instanceof AppServerError
      && error.code === APP_SERVER_CODES.REJECTED
      && error.message === APP_SERVER_CODES.REJECTED,
  );
  assert.equal(child.exitCode, 0);
});

test("超时后返回 TIMEOUT 并强制终止未退出进程", async () => {
  let child;
  const spawnProcess = () => {
    child = createFakeChild(undefined, {
      exitOnEnd: false,
      killExitDelayMs: 15,
    });
    return child;
  };

  await assert.rejects(
    renameThreadWithAppServer({
      threadId: THREAD_ID,
      name: "标题",
      spawnProcess,
      platform: "linux",
      timeoutMs: 10,
      cleanupGraceMs: 50,
    }),
    (error) => error instanceof AppServerError && error.code === APP_SERVER_CODES.TIMEOUT,
  );
  assert.equal(child.killCalls, 1);
  assert.deepEqual(child.killSignals, ["SIGTERM"]);
  assert.equal(child.signalCode, "SIGTERM");
});

test("Windows 超时清理忽略 killed 标记并等待完整进程树退出", async () => {
  let child;
  const taskkillCalls = [];
  const spawnProcess = () => {
    child = createFakeChild(undefined, {
      exitOnEnd: false,
      initiallyKilled: true,
      pid: 43210,
    });
    return child;
  };
  const spawnControlProcess = (command, args, options) => {
    taskkillCalls.push({ command, args, options });
    const taskkill = new EventEmitter();
    taskkill.exitCode = null;
    taskkill.signalCode = null;
    taskkill.killed = false;
    taskkill.kill = () => {
      taskkill.killed = true;
      queueMicrotask(() => {
        taskkill.signalCode = "SIGTERM";
        taskkill.emit("exit", null, "SIGTERM");
      });
      return true;
    };

    queueMicrotask(() => {
      taskkill.exitCode = 0;
      taskkill.emit("exit", 0, null);
    });
    setTimeout(() => child.finishExit(null, "SIGKILL"), 15);
    return taskkill;
  };

  await assert.rejects(
    renameThreadWithAppServer({
      threadId: THREAD_ID,
      name: "标题",
      spawnProcess,
      spawnControlProcess,
      platform: "win32",
      systemRoot: "C:\\Windows",
      timeoutMs: 10,
      cleanupGraceMs: 50,
    }),
    (error) => error instanceof AppServerError && error.code === APP_SERVER_CODES.TIMEOUT,
  );

  assert.equal(taskkillCalls.length, 1);
  assert.equal(taskkillCalls[0].command, "C:\\Windows\\System32\\taskkill.exe");
  assert.deepEqual(taskkillCalls[0].args, ["/pid", "43210", "/t", "/f"]);
  assert.deepEqual(taskkillCalls[0].options, {
    stdio: "ignore",
    windowsHide: true,
    shell: false,
  });
  assert.equal(child.killCalls, 0);
  assert.equal(child.signalCode, "SIGKILL");
});

test("Windows 超时清理会终止真实子进程树", {
  skip: process.platform !== "win32",
}, async () => {
  const temporaryDirectory = await mkdtemp(join(tmpdir(), "thread-title-rules-"));
  const scriptPath = join(temporaryDirectory, "process-tree-child.mjs");
  const descendantPidPath = join(temporaryDirectory, "descendant.pid");
  let descendantPid;

  await writeFile(scriptPath, `
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";

const descendant = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"], {
  stdio: "ignore",
  windowsHide: true,
});
writeFileSync(process.argv[2], String(descendant.pid), "utf8");
process.stdin.resume();
setInterval(() => {}, 1000);
`, "utf8");

  try {
    await assert.rejects(
      renameThreadWithAppServer({
        threadId: THREAD_ID,
        name: "标题",
        spawnProcess: (_command, _args, options) => spawn(
          process.execPath,
          [scriptPath, descendantPidPath],
          options,
        ),
        platform: "win32",
        timeoutMs: 500,
        cleanupGraceMs: 1_000,
      }),
      (error) => error instanceof AppServerError && error.code === APP_SERVER_CODES.TIMEOUT,
    );

    descendantPid = Number(await readFile(descendantPidPath, "utf8"));
    const deadline = Date.now() + 2_000;
    while (processIsAlive(descendantPid) && Date.now() < deadline) {
      await new Promise((resolve) => setTimeout(resolve, 25));
    }
    assert.equal(processIsAlive(descendantPid), false);
  } finally {
    if (Number.isSafeInteger(descendantPid) && processIsAlive(descendantPid)) {
      spawnSync("taskkill.exe", ["/pid", String(descendantPid), "/t", "/f"], {
        stdio: "ignore",
        windowsHide: true,
        shell: false,
      });
    }
    await rm(temporaryDirectory, { recursive: true, force: true });
  }
});

test("App Server 在响应前异常退出时返回 APP_SERVER_UNAVAILABLE", async () => {
  let child;
  const spawnProcess = () => {
    child = createFakeChild((message, currentChild) => {
      if (message.method === "initialize") {
        currentChild.exitCode = 1;
        queueMicrotask(() => currentChild.emit("exit", 1, null));
      }
    });
    return child;
  };

  await assert.rejects(
    renameThreadWithAppServer({
      threadId: THREAD_ID,
      name: "标题",
      spawnProcess,
      cleanupGraceMs: 5,
    }),
    (error) => error instanceof AppServerError
      && error.code === APP_SERVER_CODES.UNAVAILABLE,
  );
  assert.equal(child.killCalls, 0);
});
test("进程启动失败时返回 APP_SERVER_UNAVAILABLE", async () => {
  const spawnProcess = () => {
    throw new Error("not found");
  };

  await assert.rejects(
    renameThreadWithAppServer({
      threadId: THREAD_ID,
      name: "标题",
      spawnProcess,
    }),
    (error) => error instanceof AppServerError
      && error.code === APP_SERVER_CODES.UNAVAILABLE,
  );
});

test("非法 JSON 响应映射为 APP_SERVER_REJECTED", async () => {
  let child;
  const spawnProcess = () => {
    child = createFakeChild((message, currentChild) => {
      if (message.method === "initialize") {
        queueMicrotask(() => currentChild.stdout.write("not-json\n"));
      }
    });
    return child;
  };

  await assert.rejects(
    renameThreadWithAppServer({
      threadId: THREAD_ID,
      name: "标题",
      spawnProcess,
      cleanupGraceMs: 5,
    }),
    (error) => error instanceof AppServerError && error.code === APP_SERVER_CODES.REJECTED,
  );
  assert.equal(child.exitCode, 0);
});

test("合法 JSON 非对象响应映射为 APP_SERVER_REJECTED", async () => {
  for (const payload of ["null\n", "42\n", "\"text\"\n", "[]\n"]) {
    let child;
    const spawnProcess = () => {
      child = createFakeChild((message, currentChild) => {
        if (message.method === "initialize") {
          queueMicrotask(() => currentChild.stdout.write(payload));
        }
      });
      return child;
    };

    await assert.rejects(
      renameThreadWithAppServer({
        threadId: THREAD_ID,
        name: "标题",
        spawnProcess,
        cleanupGraceMs: 5,
      }),
      (error) => error instanceof AppServerError && error.code === APP_SERVER_CODES.REJECTED,
    );
    assert.equal(child.exitCode, 0);
  }
});
