# Case Study：java-story-develop 本地安装源吸收（2026-08-19）

> 归属 owner：`skill-absorption-rules`。记录「先安装本地 → 分析吸收 → 删除源」模式的首次完整实操，供下次同类吸收对照。

## 背景

用户已在本地安装 `java-story-develop__skillhub`（LobeHub 包），要求：分析吸收精华、吸收完成后删除本地源、并把该工作流固化进吸收规则。

## 关键操作

1. **定位本地原文**：不再 WebFetch，直接读 `~/.workbuddy/skills/` 与 `{workspace}/` 下带 `__skillhub` 后缀的目录。两份安装（用户级 + 工作区）内容一致。
2. **拆解**：SKILL.md（1153 行）+ coding-standards.md（11 节）→ 14 条原子规则。
3. **裁决**：3 合并 / 11 保留本地或拒绝。拒绝项给理由（机制形态不迁移、与本地红线冲突、为吸收而吸收）。
4. **落盘**：按「单一可编辑资产」逐 skill 落盘，每次只动一个 SKILL.md / reference，同步挂 References 引用。
5. **删除源**：吸收确认后 `rm -rf` 用户级 + 工作区两份，删除前先校验落盘文件存在、引用链可达。
6. **登记**：`workbuddy-absorption-map.md`（裁决表）+ `source-notes.md`（来源）双登记。

## 坑与经验

- **grep -c 误报**：`grep -c "本地安装源吸收"` 返回 0，但内容实际已写入——含引号长串 + 中文可能匹配失败。改用 `Read` 复核文件内容，不要只信 grep 计数。
- **引用悬空**：编辑后「默认执行流程」第 58 行引用「第 0 步场景」，但第 0 步没写进去——编辑 new_string 与 old_string 不匹配导致部分丢失。修复：重新 Edit 补挂第 0 步，再 grep 复核。
- **删除前必校验**：吸收内容落盘 + 宿主 SKILL.md 引用链 + UTF-8 三者全过才删源，避免「删了源才发现没吸收干净」。

## 评分对照

- 落点 skill（project-memory-rules / requirement-intake-rules）本次为 reference 增补，非根文件重构；结构维度以「新增 reference 的引用链完整、UTF-8 无乱码、语义与既有规则无冲突」为通过标准。
- 效果维度：environment-probe 覆盖 Go/Java/前端三生态探测维度；workload-mode-routing 与本地极致完整性、AC-* 冻结语义显式调和；双角色自检与既有对抗式追问边界清晰。
