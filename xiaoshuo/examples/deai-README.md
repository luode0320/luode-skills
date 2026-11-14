# 二遍去味演示（de-ai-demo）

> 本文件是 `06-去AI味.md`（首版二遍改写手册）的**可运行对照说明**：
> 同一章的「首版（带 AI 味）」与「定稿（二遍去味后）」并排（`deai-before-*.md` / `deai-after-*.md`），跑一次 C11 就能看见「命中 → 清零」。

## 怎么跑

`examples/` 是平铺目录，先把三个文件复制成最小可跑的两棵树：

```powershell
$demo = Join-Path $env:TEMP 'de-ai-demo'
New-Item -ItemType Directory -Force -Path "$demo\bible", "$demo\before", "$demo\after" | Out-Null
Copy-Item examples\deai-bible-world-bible.md            "$demo\bible\world-bible.md"   # 最小 bible，仅隔离 C1–C10，让报告只显示 C11
Copy-Item examples\deai-before-第1章_穰县醒_首版.md      "$demo\before\第1章_首版.md"
Copy-Item examples\deai-after-第1章_穰县醒_定稿.md        "$demo\after\第1章_定稿.md"

# 1) 首版：应触发多类 C11 WARN
python scripts/consistency_audit.py --bible "$demo\bible" --ms "$demo\before"

# 2) 定稿：应 WARN 0（C11 清零）
python scripts/consistency_audit.py --bible "$demo\bible" --ms "$demo\after"

# 3) 用完删掉
Remove-Item -Recurse -Force $demo
```

## 预期结果（已实测）

| 版本 | ERROR | WARN | C11 命中类别 |
|---|---|---|---|
| `before/第1章_首版.md`（源：`deai-before-第1章_穰县醒_首版.md`） | 0 | 7 | 比喻连接词×3、破折号×6、情绪直给×2、说教收尾×3、信息交代开头×1、无人称感受句×2、突发转场×3 |
| `after/第1章_定稿.md`（源：`deai-after-第1章_穰县醒_定稿.md`） | 0 | 0 | 无（全部清零） |

> 注 1：本章「套路填充词」为 0，属正常——它证明探测器**不误报**：没出现的类别就不报警。
> 若想看套路填充词（不知何时/忽然/猛地…）也被抓，在 `before` 里加几句即可，阈值 `filler=3`。
> 注 2：`deai-before-*` 与 `deai-after-*` 均保留中文冒号/破折号以外的写作特征，供 C11 探测；两者用 `check_prose.py` 跑时，`deai-after-*` 已清零硬禁令（退出码 0），`deai-before-*` 仍会因冒号/破折号失败（退出码 1）——这是设计如此，首版就该被硬禁令抓住。

## before → after 改写对照（按 `06-去AI味.md` 八类范式）

| 信号 | before（AI 味） | after（去味） | 对应手册 |
|---|---|---|---|
| 信息交代开头 | 「这是一座位于南阳的小城，名叫穰县。」 | 「建安五年的第一场雪，落在穰县。」 | §2.6 从场景/动作切入 |
| 破折号 ×6 | 「陈恪——一个活在…的博士生——后一半属于陈默——南阳郡…」 | 拆成两句逗号句，零破折号 | §2.1 破折号只留必要顿挫 |
| 比喻连接词 ×3 | 「他仿佛被人从深水中捞起，又似乎落进了一场梦」 | 删连接词，直接写「深水中被捞起的那一刻」 | §2.2 落地成感官/动作 |
| 情绪直给 ×2 | 「他感到一阵茫然，一种莫名的恐惧攥住他」 | 「陈默没作声」+ 用记忆闪回外化 | §2.4 靠动作外化 |
| 无人称感受句 ×2 | 「令人心酸，让人鼻酸」 | 删「令人/让人」，给具体反应 | §2.7 情绪从具体的人长出来 |
| 突发转场 ×3 | 「突然…忽然…猛地…」 | 「邻舍柴垛塌了，一声闷响」用触发物带出 | §2.8 删预警词 |
| 说教收尾 ×3 | 「他明白…那一刻，他懂得了乱世里活着的不易」 | 结尾落「他低头看腕上勒痕，指腹摩挲眉骨旧疤」 | §2.5 用意象收尾，道理留给读者 |

## 要点

1. **探测器只探雷，不改文**：C11 把明显雷点列成清单，真正的去味是照 `06-去AI味.md` 逐条改写。
2. **先逻辑后文风**：二遍去味前，务必确认 C1–C10 已 ERROR 0（本 demo 用最小 bible 隔离了它们；正式项目请用完整 bible）。
3. **改完重跑**：去味后必须重跑全量审计，确认 C1–C10 没因改写回退、C11 已清零。
4. **阈值可调**：`C11_THRESHOLDS` 在 `scripts/consistency_audit.py` 顶部，按文风松紧微调。
