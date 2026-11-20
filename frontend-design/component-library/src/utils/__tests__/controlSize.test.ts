import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { CONTROL_SIZES, controlSizeAttr, controlVars, isControlSize, normalizeControlSize } from '../controlSize.ts'

const SRC = new URL('../../', import.meta.url)
const readStyle = (name: string) => readFileSync(new URL(`styles/${name}`, SRC), 'utf8')
const STYLE_SOURCE = readStyle('tokens.css') + readStyle('overrides.css')

test('controlVars 只产出 var 引用，不内联像素数字', () => {
  const vars = controlVars('sm')
  assert.deepEqual(Object.keys(vars).sort(), ['--ctl-fs', '--ctl-h', '--ctl-icon', '--ctl-px'])
  for (const value of Object.values(vars)) {
    assert.match(value, /^var\(--[a-z-]+\)$/)
    assert.doesNotMatch(value, /\d+px/)
  }
})

test('四档生成的令牌名在样式层里真实存在（映射闭合）', () => {
  for (const size of CONTROL_SIZES) {
    const vars = controlVars(size)
    for (const [name, value] of Object.entries(vars)) {
      const token = value.slice(4, -1)
      assert.match(
        STYLE_SOURCE,
        new RegExp(`${token}\\s*:`),
        `${size} 档的 ${name} 指向 ${token}，但样式层未定义该令牌`
      )
    }
  }
})

test('md 档别名到上游 --control-h，引入后不产生位移', () => {
  assert.equal(controlVars('md')['--ctl-h'], 'var(--control-h-md)')
  assert.match(STYLE_SOURCE, /--control-h-md:\s*var\(--control-h\)/)
})

test('非法档位一律回落 md，不把空引用写进样式', () => {
  for (const bad of [undefined, null, '', 'huge', 'MD', 3, {}] as unknown[]) {
    assert.equal(normalizeControlSize(bad), 'md')
    assert.equal(controlVars(bad)['--ctl-h'], 'var(--control-h-md)')
  }
})

test('isControlSize 只接受四档字面量', () => {
  for (const size of CONTROL_SIZES) assert.equal(isControlSize(size), true)
  for (const bad of ['MD', 'xsmall', '', undefined, 0]) assert.equal(isControlSize(bad), false)
})

test('controlSizeAttr 输出可直接绑定的属性对象', () => {
  assert.deepEqual(controlSizeAttr('lg'), { 'data-size': 'lg' })
  assert.deepEqual(controlSizeAttr('nope'), { 'data-size': 'md' })
})
