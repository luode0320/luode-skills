#!/usr/bin/env python3
"""写入 GitHub 仓库级 Actions Secret（libsodium sealed box 加密）。

为什么需要它：GitHub 的 secret 值不可回读，写入必须用仓库公钥做 sealed box 加密；
本机默认没有 `gh` CLI，用本脚本可替代 `gh secret set`。

用法：
    # 单条
    python set_repo_secret.py <owner>/<repo> REMOTE_HOST 203.0.113.10 --token-file ~/.github/token

    # 批量（推荐配四要素时用）
    python set_repo_secret.py <owner>/<repo> --json-file ./repo-env.json --token-file ~/.github/token

repo-env.json 形如：
    {"REMOTE_HOST": "...", "REMOTE_PORT": "18998",
     "REMOTE_USER": "root", "REMOTE_PASSWORD": "..."}

token 解析优先级：--token-file > 环境变量 GITHUB_TOKEN > ~/.github/token。
安全约定：secret 值不回显、不进命令行历史（批量模式从文件读），只输出名称与长度。
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"
DEFAULT_TOKEN_FILE = Path.home() / ".github" / "token"


def load_token(token_file: str | None) -> str:
    if token_file:
        return Path(token_file).expanduser().read_text(encoding="utf-8").strip()
    env_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if env_token:
        return env_token
    if DEFAULT_TOKEN_FILE.exists():
        return DEFAULT_TOKEN_FILE.read_text(encoding="utf-8").strip()
    sys.exit("未找到 token：请用 --token-file 指定，或设置 GITHUB_TOKEN")


def api_request(url: str, token: str, method: str = "GET", body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "repo-env-config")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:300]
        return exc.code, {"error": detail}


def fetch_public_key(repo: str, token: str) -> dict:
    status, data = api_request(f"{API}/repos/{repo}/actions/secrets/public-key", token)
    if status != 200 or not data:
        sys.exit(f"获取仓库公钥失败 status={status} resp={data}")
    return data


def encrypt(value: str, key_b64: str) -> str:
    # 必须显式导入 nacl.public：只 import nacl.bindings 时 nacl.public 不会被挂载，
    # 访问 nacl.public.PublicKey 会报 AttributeError: module 'nacl' has no attribute 'public'
    import nacl.bindings
    import nacl.public

    public_key = nacl.public.PublicKey(base64.b64decode(key_b64))
    sealed = nacl.bindings.crypto_box_seal(value.encode("utf-8"), public_key._public_key)
    return base64.b64encode(sealed).decode()


def put_secret(repo: str, name: str, value: str, key_data: dict, token: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"[dry-run] 将写入 {name} (len={len(value)})")
        return True
    payload = {
        "encrypted_value": encrypt(value, key_data["key"]),
        "key_id": key_data["key_id"],
    }
    status, data = api_request(
        f"{API}/repos/{repo}/actions/secrets/{name}", token, method="PUT", body=payload
    )
    if status in (201, 204):
        print(f"OK   {name} 已更新 (len={len(value)}, key_id={key_data['key_id']})")
        return True
    print(f"FAIL {name} status={status} resp={data}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="写入 GitHub 仓库级 Actions Secret")
    parser.add_argument("repo", help="owner/repo")
    parser.add_argument("name", nargs="?", help="secret 名称（单条模式）")
    parser.add_argument("value", nargs="?", help="secret 值（单条模式）")
    parser.add_argument("--json-file", help="批量模式：JSON 文件，形如 {\"NAME\": \"value\"}")
    parser.add_argument("--token-file", help="PAT 文件路径")
    parser.add_argument("--dry-run", action="store_true", help="只打印将要写入哪些项")
    args = parser.parse_args()

    if args.json_file:
        pairs = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        if not isinstance(pairs, dict):
            sys.exit("--json-file 内容必须是对象 {\"NAME\": \"value\"}")
    elif args.name and args.value is not None:
        pairs = {args.name: args.value}
    else:
        parser.error("需提供 NAME VALUE，或 --json-file")

    token = load_token(args.token_file)
    key_data = fetch_public_key(args.repo, token)

    failures = [name for name, value in pairs.items()
                if not put_secret(args.repo, name, str(value), key_data, token, args.dry_run)]
    if failures:
        print(f"失败项: {', '.join(failures)}")
        return 1
    if args.dry_run:
        print(f"[dry-run] 未写入任何 secret（共 {len(pairs)} 项待写入 {args.repo}）")
        return 0
    print(f"完成：{len(pairs)} 个 secret 已对齐 {args.repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
