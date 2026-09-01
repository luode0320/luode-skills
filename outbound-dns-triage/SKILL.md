---
name: outbound-dns-triage
description: >-
  服务器"不能出网 / ping 不通域名 / curl 超时 / 容器访问上游失败"的分层排查与修复。
  核心判断：绝大多数"不能出网"其实是 DNS 解析故障，物理网络完全正常。覆盖
  境外服务器误配国内 DNS、systemd-resolved 停用导致 netplan 不写 /etc/resolv.conf、
  容器内 resolv.conf 指向 127.0.0.53 死桩三个高频根因。当用户提到"服务器不能出网"
  "ping 不通 baidu.com""网络断了""curl 失败""容器内连不上外网""DNS 解析失败"时触发。

---

# 出网故障分层排查

## 铁律 1：不要用 ping 域名判断出网状态

`ping 不通 baidu.com` 包含两种完全不同的故障：**链路断** 与 **域名解析不出**。
前者是真故障，后者是 DNS 故障但网络全通。必须先分层，禁止一上来就改路由/防火墙。

排查顺序固定为：接口 → 网关 → 公网 IP → TCP 端口 → DNS。**逐层排除，用 IP 而非域名做连通性测试**。

## 分层排查命令集

```bash
ip -br addr                          # 接口是否 UP、IP 是否正确
ip route                             # 默认路由是否存在
GW=$(ip route | awk '/default/ {print $3; exit}')
ping -c3 -W3 $GW                     # 网关（L2/L3）
ping -c3 -W3 1.2.3.4                 # 控制组：必须全丢包
ping -c3 -W3 110.242.68.4            # 公网 IP 直连（绕过 DNS）
timeout 6 bash -c 'exec 3<>/dev/tcp/110.242.68.4/80 && echo TCP80_OK'
timeout 6 bash -c 'exec 3<>/dev/tcp/1.1.1.1/443 && echo TCP443_OK'
getent hosts baidu.com               # DNS 是否解析
```

**控制组不可省略**：`ping 1.2.3.4` 若也"通"，说明网关在伪造 ICMP 应答（部分 CNAT/NAT VPS 会这样），
此时 ping 结果全部不可信，必须以 TCP 建连为准。

### 结果判读

| 现象 | 判定 |
| --- | --- |
| 网关通、公网 IP 通、TCP 通、DNS 失败 | **DNS 故障**，网络正常 |
| 网关通、公网 IP 不通 | 上游/网关/NAT 侧故障，本机无从修复，找服务商 |
| 网关不通 | 本机网络配置或虚拟网卡故障 |
| 全通但业务仍失败 | 应用或容器层问题，见"容器 127.0.0.53 死桩" |

## 根因 A：境外服务器误配国内公共 DNS

**判据**：UDP53 对国内 DNS 超时、TCP53 被 RST；对 `8.8.8.8`/`1.1.1.1` 正常。

```bash
for d in 223.5.5.5 114.114.114.114 8.8.8.8 1.1.1.1; do
  timeout 5 dig +short +time=1 +tries=1 @$d baidu.com >/dev/null 2>&1 \
    && echo "$d OK" || echo "$d FAIL"
done
```

`223.5.5.5`（阿里）、`114.114.114.114`（南京信风）**不对境外来源 IP 提供递归查询**。
服务器在中国香港/新加坡/美西时配这两个，表现为"完全不能出网"。

先确认出口归属地再选 DNS：

```bash
EG=$(dig +short @208.67.222.222 myip.opendns.com | head -1)   # 出口 IP
API=$(dig +short @8.8.8.8 ip-api.com | head -1)
curl -s -m 5 -H "Host: ip-api.com" "http://$API/json/$EG"      # 归属地
```

境外用 `1.1.1.1` + `8.8.8.8`；境内用 `223.5.5.5` + `119.29.29.29`。
**不要把不可达的 DNS 留在列表里**——每次解析都要等它超时，拖慢全部请求。

## 根因 B：systemd-resolved 停用时，netplan 不写 /etc/resolv.conf

**这是最容易踩的坑。** `systemd-resolved` 为 `disabled` 时，`netplan apply` 只把 `DNS=` 下发到
systemd-networkd 的运行时配置（`/run/systemd/network/*.network`），**不会更新 /etc/resolv.conf**。
表现：apply 返回成功，验证却仍然失败。

排查归属：

```bash
systemctl is-active systemd-resolved          # inactive 即命中
ls -la /etc/resolv.conf                       # 普通文件还是软链
lsattr /etc/resolv.conf                       # 是否有 i 属性
grep -i "^DNS=" /run/systemd/network/*.network
grep -h "resolv.conf" /var/log/cloud-init.log | tail -5    # cloud-init 是否写过
```

**修复必须双写**：netplan（持久化意图）+ `/etc/resolv.conf`（当前实际生效）。只改一处等于没改。

## 根因 C：容器内 nameserver 指向 127.0.0.53 死桩

容器创建时 Docker 会**快照**宿主的 `/etc/resolv.conf`。若当时宿主用的是 systemd-resolved 的 stub
（`nameserver 127.0.0.53`），之后 resolved 被停用，容器内这个地址就再无进程监听 → 容器解析全挂。

```bash
docker exec <c> cat /etc/resolv.conf          # 看到 127.0.0.53 即命中
ss -lntup | grep 127.0.0.53                   # 无任何监听即确认死桩
```

**`docker restart` 无效**——restart 不重建 resolv.conf。必须**重建容器**：
`docker compose up -d --force-recreate` 或 `docker rm -f <c>` 后重新 `run`。

若要一劳永逸：在 `/etc/docker/daemon.json` 写 `"dns": ["1.1.1.1","8.8.8.8"]`，
但改 daemon.json 需重启 dockerd，未开 live-restore 时会连带重启所有容器，属高危操作，需确认。

## 修复执行规范

1. **先备份**两份：`/etc/netplan/*.yaml`、`/etc/resolv.conf`。
2. **后台 + 自动回滚**：`nohup bash fix.sh >/dev/null 2>&1 & disown`。
   `netplan apply` 有闪断风险，SSH 若中断，脚本仍能在服务器本地完成回滚。
3. **脚本内自校验**：`netplan generate`（语法）→ `netplan apply` → `sleep` → 验证解析 →
   失败立即回滚并重新 apply。**验证项要包含"resolv.conf 未被 netplan 覆写"**。
4. 用 `sed` 精确改 netplan 的 IP 行，不要整文件重写，避免破坏 YAML 缩进。
5. 改 DNS 属于配置替换，执行前须声明目标服务器并向用户确认影响范围。

## 验证清单

```bash
getent hosts baidu.com && ping -c3 -W3 baidu.com
curl -s -m 8 -o /dev/null -w "%{http_code}\n" https://www.baidu.com
getent hosts archive.ubuntu.com                       # apt 源
docker exec <c> getent hosts baidu.com 2>/dev/null || echo "容器需重建才生效"
```

## 次生检查

- **IPv6 不通但解析返回 AAAA**：`getent` 优先 IPv6 时 apt 会卡顿。
  用 `dig +short @1.1.1.1 A <host>` 确认 A 记录存在；必要时 `Acquire::ForceIPv4=true`。
- **ping 首包丢失**：首包常在解析完成瞬间发出而被丢，2/3 收到属正常，不必处理。
- **netplan 文件权限告警**：`Permissions ... too open` 不影响功能，可 `chmod 600` 消除。
