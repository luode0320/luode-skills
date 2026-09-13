# Apple 流体交互设计参考

> 本文件吸收了 `apple-design`（个人开发者市场 skill）的精华，提炼苹果 WWDC 流体交互设计思想，供 frontend-design 在设计评审与实现时参考。

## 弹簧物理参数

### 核心概念

| 参数 | 说明 | 含义 |
|------|------|------|
| 阻尼比 (damping ratio) | 控制过冲弹跳程度 | 1.0 = 临界阻尼（无弹跳）；<1 = 产生弹跳震荡，数值越小弹跳越强 |
| 响应时间 (response) | 物体趋近目标的速度，秒 | 不是固定动画时长—弹簧无固定时长，数值越小趋近越快 |

### Apple 官方交互参数

| 交互类型 | 阻尼比 | 响应时间(s) |
|---------|--------|------------|
| 移动/画中画 | 1.0 | 0.4 |
| 旋转动画 | 0.8 | 0.4 |
| 抽屉/底部弹窗 sheet | 0.8 | 0.3 |

### Web 映射到 Motion / Framer-Motion

- 默认普通 UI：`damping=1.0`（临界阻尼，无弹跳）
- 手势抛动/轻扫：`damping≈0.8`，少量弹跳，仅在手势带有动量时使用

### 速度移交公式

```
相对速度 = 手势释放速度 / (目标值 − 当前值)
```

> Framer-Motion / Motion 支持直接传入 px/s 绝对速度，不需要手动归一化。

### 动量投射公式（苹果官方）

```js
// decelerationRate: 0.998 普通滚动; 0.99 更干脆
function project(initialVelocity, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}
const projectedEndpoint = currentPosition + project(releaseVelocity);
const target = 最近吸附点(projectedEndpoint);
```

## 毛玻璃材质配方

### 标准工具栏毛玻璃

```css
.toolbar {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  border-top: 1px solid rgba(255, 255, 255, 0.4);
}
```

### 关键参数

- `backdrop-filter: blur(20px) saturate(180%)` — 标准毛玻璃效果
- 背景色使用半透明值（`rgba(255,255,255,0.6)` 或按需调整透明度）
- 顶部/底部边框用半透明白色高光线（`rgba(255,255,255,0.4)`）增加层次感
- 深色模式：背景色替换为 `rgba(0,0,0,0.6)`，边框用 `rgba(255,255,255,0.1)`

## 无障碍动效降级方案

### CSS 媒体查询适配

```css
/* 减弱动效：降级为简单淡入淡出，禁用弹簧弹跳和位移 */
@media (prefers-reduced-motion: reduce) {
  .sheet {
    transition: opacity 200ms ease;
    transform: none !important;
  }
  /* 禁用弹簧动画，改为 transition */
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* 降低透明度：移除毛玻璃，降级为纯色背景 */
@media (prefers-reduced-transparency: reduce) {
  .toolbar {
    background: white;
    backdrop-filter: none;
  }
  /* 暗色模式 */
  @media (prefers-color-scheme: dark) {
    .toolbar {
      background: #1c1c1e;
    }
  }
}
```

### 适配原则

- 仅当 `prefers-reduced-motion: reduce` 时降级，不默认禁用动效
- 降级后保留核心功能语义（如打开/关闭仍然可见，但无弹跳）
- 毛玻璃降级为纯色背景后保证对比度达标

## 八大设计原则校验清单

| # | 原则 | 检查要点 |
|---|------|---------|
| 1 | 目的性 | 每个交互元素是否有明确目的？是否服务于用户任务？ |
| 2 | 用户控制权 | 用户是否能随时中断、撤销、重做？动画是否可打断？ |
| 3 | 责任 | 系统行为是否可预测？有无意外副作用？ |
| 4 | 熟悉感 | 交互模式是否遵循用户已有的心智模型？ |
| 5 | 灵活性 | 是否支持多种交互方式（点击/拖拽/键盘）？ |
| 6 | 简洁 | 是否有不必要的复杂交互？能否进一步简化？ |
| 7 | 工艺 | 细节是否打磨到位？动效/间距/对齐是否精确？ |
| 8 | 愉悦感 | 交互是否带来使用上的愉悦而非仅仅是功能完成？ |

## 核心交互校验清单（UI 评审用）

- [ ] **按下即反馈**：触摸/点击瞬间有视觉反馈，不在抬起后才响应
- [ ] **拖拽 1:1 跟随**：拖拽对象精确跟随手指或光标，尊重抓取偏移
- [ ] **动画可打断**：动画随时可中断，从屏幕实时位置开始新动画，不跳回起点
- [ ] **弹簧替代 transition**：使用弹簧物理驱动而非固定时长 transition
- [ ] **动量投射**：手势释放时移交原始速度，根据动量投射计算吸附点
- [ ] **橡胶边界**：到达边界时使用弹性缓冲，而非硬截断
- [ ] **路径对称**：入场与出场路径对称，弹窗从触发源弹出

## 流体交互核心思想

> 当界面对齐人的思考与运动方式，就不再像一台计算机，而是无缝的延伸。

- **即时响应**：操作瞬间得到反馈，消除等待感
- **连续运动**：位置和状态变化通过连续动画过渡，不跳跃
- **携带动量**：手势释放后动画继承手势的剩余速度
- **边界阻力**：到达边界时模拟物理弹性，克制但可感知
- **可打断**：运动过程随时可被新的交互中断并重定向