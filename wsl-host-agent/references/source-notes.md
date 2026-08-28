# wsl-host-agent 来源记录（source-notes）

> 归属 owner：`wsl-host-agent`。记录历次调整来源，保证可回指。

## 2026-08-26 内部调整

- 来源：内部调整：`wsl-host-agent`（新建），诉求「把 Windows 挂载 WSL 项目（agent 在 Windows、项目在 WSL）的使用/编译/启动调试经验吸收到 skill 中」。
- 上游素材：
  1. 知识库笔记 `D:\谷歌云盘\知识库\20-Knowledge\开发环境\agent在Windows项目在WSL的编译启动调试经验.md`（2026-08-26 沉淀，含路线 A/B 对比）。
  2. 2026-08-26 会话实测：EllipalFinance-go 三个 v2 列表接口 URL 改名（getMainPairList→mainList 等）+ apifox 云端 endpoint/用例同步 + 真实测试 10/10 通过，全程踩坑：Windows go RLock 失败、wsl.exe chdir 失败、nohup 失效、MSYS 路径转换、shim 子进程 PATH 坑。
- 落点：SKILL.md + references/command-templates.md + workbuddy-absorption-map.md + 本文件。
- 验证：frontmatter YAML 解析通过；引用可达（知识库笔记路径存在）；同域冗余扫描 PASS。

## 历史来源

（暂无）
