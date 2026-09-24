# 代码骨架（可直接移植）

两层的可复制骨架。方括号 `<...>` 为占位符，替换成目标项目实际值。
首个落地样例参见项目级 skill `project-binance-api-tv-dashboard-rules`（同仓库），本文件只放通用骨架。

---

## 一、导出层骨架（Python）

```python
"""回测绘图数据导出：复用生产引擎记录成交 + 聚合日线 OHLCV + 日度曲线。"""
import datetime, io, json, sys, zipfile
from pathlib import Path

# ---- 0. 常量（替换为项目实际值）----
SYMBOLS     = ["<SYM1>", "<SYM2>"]
START_TIME  = "<YYYY-MM-DD> 00:00:00"
END_TIME    = "<YYYY-MM-DD> 00:00:00"
TZ_OFFSET   = 8                       # 数据源时区与本地时区的偏移
CACHE_DIR   = "<K线缓存目录>"
BASELINE    = "<基准结果 JSON 路径>"   # 既有回测结果，用于逐项对照

# ---- 1. 引入生产引擎（模块级只应有常量与类定义，且有 __main__ 保护）----
sys.path.insert(0, str(Path(__file__).resolve().parent))
import <ENGINE_MODULE> as E


class RecEngine(E.<ENGINE_CLASS>):
    """记录层：只覆写成交方法，交易逻辑一律走父类，绝不重写。"""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.events = []      # [(minute_idx, 'b'|'s', price, profit)]
        self._idx = 0         # 当前分钟索引，回放循环里更新

    def place_buy(self, time_str, price):
        n0 = self.buy_count
        super().place_buy(time_str, price)
        if self.buy_count > n0:                     # 父类可能因现金不足跳过，须比对计数
            self.events.append((self._idx, "b", price, 0.0))

    def place_sell(self, time_str, order, sell_price):
        n0 = self.sell_count
        super().place_sell(time_str, order, sell_price)
        if self.sell_count > n0:
            tr = self.completed_trades[-1]
            self.events.append((self._idx, "s", sell_price, tr["profit"]))
```

> 关键：`place_buy` 可能被父类静默跳过（金额不足/现金不足），所以必须**比对计数再记录**，
> 否则图上会出现不存在的买入点。

### 日线聚合（一遍遍历同时产出分钟价与日线 OHLCV）

```python
def load_symbol(symbol, start_dt, total_minutes):
    """返回 (分钟 open 序列, 日线 [o,h,l,c,vol] 列表)；日边界 = 本地 00:00。"""
    opens = [None] * total_minutes
    n_days = (total_minutes + 1439) // 1440
    agg = [[None] * 5 for _ in range(n_days)]

    for zip_path in sorted(Path(CACHE_DIR).glob(f"{symbol}-*.zip")):
        with zipfile.ZipFile(zip_path) as zf:
            with zf.open(zf.namelist()[0]) as f:
                for line in io.TextIOWrapper(f, encoding="utf-8"):
                    p = line.strip().split(",")
                    if len(p) < 6 or not p[0].isdigit():
                        continue
                    ms = int(p[0])
                    if ms > 10_000_000_000_000:          # 兼容微秒时间戳
                        ms //= 1000
                    # 用 fromtimestamp(ts, UTC) 而非已弃用的 utcfromtimestamp
                    dt = (datetime.datetime.fromtimestamp(ms / 1000.0, datetime.UTC)
                          + datetime.timedelta(hours=TZ_OFFSET))
                    idx = int((dt - start_dt).total_seconds() // 60)
                    if not 0 <= idx < total_minutes:
                        continue
                    o, h, l, c, v = (float(p[1]), float(p[2]), float(p[3]),
                                     float(p[4]), float(p[5]))
                    opens[idx] = o                          # 引擎用的价格口径
                    a = agg[idx // 1440]
                    if a[0] is None:
                        a[0], a[1], a[2] = o, h, l
                    else:
                        a[1] = max(a[1], h)
                        a[2] = min(a[2], l)
                    a[3] = c
                    a[4] = (a[4] or 0.0) + v
    return opens, agg
```

### 日期标签与日度曲线对齐

```python
# 日度快照口径要与引擎一致（例如每满 1440 分钟 append 一次）
days = [(start_dt + datetime.timedelta(minutes=i * 1440)).strftime("%Y-%m-%d")
        for i in range(len(nav_curve))]
trades_out = [[idx // 1440, side, round(px, 8), round(profit, 4)]
              for idx, side, px, profit in eng.events]
```

### 对照校验（不一致就必须先修导出层）

```python
ref = json.loads(Path(BASELINE).read_text(encoding="utf-8"))
all_ok = True
for sym, eng in zip(SYMBOLS, engines):
    want = ref["assets"][sym]["final_equity"]
    dev = abs(eng.equity() - want)
    ok = dev < 0.05                                   # 容差按资金量级设
    all_ok &= ok
    print(f"[对照] {sym:<10} 本脚本 {eng.equity():>10.2f} vs 基准 {want:>10.2f} "
          f"Δ{dev:+.4f} {'OK' if ok else 'FAIL'}")
print("[对照]", "全部通过" if all_ok else "存在不一致，禁止交付")
```

---

## 二、渲染层骨架（JS，v4 API）

### 蜡烛图 + 成交量 + 防负刻度

```js
var cs = chart.addCandlestickSeries({
  upColor: '#ef232a', downColor: '#14b143',                  // 中国市场：红涨绿跌
  borderUpColor: '#ef232a', borderDownColor: '#14b143',
  wickUpColor: '#ef232a', wickDownColor: '#14b143',
  priceLineVisible: false,
  autoscaleInfoProvider: function (orig) {                   // 防止价格轴延伸到负值
    var r = orig();
    if (r && r.priceRange && r.priceRange.minValue < 0) r.priceRange.minValue = 0;
    return r;
  }
});

var vol = chart.addHistogramSeries({
  priceFormat: { type: 'volume' }, priceScaleId: '',
  priceLineVisible: false, lastValueVisible: false
});
vol.priceScale().applyOptions({ scaleMargins: { top: 0.79, bottom: 0 } });
```

### 精度随标的自适应（每换标的都要设）

```js
// 注意：chart 级 localization.priceFormatter 会覆盖这里的设置，两处不要同设
var prec = lastPrice >= 1000 ? 0 : lastPrice >= 100 ? 1 : lastPrice >= 1 ? 2 : 4;
cs.applyOptions({
  priceFormat: { type: 'price', precision: prec, minMove: 1 / Math.pow(10, prec) }
});
```

### 买卖标记（时间必须命中 K 线存在的日期）

```js
cs.setMarkers(trades.map(function (t) {
  var buy = t[1] === 'b';
  return {
    time: days[t[0]],                                        // 必须是 'YYYY-MM-DD' 且存在于 K 线
    position: buy ? 'belowBar' : 'aboveBar',
    color: buy ? '#ef232a' : '#14b143',
    shape: buy ? 'arrowUp' : 'arrowDown',
    text: buy ? 'B' : (t[3] >= 0 ? '+' : '') + t[3].toFixed(1)
  };
}));
```

### 倒挂回撤图（invertScale 在 chart 级）

```js
var ddChart = LightweightCharts.createChart(el, {
  rightPriceScale: { invertScale: true, scaleMargins: { top: 0.08, bottom: 0.08 } },
  timeScale: { borderColor: '#e3e7ee' },
  layout: { background: { type: 'solid', color: '#ffffff' }, textColor: '#4b5563' }
});
ddChart.addAreaSeries({                                      // 数据传正值
  lineColor: '#e53935', topColor: 'rgba(229,57,53,.20)',
  bottomColor: 'rgba(229,57,53,.20)', priceLineVisible: false,
  priceFormat: { type: 'custom', formatter: function (p) { return p.toFixed(1) + '%'; } }
}).setData(days.map(function (d, i) { return { time: d, value: dd[i] }; }));
```

### 多图时间轴同步（加锁防死循环）

```js
var charts = [priceChart, navChart, ddChart, eqChart], lock = false;
charts.forEach(function (src) {
  src.timeScale().subscribeVisibleLogicalRangeChange(function (r) {
    if (lock || !r) return;
    lock = true;
    charts.forEach(function (dst) {
      if (dst !== src) { try { dst.timeScale().setVisibleLogicalRange(r); } catch (e) {} }
    });
    lock = false;
  });
});
```

### 单文件交付 + 深链

```js
// 构建脚本把库与数据直接内联进 HTML，保证离线可开：
//   <script id="TV_DATA" type="application/json">{...}</script>
//   <script>{轻量图表库源码}</script>
//   <script>{看板逻辑}</script>
// 初始标的从 hash 读取，切换时回写，便于分享单标的视图：
var hashSym = (location.hash || '').replace('#', '').toUpperCase();
// setSymbol 末尾：
if (window.history && history.replaceState) history.replaceState(null, '', '#' + sym);
```

---

## 三、无头验证命令

```sh
"<chrome 或 edge>" --headless=new --disable-gpu --hide-scrollbars \
  --virtual-time-budget=15000 --window-size=1560,2560 \
  --screenshot="<out.png>" "file:///<abs>/dashboard.html#<SYMBOL>"
```

- `--virtual-time-budget` 必须给足（10~15s），否则截到未渲染完的空框架。
- 截图后**用 Read 打开图片肉眼确认**：KPI 是否填充、K 线是否出现、标记是否可见、轴刻度是否正常。
- 若 CDP 自动化工具（agent-browser 等）启动挂起无输出，直接改用本命令，不要重试。
