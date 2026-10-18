/**
 * 启动器提示文案：由 启动组件库.bat 调用，用 node 输出 UTF-8 中文。
 * 独立成文件的原因：cmd.exe 按字节偏移逐行读批处理，bat 内一旦出现中文就会
 * 在 chcp 切换后被截断执行；把中文放在 .mjs 里可让 bat 保持纯 ASCII。
 * [用法] node scripts/launch-message.mjs <welcome|prepare|start|exit|no-node|install-failed> [退出码]
 * [返回] 退出码 0；文本打印到 stdout。
 * 最近修改时间：2026-10-17 22:35:00；改动原因：把中文提示从 bat 中抽离。
 */
const messages = {
  welcome: () => [
    '',
    '  珍珠玻璃组件库 · 本地开发服务',
    '  ----------------------------------------',
    `  目录：${process.cwd()}`,
    '',
  ],
  prepare: () => [
    '',
    '  [准备] 首次启动，正在安装依赖（npm install）...',
    '         这一步需要联网，通常 1-3 分钟，请勿关闭窗口。',
    '',
  ],
  start: () => [
    '  [启动] 正在拉起开发服务，浏览器会自动打开 http://localhost:5173',
    '         登录页任意账号密码即可进入（本地 mock 放行）。',
    '         关闭本窗口或按 Ctrl+C 即可停止服务。',
    '',
  ],
  exit: (code) => [
    '',
    `  [退出] 开发服务异常结束，退出码 ${code}。`,
  ],
  'no-node': () => [
    '',
    '  [失败] 未找到 Node.js，无法启动 Vite。',
    '         请先安装 Node.js 18 或更高版本：https://nodejs.org/',
    '',
  ],
  'install-failed': () => [
    '',
    '  [失败] 依赖安装失败，请检查网络或代理后重试。',
    '         也可在本目录手动执行：npm install',
    '',
  ],
}

const [kind, arg] = process.argv.slice(2)
const build = messages[kind]
if (!build) {
  console.error(`未知的提示类型：${kind}`)
  process.exit(1)
}
console.log(build(arg).join('\n'))
