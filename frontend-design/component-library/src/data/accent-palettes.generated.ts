/* 由 frontend-design/scripts/build_accent_palette.py 从 references/accent-palettes.json 生成。
   禁止手改：加色板请改 JSON 后重跑脚本。 */

export interface AccentPalette {
  key: string
  label: string
}

export const ACCENT_PALETTES: AccentPalette[] = [
  { key: 'blue', label: '珍珠蓝' },
  { key: 'teal', label: '青碧' },
  { key: 'violet', label: '丁香紫' },
  { key: 'moss', label: '苔绿' },
  { key: 'amber', label: '琥珀' },
]

export const DEFAULT_ACCENT = 'blue'
