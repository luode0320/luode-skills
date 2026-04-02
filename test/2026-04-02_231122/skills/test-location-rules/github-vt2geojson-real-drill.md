# `mapbox/vt2geojson` 真实遗留散落测试资产演练

## 补充文档类型

- 外部 GitHub 小项目真实迁移演练记录

## 对应的真实代码路径

- 外部仓库：`C:\Users\Administrator\.codex\playgrounds\vt2geojson-legacy-asset-drill`
- 基线对照仓库：`C:\Users\Administrator\.codex\playgrounds\vt2geojson-baseline-check`

## 补充目的

用一个真实 GitHub 小项目验证：新拆分 skill 集合不仅能在当前 skills 仓库里通过静态和动态样例验证，还能迁移外部项目里的真实遗留散落测试资产，并保持测试脚本可运行。

## 选择理由

- 目标仓库：`mapbox/vt2geojson`
- 来源：GitHub 仓库主页可直接看到根目录存在 `test.js` 和 `fixtures/`，属于典型“测试脚本与 fixture 散落在仓库根目录”的旧结构。
- commit：`57b70d7`

## 实际演练动作

1. 在外部仓库创建分支 `legacy-test-asset-drill`。
2. 创建 `test/2026-04-02_232735/真实遗留散落测试资产迁移演练/README.md`。
3. 将根目录 `test.js` 迁移到 `test/2026-04-02_232735/package-root/test.js`。
4. 将根目录 `fixtures/` 迁移到 `test/2026-04-02_232735/package-root/fixtures/`。
5. 更新 `package.json` 的 `test` 脚本路径。
6. 更新迁移后 `test.js` 中的 `require` 路径和 fixtures 路径引用。
7. 更新 CLI 示例中的旧 fixture 路径。
8. 在迁移副本中执行 `npm install` 和 `npm test`。
9. 在同一 commit 的干净基线副本中执行 `npm install` 和 `npm test` 做对照。

## 实际结果

- 迁移副本的 `npm test` 中，TAP 断言 `150/150` 全部通过。
- 干净基线副本的 `npm test` 也同样输出 TAP 全通过。
- 迁移副本与基线副本都出现 `EXIT_CODE=1`，因此该退出码不归因于本轮迁移。
- 从“散落资产归位 + 路径引用同步 + 测试可运行”三个目标看，本轮真实外部项目演练通过。

## 结论

- 新拆分 skill 集合在真实小项目上具备可执行性。
- 旧 `test-location-rules` 当前已不再是验证新 skill 集合完整性的阻断项。
- 如果只从规则内容、结构落点和真实项目迁移演练结果看，已经具备进入旧 skill 删除评估的条件。

## 残余风险

- 仍未验证生产级自动触发器中的命中优先级实现。
- 当前外部演练项目是 Node 仓库，尚未再追加 Go 项目的真实外部迁移演练。

## 与主 README 的关联说明

- 本文件是 `test/2026-04-02_231122/test-location-rules拆分对照验证/README.md` 的第四轮补充证据文档。
