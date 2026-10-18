#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""边角遮挡的测量体：页面内探针与登录、菜单导航等浏览器操作。

[判据] 由调用方（check_corner_occlusion.py）持有；本模块只负责在页面里取事实。
[边界] 不做任何 PASS/FAIL 裁决，只返回原始几何与样式记录。
最近修改时间：2026-10-17 12:36:00；改动原因：从裁决入口拆出测量体，
  让入口回到仓库 200 行文件基准内，拆分只做搬运，输出与拆分前逐项一致。
"""

PROBE = r"""
() => {
  const findings = []
  const px = (v) => parseFloat(v) || 0;
  const corners = ['tl', 'tr', 'bl', 'br'];
  const radiusKey = { tl: 'borderTopLeftRadius', tr: 'borderTopRightRadius', bl: 'borderBottomLeftRadius', br: 'borderBottomRightRadius' };
  const borderKey = { tl: 'borderTopWidth', tr: 'borderTopWidth', bl: 'borderBottomWidth', br: 'borderBottomWidth' };
  const radiusOf = (cs, side) => px(cs[radiusKey[side]]);
  const borderOf = (cs, side) => px(cs[borderKey[side]]);
  const paints = (cs) => {
    const bg = cs.backgroundColor || '';
    // 透明背景 + 只有边框的布局块（如 .rail-foot 的 1px 顶线）不会在角部形成色块，
    // 只有真正铺色的背景或背景图才可能盖住父级描边。
    return (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent')
      || cs.backgroundImage !== 'none';
  };
  const near = (a, b) => Math.abs(a - b) <= 1.5;
  const seen = new Set();
  const record = (item) => {
    const key = [item.parent, item.child, item.side].join('|');
    if (seen.has(key)) return;
    seen.add(key);
    findings.push(item);
  };
  for (const parent of document.querySelectorAll('*')) {
    const pcs = getComputedStyle(parent);
    const maxRadius = Math.max(...corners.map((s) => radiusOf(pcs, s)));
    if (maxRadius < 8) continue;
    const pr = parent.getBoundingClientRect();
    if (pr.width < 40 || pr.height < 40) continue;
    const maxBorder = Math.max(...corners.map((s) => borderOf(pcs, s)));
    const inner = maxRadius - maxBorder;
    // 判据一：粗描边父级的圆角内弧被直角子元素盖住（描边缺失，角部露出方角）。
    const thickBorder = maxBorder >= 3 && inner > 0;
    // 判据二：有背景的圆角父级，子元素贴角但自身圆角更小，方角直接露在父级弧外。
    const parentPaints = paints(pcs);
    if (!thickBorder && !parentPaints) continue;
    for (const child of parent.children) {
      const ccs = getComputedStyle(child);
      if (!paints(ccs)) continue;
      const cr = child.getBoundingClientRect();
      const atTop = near(cr.top, pr.top + borderOf(pcs, 'tl'));
      const atBottom = near(cr.bottom, pr.bottom - borderOf(pcs, 'bl'));
      const atLeft = near(cr.left, pr.left + borderOf(pcs, 'tl'));
      const atRight = near(cr.right, pr.right - borderOf(pcs, 'tr'));
      const sides = [];
      if (atTop && atLeft) sides.push('tl');
      if (atTop && atRight) sides.push('tr');
      if (atBottom && atLeft) sides.push('bl');
      if (atBottom && atRight) sides.push('br');
      if (!sides.length) continue;
      for (const side of sides) {
        const parentCorner = radiusOf(pcs, side);
        if (parentCorner < 8) continue;
        const childCorner = radiusOf(ccs, side);
        if (thickBorder && parentCorner >= inner && childCorner < inner) {
          record({
            kind: 'border-occluded',
            parent: String(parent.className || parent.tagName).slice(0, 60),
            child: String(child.className || child.tagName).slice(0, 60),
            side,
            need: inner,
            actual: childCorner,
          });
        } else if (!thickBorder && parentPaints && childCorner < parentCorner) {
          // 父级自身裁剪时，子元素方角会被裁到圆角以内，不会外露；只有不裁剪的父级才暴露。
          const clips = pcs.overflow === 'hidden' || pcs.overflow === 'clip';
          if (clips) continue;
          record({
            kind: 'corner-mismatch',
            parent: String(parent.className || parent.tagName).slice(0, 60),
            child: String(child.className || child.tagName).slice(0, 60),
            side,
            need: parentCorner,
            actual: childCorner,
          });
        }
      }
    }
  }
  return findings;
}
"""


def menu_labels(page):
    """读取侧栏全部子分组标签，作为逐页扫描的路由来源。"""
    return page.evaluate(
        """() => [...document.querySelectorAll('aside button, aside [role=menuitem], aside .nav-item')]
            .map((el) => el.textContent.trim())
            .filter((t) => t && t.length < 12)"""
    )


def sign_in(page, base):
    """用本地 mock 接口换 token 并写入会话存储，跳过登录页表单。

    本地 mock 的验证码固定为 1024、账号密码不校验，这里只取 token；
    用户信息用 /api/auth/me 的返回，避免手抄字段与生产结构漂移。
    """
    return page.evaluate(
        """async (base) => {
            const login = await fetch(base + '/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: 'admin', password: 'admin123', captcha: '1024', uuid: 'probe' }),
            }).then((r) => r.json())
            const me = await fetch(base + '/api/auth/me', {
                headers: { Authorization: 'Bearer ' + login.data.token },
            }).then((r) => r.json())
            const user = me.data
            localStorage.setItem('scaffold.token', login.data.token)
            localStorage.setItem('scaffold.user', JSON.stringify(user))
            localStorage.setItem('scaffold.expiresAt', String(Date.now() + login.data.expiresIn * 1000))
            return { token: Boolean(login.data.token), user: user.username }
        }""",
        base,
    )


def goto_label(page, label):
    """按标签点击侧栏项，返回是否点击成功。"""
    return page.evaluate(
        """(text) => {
            const items = [...document.querySelectorAll('aside button, aside [role=menuitem], aside .nav-item')];
            const target = items.find((e) => e.textContent.trim() === text);
            if (!target) return false;
            target.click();
            return true;
        }""",
        label,
    )
