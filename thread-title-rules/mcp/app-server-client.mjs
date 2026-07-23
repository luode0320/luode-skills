import { spawn as nodeSpawn } from "node:child_process";

export const APP_SERVER_CODES = Object.freeze({
  UNAVAILABLE: "APP_SERVER_UNAVAILABLE",
  REJECTED: "APP_SERVER_REJECTED",
  TIMEOUT: "TIMEOUT",
});

export class AppServerError extends Error {
  /**
   * 创建只包含公开错误码的 App Server 异常。
   * [参数] code：允许返回给模型的稳定错误码。
   * [返回] AppServerError 实例。
   * 最近修改时间：2026-07-23 01:45:52，补齐公开错误对象的注释契约。
   */
  constructor(code) {
    super(code);
    this.name = "AppServerError";
    this.code = code;
  }
}

/**
 * 将稳定错误码包装为公开异常，避免泄露底层响应。
 * [参数] code：稳定错误码。
 * [返回] AppServerError 实例。
 * 最近修改时间：2026-07-23 01:45:52，补齐错误包装函数说明。
 */
function createPublicError(code) {
  return new AppServerError(code);
}

/**
 * 仅依据真实退出状态判断子进程是否仍存活。
 * [参数] child：Node 子进程对象。
 * [返回] 进程尚未产生 exitCode 或 signalCode 时返回 true。
 * 最近修改时间：2026-07-23 01:45:52，避免把 killed 标记误判为已退出。
 */
function isProcessAlive(child) {
  return child.exitCode === null && child.signalCode === null;
}

/**
 * 在限定时间内等待子进程产生真实退出状态。
 * [参数] child：Node 子进程对象；timeoutMs：最大等待毫秒数。
 * [返回] Promise<boolean>，true 表示已观察到退出。
 * 最近修改时间：2026-07-23 01:45:52，处理监听注册期间的退出竞态。
 */
function waitForExit(child, timeoutMs) {
  // 1. 已退出的进程直接返回，避免重复注册监听器。
  if (!isProcessAlive(child)) {
    return Promise.resolve(true);
  }

  // 2. 同时监听 exit/error 和超时，并在任一路径完成后清理监听器。
  return new Promise((resolve) => {
    let timer;
    let settled = false;

    const finish = (exited) => {
      if (settled) {
        return;
      }
      settled = true;
      clearTimeout(timer);
      child.removeListener("exit", onExit);
      child.removeListener("error", onError);
      resolve(exited);
    };
    const onExit = () => finish(true);
    const onError = () => finish(false);

    child.once("exit", onExit);
    child.once("error", onError);
    if (!isProcessAlive(child)) {
      finish(true);
      return;
    }

    timer = setTimeout(() => finish(!isProcessAlive(child)), timeoutMs);
    timer.unref?.();
  });
}

/**
 * 解析 Windows 系统目录中的 taskkill 可执行文件。
 * [参数] systemRoot：Windows 系统根目录。
 * [返回] taskkill.exe 的可执行路径或 PATH 回退名称。
 * 最近修改时间：2026-07-23 01:45:52，固定无 Shell 的进程树清理入口。
 */
function taskkillExecutable(systemRoot) {
  const normalizedRoot = systemRoot?.trim().replace(/[\\/]+$/, "");
  return normalizedRoot
    ? `${normalizedRoot}\\System32\\taskkill.exe`
    : "taskkill.exe";
}

/**
 * 等待并在必要时终止用于清理的控制进程。
 * [参数] child：taskkill 等控制进程；graceMs：优雅退出等待时间。
 * [返回] Promise<void>。
 * 最近修改时间：2026-07-23 01:45:52，避免清理控制进程自身遗留。
 */
async function stopControlProcess(child, graceMs) {
  // 1. 先等待控制进程自然完成。
  await waitForExit(child, graceMs);
  if (!isProcessAlive(child)) {
    return;
  }

  // 2. 超时后终止控制进程并再次等待真实退出。
  try {
    child.kill();
  } catch {
    return;
  }
  await waitForExit(child, graceMs);
}

/**
 * 跨平台终止 App Server 包装进程及其后代。
 * [参数] child：目标子进程；platform：平台；graceMs：等待时间；spawnControlProcess：控制进程启动器；systemRoot：Windows 系统根目录。
 * [返回] Promise<void>。
 * 最近修改时间：2026-07-23 01:45:52，Windows 改为 taskkill /t /f 并等待真实退出。
 */
async function terminateProcessTree(child, {
  platform,
  graceMs,
  spawnControlProcess,
  systemRoot,
}) {
  // 1. 已退出时不再发送任何终止信号。
  if (!isProcessAlive(child)) {
    return;
  }

  // 2. Windows 优先使用 taskkill 终止完整进程树，而不是只杀 cmd 包装进程。
  if (platform === "win32" && Number.isSafeInteger(child.pid) && child.pid > 0) {
    let taskkill;
    try {
      taskkill = spawnControlProcess(
        taskkillExecutable(systemRoot),
        ["/pid", String(child.pid), "/t", "/f"],
        {
          stdio: "ignore",
          windowsHide: true,
          shell: false,
        },
      );
    } catch {
      taskkill = null;
    }

    if (taskkill) {
      await Promise.all([
        stopControlProcess(taskkill, graceMs),
        waitForExit(child, graceMs),
      ]);
    }
  }

  // 3. 控制进程不可用或目标仍存活时，执行平台对应的直接终止兜底。
  if (!isProcessAlive(child)) {
    return;
  }

  try {
    child.kill(platform === "win32" ? "SIGKILL" : "SIGTERM");
  } catch {
    return;
  }
  await waitForExit(child, graceMs);

  // 4. 非 Windows 的优雅终止未生效时升级为 SIGKILL。
  if (platform !== "win32" && isProcessAlive(child)) {
    try {
      child.kill("SIGKILL");
    } catch {
      return;
    }
    await waitForExit(child, graceMs);
  }
}

class AppServerSession {
  /**
   * 建立单次 App Server JSON-RPC 会话并注册流事件。
   * [参数] child：已启动且带 stdin/stdout 的 App Server 子进程。
   * [返回] AppServerSession 实例。
   * 最近修改时间：2026-07-23 01:45:52，补齐会话初始化与异常监听说明。
   */
  constructor(child) {
    // 1. 先验证协议所需的标准输入输出流。
    if (!child?.stdin || !child?.stdout) {
      throw createPublicError(APP_SERVER_CODES.UNAVAILABLE);
    }

    // 2. 初始化请求状态并绑定输出、错误和退出事件。
    this.child = child;
    this.nextRequestId = 1;
    this.pending = new Map();
    this.buffer = "";
    this.failure = null;
    this.closing = false;

    const failUnavailable = () => this.fail(createPublicError(APP_SERVER_CODES.UNAVAILABLE));
    child.stdout.setEncoding("utf8");
    child.stdout.on("data", (chunk) => this.#consume(chunk));
    child.stdout.on("error", failUnavailable);
    child.stdin.on("error", failUnavailable);
    child.stderr?.on("error", failUnavailable);
    child.stderr?.resume();
    child.once("error", failUnavailable);
    child.once("exit", () => {
      if (!this.closing) {
        failUnavailable();
      }
    });
  }

  /**
   * 发送带请求 ID 的 JSON-RPC 请求。
   * [参数] method：方法名；params：请求参数。
   * [返回] Promise<any>，收到对应响应时完成。
   * 最近修改时间：2026-07-23 01:45:52，补齐请求生命周期说明。
   */
  request(method, params) {
    // 1. 会话已失败时直接复用稳定错误。
    if (this.failure) {
      return Promise.reject(this.failure);
    }

    // 2. 注册待处理请求后写入单行 JSON-RPC 消息。
    const id = this.nextRequestId++;
    const response = new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });

    try {
      this.#write({ id, method, params });
    } catch {
      const error = createPublicError(APP_SERVER_CODES.UNAVAILABLE);
      this.fail(error);
      return Promise.reject(error);
    }

    return response;
  }

  /**
   * 发送不需要响应的 JSON-RPC 通知。
   * [参数] method：通知方法名。
   * [返回] 无。
   * 最近修改时间：2026-07-23 01:45:52，补齐 initialized 通知说明。
   */
  notify(method) {
    if (this.failure) {
      throw this.failure;
    }
    this.#write({ method });
  }

  /**
   * 将会话标记为失败并拒绝全部待处理请求。
   * [参数] error：公开稳定异常。
   * [返回] 无。
   * 最近修改时间：2026-07-23 01:45:52，统一异常、超时与退出失败收口。
   */
  fail(error) {
    if (this.failure) {
      return;
    }

    this.failure = error;
    for (const { reject } of this.pending.values()) {
      reject(error);
    }
    this.pending.clear();
  }

  /**
   * 关闭输入流并在必要时回收完整进程树。
   * [参数] graceMs：等待时间；platform：平台；spawnControlProcess：清理进程启动器；systemRoot：Windows 系统目录。
   * [返回] Promise<void>。
   * 最近修改时间：2026-07-23 01:45:52，保证成功和失败路径都等待真实退出。
   */
  async close({ graceMs, platform, spawnControlProcess, systemRoot }) {
    // 1. 停止新请求并关闭标准输入，优先让 App Server 自然退出。
    this.closing = true;
    this.fail(createPublicError(APP_SERVER_CODES.UNAVAILABLE));

    if (!this.child.stdin.destroyed) {
      this.child.stdin.end();
    }

    // 2. 优雅等待失败时终止完整进程树。
    await waitForExit(this.child, graceMs);
    if (isProcessAlive(this.child)) {
      await terminateProcessTree(this.child, {
        platform,
        graceMs,
        spawnControlProcess,
        systemRoot,
      });
    }
  }

  /**
   * 将一条 JSON-RPC 消息写入 App Server 标准输入。
   * [参数] message：可序列化的协议消息。
   * [返回] 无。
   * 最近修改时间：2026-07-23 01:45:52，固定 UTF-8 单行协议写入。
   */
  #write(message) {
    this.child.stdin.write(`${JSON.stringify(message)}\n`, "utf8");
  }

  /**
   * 消费标准输出中的换行分隔 JSON-RPC 响应。
   * [参数] chunk：UTF-8 输出片段。
   * [返回] 无。
   * 最近修改时间：2026-07-23 01:45:52，新增合法 JSON 非对象保护并稳定映射拒绝码。
   */
  #consume(chunk) {
    // 1. 累积可能被拆分的输出片段并逐行解析。
    this.buffer += chunk;

    while (true) {
      // 1.1. 不完整行保留到下一批数据。
      const newlineIndex = this.buffer.indexOf("\n");
      if (newlineIndex < 0) {
        return;
      }

      // 1.2. 空行忽略，非空行必须是 JSON 对象。
      const line = this.buffer.slice(0, newlineIndex).trim();
      this.buffer = this.buffer.slice(newlineIndex + 1);
      if (line.length === 0) {
        continue;
      }

      let message;
      try {
        message = JSON.parse(line);
      } catch {
        this.fail(createPublicError(APP_SERVER_CODES.REJECTED));
        return;
      }

      // 1.3. 合法 JSON 的 null、数组和标量同样不是协议对象，统一拒绝以免触发 TypeError。
      if (!message || typeof message !== "object" || Array.isArray(message)) {
        this.fail(createPublicError(APP_SERVER_CODES.REJECTED));
        return;
      }

      // 1.4. 通知和未知请求 ID 不影响当前待处理请求。
      if (!("id" in message)) {
        continue;
      }

      // 1.5. 只解析匹配请求 ID 的 result 或 error。
      const pending = this.pending.get(message.id);
      if (!pending) {
        continue;
      }
      this.pending.delete(message.id);

      if (message.error) {
        pending.reject(createPublicError(APP_SERVER_CODES.REJECTED));
      } else if ("result" in message) {
        pending.resolve(message.result);
      } else {
        pending.reject(createPublicError(APP_SERVER_CODES.REJECTED));
      }
    }
  }
}

/**
 * 生成当前平台启动 Codex App Server 的命令。
 * [参数] platform：Node 平台名；commandProcessor：Windows 命令处理器。
 * [返回] executable 与 args 组成的命令对象。
 * 最近修改时间：2026-07-23 01:45:52，保持 Windows codex.cmd 与其他平台 codex 的分流。
 */
function appServerCommand(platform, commandProcessor) {
  if (platform === "win32") {
    return {
      executable: commandProcessor,
      args: ["/d", "/s", "/c", "codex.cmd app-server --stdio"],
    };
  }

  return {
    executable: "codex",
    args: ["app-server", "--stdio"],
  };
}

/**
 * 通过 Codex App Server 修改线程名称，并保证异常路径能够回收子进程。
 * [参数] threadId：宿主当前任务 ID；name：新标题；timeoutMs：协议超时；cleanupGraceMs：清理等待；signal：取消信号；其余参数为测试注入点。
 * [返回] Promise<void>，成功表示 App Server 已接受改名。
 * 最近修改时间：2026-07-23 01:45:52，补齐进程树回收和合法响应防护后的调用契约。
 */
export async function renameThreadWithAppServer({
  threadId,
  name,
  timeoutMs = 5_000,
  cleanupGraceMs = 100,
  signal,
  spawnProcess = nodeSpawn,
  spawnControlProcess = nodeSpawn,
  platform = process.platform,
  commandProcessor = process.env.ComSpec || "cmd.exe",
  systemRoot = process.env.SystemRoot,
} = {}) {
  // 1. 使用无 Shell 参数启动单次 App Server 子进程。
  const command = appServerCommand(platform, commandProcessor);
  let child;
  try {
    child = spawnProcess(command.executable, command.args, {
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
      shell: false,
    });
  } catch {
    throw createPublicError(APP_SERVER_CODES.UNAVAILABLE);
  }

  // 2. 建立协议会话；初始化失败也必须回收已启动的进程树。
  let session;
  try {
    session = new AppServerSession(child);
  } catch (error) {
    if (child) {
      await terminateProcessTree(child, {
        platform,
        graceMs: cleanupGraceMs,
        spawnControlProcess,
        systemRoot,
      });
    }
    throw error instanceof AppServerError
      ? error
      : createPublicError(APP_SERVER_CODES.UNAVAILABLE);
  }

  // 3. 注册统一超时与外部取消信号，避免请求永久挂起。
  const timeoutError = createPublicError(APP_SERVER_CODES.TIMEOUT);
  let timeoutHandle;
  const onAbort = () => session.fail(timeoutError);
  signal?.addEventListener("abort", onAbort, { once: true });

  const timeout = new Promise((_, reject) => {
    timeoutHandle = setTimeout(() => {
      session.fail(timeoutError);
      reject(timeoutError);
    }, timeoutMs);
    timeoutHandle.unref?.();
  });

  // 4. 按顺序完成 initialize、initialized 和 thread/name/set。
  const operation = (async () => {
    await session.request("initialize", {
      clientInfo: {
        name: "thread-title-rules-mcp",
        version: "1.0.0",
      },
      capabilities: {
        experimentalApi: true,
      },
    });
    session.notify("initialized");
    await session.request("thread/name/set", {
      threadId,
      name,
    });
  })();

  // 5. 无论成功或失败都关闭会话、清理计时器并等待操作 Promise 收口。
  try {
    if (signal?.aborted) {
      throw timeoutError;
    }
    await Promise.race([operation, timeout]);
  } catch (error) {
    if (error instanceof AppServerError) {
      throw error;
    }
    throw createPublicError(APP_SERVER_CODES.REJECTED);
  } finally {
    clearTimeout(timeoutHandle);
    signal?.removeEventListener("abort", onAbort);
    await session.close({
      graceMs: cleanupGraceMs,
      platform,
      spawnControlProcess,
      systemRoot,
    });
    await operation.catch(() => undefined);
  }
}
