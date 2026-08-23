#!/usr/bin/env node
/**
 * push_pubkey.js — 密码首连推送公钥到服务器 authorized_keys
 *
 * 用途：SSH 免密接入的「第一次也是唯一一次」需要密码的步骤。
 * 之后所有连接走密钥认证，密码用后即弃、不落盘。
 *
 * 依赖：ssh2（npm install ssh2）
 *
 * 用法：
 *   SSH_PASSWORD='<password>' node push_pubkey.js \
 *     --host <host> --port <port> --user <username> \
 *     --pubkey "C:\Users\luode\.ssh\id_ed25519_<alias>.pub"
 *
 * 密码来源优先级：--password 参数 > 环境变量 SSH_PASSWORD > 交互式输入。
 * 推荐环境变量方式，避免命令行进程列表暴露。
 *
 * 退出码：0 成功；1 失败。
 */

'use strict';

const { Client } = require('ssh2');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const cur = argv[i];
    if (cur.startsWith('--')) {
      const key = cur.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

function askPassword(host, user) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(`请输入 ${user}@${host} 的密码: `, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

function execRemote(conn, command) {
  return new Promise((resolve, reject) => {
    conn.exec(command, (err, stream) => {
      if (err) return reject(err);
      let stdout = '';
      let stderr = '';
      stream.on('close', (code) => resolve({ code, stdout, stderr }));
      stream.on('data', (d) => { stdout += d.toString(); });
      stream.stderr.on('data', (d) => { stderr += d.toString(); });
    });
  });
}

async function main() {
  const args = parseArgs(process.argv);
  const host = args.host;
  const port = parseInt(args.port || '22', 10);
  const user = args.user;
  const pubkeyPath = args.pubkey;

  if (!host || !user || !pubkeyPath) {
    console.error('缺少参数。用法：node push_pubkey.js --host <host> --port <port> --user <user> --pubkey <公钥文件路径>');
    process.exit(1);
  }

  const pubkeyPathResolved = path.resolve(pubkeyPath);
  if (!fs.existsSync(pubkeyPathResolved)) {
    console.error(`公钥文件不存在: ${pubkeyPathResolved}`);
    process.exit(1);
  }

  // 密码来源：--password > SSH_PASSWORD > 交互式输入
  let password = args.password || process.env.SSH_PASSWORD;
  if (!password) {
    password = await askPassword(host, user);
  }

  const pubkey = fs.readFileSync(pubkeyPathResolved, 'utf8').trim();
  if (!pubkey.startsWith('ssh-')) {
    console.error('公钥文件格式不正确（应为 ssh-ed25519/ssh-rsa/ecdsa 开头的 .pub 文件内容）');
    process.exit(1);
  }

  const conn = new Client();

  conn.on('ready', async () => {
    try {
      // 1) 确保远端 ~/.ssh 存在且权限正确
      const mkdir = await execRemote(conn, 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys');
      if (mkdir.code !== 0) {
        throw new Error(`初始化远端 .ssh 失败: ${mkdir.stderr || mkdir.stdout}`);
      }

      // 2) 检查公钥是否已存在（幂等）
      const escaped = pubkey.replace(/'/g, "'\\''");
      const check = await execRemote(conn, `grep -qF -- "${escaped}" ~/.ssh/authorized_keys 2>/dev/null; echo $?`);
      const grepCode = parseInt((check.stdout || '').trim() || '1', 10);

      if (grepCode === 0) {
        console.log('公钥已存在于 authorized_keys，跳过追加（幂等）。');
      } else {
        // 3) 追加公钥
        const append = await execRemote(conn, `printf '%s\\n' "${escaped}" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys`);
        if (append.code !== 0) {
          throw new Error(`追加公钥失败: ${append.stderr || append.stdout}`);
        }
        console.log(`公钥已推送到 ${user}@${host}:~/.ssh/authorized_keys`);
      }

      conn.end();
      process.exit(0);
    } catch (err) {
      console.error(`推送失败: ${err.message}`);
      conn.end();
      process.exit(1);
    }
  });

  conn.on('error', (err) => {
    console.error(`SSH 连接失败: ${err.message}`);
    process.exit(1);
  });

  conn.connect({
    host,
    port,
    username: user,
    password,
    readyTimeout: 30000,
    keepaliveInterval: 10000,
  });
}

main().catch((err) => {
  console.error(`未预期错误: ${err.message}`);
  process.exit(1);
});
