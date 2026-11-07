#!/usr/bin/env bash
# 全量守卫跑批：逐条执行并汇总 rc 与末行结论。
# [用途] 一次遍历所有守卫，避免逐条手工调用漏项。
# [边界] 只跑不修；失败项由调用方按输出定位。
cd "D:/谷歌云盘/luode-skills/frontend-design" || exit 1
export PYTHONUTF8=1
PY=/c/Python314/python.exe
OUT=/tmp/guard-sweep.txt
: > "$OUT"

run() {
  local name="$1"; shift
  local start=$(date +%s)
  "$@" > /tmp/one.log 2>&1
  local rc=$?
  local dur=$(( $(date +%s) - start ))
  local tail_line
  tail_line=$(grep -v '^[[:space:]]*$' /tmp/one.log | tail -1 | cut -c1-160)
  printf '%-38s rc=%-3s %4ss  %s\n' "$name" "$rc" "$dur" "$tail_line" | tee -a "$OUT"
}

# ---- 静态（不需要服务） ----
run "verify_fidelity"            python scripts/verify_fidelity.py --offline
run "fidelity_selftest"          python scripts/verify_fidelity_selftest.py
run "component_inventory"        python scripts/test_component_inventory.py
run "contracts_selftest"         python scripts/check_component_contracts.py --selftest
run "contracts"                  python scripts/check_component_contracts.py
run "component_categories"       node  scripts/check_component_categories.mjs
run "arco_parity"                python scripts/check_arco_parity.py
run "arco_component_parity"      python scripts/check_arco_component_parity.py
run "catalog_check"              node  scripts/build_component_catalog.mjs --check
run "demo_variants_check"        node  scripts/check_demo_variants.mjs
run "demo_events_check"          node  scripts/build_demo_events.mjs --check
run "a11y_wiring_selftest"       python scripts/check_a11y_wiring.py --selftest
run "a11y_wiring"                python scripts/check_a11y_wiring.py
run "font_overrides_check"       python -X utf8 -B scripts/build_font_overrides.py --check
run "accent_palettes_check"      python -X utf8 -B scripts/build_accent_palette.py --check
run "motion_overrides_check"     python -X utf8 -B scripts/build_motion_overrides.py --check
run "motion_language_selftest"   python -X utf8 -B scripts/check_motion_language.py --selftest
run "motion_language"            python -X utf8 -B scripts/check_motion_language.py
run "overlay_motion"              $PY scripts/check_overlay_motion.py
run "contrast"                   python scripts/check_contrast.py

# ---- 渲染类（需要 dev server） ----
# 注意：这一段不能与其它 Playwright 任务并发跑。实测并发时 CPU 抢占会让
# wait_for_selector(".g-cell") 在 30s 超时，报出假的「空页」失败；单独复跑即通过。
run "admin_coverage"             node  scripts/check_admin_component_coverage.mjs
run "shadow_clipping"            node  scripts/check_shadow_clipping.mjs
run "verify_keyboard"            $PY scripts/_verify_keyboard.py
run "verify_crystallize"         $PY scripts/_verify_crystallize.py
run "corner_occlusion"           $PY scripts/check_corner_occlusion.py
run "content_padding"            $PY scripts/check_content_padding.py
run "demo_style"                  $PY scripts/check_demo_style.py
run "demo_visibility"            $PY scripts/check_demo_visibility.py
run "demo_guides"                $PY scripts/check_demo_guides.py
run "demo_event_wiring"          $PY scripts/check_demo_event_wiring.py
run "demo_health_light"          $PY scripts/check_demo_health.py
run "demo_health_dark"           $PY scripts/check_demo_health.py --theme dark
run "help_tip"                   $PY scripts/check_help_tip_interaction.py

echo "=== 失败项 ===" | tee -a "$OUT"
grep "rc=[^0]" "$OUT" | grep -v "rc=0  " || echo "（无）" | tee -a "$OUT"
