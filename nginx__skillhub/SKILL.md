---
name: nginx
description: "配置 Nginx 反向代理、负载均衡、SSL/TLS 终止、静态服务与性能调优：location 匹配优先级、proxy_pass 尾斜杠语义、try_files、proxy 头、upstream 健康检查、常见配置错误、变量、gzip/缓存。适用于写/改 nginx.conf、排查 502/404/路径转发错误、配置 HTTPS 与反向代理场景。触发词：nginx、nginx 配置、反向代理、proxy_pass、location、负载均衡、upstream、ssl 证书、https 配置、502 bad gateway、404、try_files、rewrite、gzip、nginx -t、端口转发、静态文件。"
license: MIT
metadata:
  displayName: "Nginx 配置与排障"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# Nginx 配置与排障

Nginx 配置正确性与排障手册。**先走「工作流」再查「知识区」**：改配置、配代理、配 HTTPS、排障分别有固定流程；语法细节按主题索引文件深入。

## 工作流

### 改配置工作流
1. **改前备份**：复制 `nginx.conf` 与涉及的 `conf.d/*.conf` 到 `.bak`。
2. **语法检查**：`nginx -t`（每次改动必做，别依赖肉眼）。
3. **平滑重载**：`nginx -s reload`（不要 restart，避免断连）。
4. **验证**：`curl -v http://localhost/...` 看实际响应与请求路径；`nginx -T` 导出完整生效配置核对。

### 反向代理配置流程
1. 确认转发路径语义：`proxy_pass http://backend`（保留路径）vs `proxy_pass http://backend/`（替换路径）——**尾斜杠是最高频错误源**。
2. 补全代理头：`Host`、`X-Real-IP`、`X-Forwarded-For`、`X-Forwarded-Proto`。
3. 后端为多实例时建 `upstream` 块 + `keepalive 32`。
4. 验证：`curl -v` 确认后端收到的实际 URL 与预期一致。

### HTTPS 配置流程
1. 证书链完整：`ssl_certificate` 填全链（证书+中间证书），`ssl_certificate_key` 私钥权限收紧。
2. 协议裁剪：`ssl_protocols TLSv1.2 TLSv1.3`。
3. 80→443 跳转：`return 301 https://$host$request_uri;`。
4. 验证：`curl -vI https://域名` 无证书告警；`ssl_certificate_key` 文件权限 `600`。

### 502/404 排障流程
1. `502 Bad Gateway`：先 `curl -v` 后端直连是否通 → 不通则查后端服务/端口；通则查 upstream 配置与 `max_fails`。
2. `404`：确认是 Nginx 层（`error.log` 有记录）还是后端返回；Nginx 层查 `root`/`alias` 与 `try_files` 最后参数。
3. `location` 没按预期命中：对照「Location 匹配优先级」逐级核对。

## When to Use

User needs Nginx expertise — from basic server blocks to production configurations. Agent handles reverse proxy, SSL, caching, and performance tuning.

## Quick Reference

| Topic | File |
|-------|------|
| Reverse proxy patterns | `proxy.md` |
| SSL/TLS configuration | `ssl.md` |
| Performance tuning | `performance.md` |
| Common configurations | `examples.md` |

## Location Matching

- Exact `=` first, then `^~` prefix, then regex `~`/`~*`, then longest prefix
- `location /api` matches `/api`, `/api/`, `/api/anything` — prefix match
- `location = /api` only matches exactly `/api` — not `/api/`
- `location ~ \.php$` is regex, case-sensitive — `~*` for case-insensitive
- `^~` stops regex search if prefix matches — use for static files

## proxy_pass Trailing Slash

- `proxy_pass http://backend` preserves location path — `/api/users` → `/api/users`
- `proxy_pass http://backend/` replaces location path — `/api/users` → `/users`
- Common mistake: missing slash = double path — or unexpected routing
- Test with `curl -v` to see actual backend request

## try_files

- `try_files $uri $uri/ /index.html` for SPA — checks file, then dir, then fallback
- Last argument is internal redirect — or `=404` for error
- `$uri/` tries directory with index — set `index index.html`
- Don't use for proxied locations — use `proxy_pass` directly

## Proxy Headers

- `proxy_set_header Host $host` — backend sees original host, not proxy IP
- `proxy_set_header X-Real-IP $remote_addr` — client IP, not proxy
- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for` — append to chain
- `proxy_set_header X-Forwarded-Proto $scheme` — for HTTPS detection

## Upstream

- Define servers in `upstream` block — `upstream backend { server 127.0.0.1:3000; }`
- `proxy_pass http://backend` uses upstream — load balancing included
- Health checks with `max_fails` and `fail_timeout` — marks server unavailable
- `keepalive 32` for connection pooling — reduces connection overhead

## SSL/TLS

- `ssl_certificate` is full chain — cert + intermediates, not just cert
- `ssl_certificate_key` is private key — keep permissions restricted
- `ssl_protocols TLSv1.2 TLSv1.3` — disable older protocols
- `ssl_prefer_server_ciphers on` — server chooses cipher, not client

## Common Mistakes

- `nginx -t` before `nginx -s reload` — test config first
- Missing semicolon — syntax error, vague message
- `root` inside `location` — prefer in `server`, override only when needed
- `alias` vs `root` — alias replaces location, root appends location
- Variables in `if` — many things break inside if, avoid complex logic

## Variables

- `$uri` is decoded, normalized path — `/foo%20bar` becomes `/foo bar`
- `$request_uri` is original with query string — unchanged from client
- `$args` is query string — `$arg_name` for specific parameter
- `$host` from Host header — `$server_name` from config

## Performance

- `worker_processes auto` — matches CPU cores
- `worker_connections 1024` — per worker, multiply by workers for max
- `sendfile on` — kernel-level file transfer
- `gzip on` only for text — `gzip_types text/plain application/json ...`
- `gzip_min_length 1000` — small files not worth compressing

## Logging

- `access_log off` for static assets — reduces I/O
- Custom log format with `log_format` — add response time, upstream time
- `error_log` level: `debug`, `info`, `warn`, `error` — debug is verbose
- Conditional logging with `map` and `if` — skip health checks

## 适用边界

**何时用**：写/改 nginx 配置（反代/负载均衡/SSL/静态服务）、排查 502/404/路径转发/证书问题、性能调优。

**何时不用**：
- 需要可视化流量管理 / 商业 WAF 能力 → 用云厂商 LB/WAF 或 OpenResty 扩展；
- Docker 内服务编排（非 nginx 语法问题）→ 转 `docker__skillhub`、`docker-direct-deploy`；
- 服务器运维与部署流水线 → 转 `ssh-server-ops-rules`、`docker-direct-deploy`；
- 客户端浏览器侧问题（与 Nginx 无关）→ 转 `frontend-design` 等同域 skill。

## 验收清单

- [ ] 改动前已备份配置文件
- [ ] `nginx -t` 通过后才 `nginx -s reload`
- [ ] `proxy_pass` 尾斜杠语义与预期一致（curl -v 实证）
- [ ] 代理头（Host/X-Real-IP/X-Forwarded-For/Proto）已按需补齐
- [ ] HTTPS：证书全链、协议 TLSv1.2+、私钥权限 600
- [ ] 502/404 已按「排障流程」定位到根因，不是凭猜测改配置
