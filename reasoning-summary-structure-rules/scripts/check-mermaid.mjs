import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

// NODE_PATH 对 ESM 的 import 不生效，所以按顺序探测已知位置，用 createRequire 解析 CJS 的 jsdom
const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.dirname(here); // scripts/ 的上一级，即 skill 根目录
const SEARCH_ROOTS = [
  process.cwd(),
  skillRoot,
  here
];

let JSDOM = null;
for (const root of SEARCH_ROOTS) {
  for (const base of [root, path.join(root, 'node_modules')]) {
    try {
      JSDOM = require(require.resolve('jsdom', { paths: [base] })).JSDOM;
      break;
    } catch { /* 继续探测下一个位置 */ }
  }
  if (JSDOM) break;
}
if (!JSDOM) {
  try { ({ JSDOM } = await import('jsdom')); } catch { /* 落到下面的报错 */ }
}
if (!JSDOM) {
  console.log(`找不到 jsdom。先装依赖：npm install jsdom --prefix "${skillRoot}"`);
  process.exit(1);
}

const target = process.argv[2];
const vendor = process.argv[3] || path.join(path.dirname(target), 'mermaid.min.js');

const html = fs.readFileSync(target, 'utf8');
const htmlBlocks = [...html.matchAll(/<pre class="mermaid"[^>]*>([\s\S]*?)<\/pre>/g)].map(m => m[1]);
const mdBlocks = [...html.matchAll(/```mermaid\n([\s\S]*?)```/g)].map(m => m[1]);
const blocks = [...htmlBlocks, ...mdBlocks];

if (blocks.length === 0) {
  console.log('没有找到 mermaid 代码块');
  process.exit(1);
}
if (!fs.existsSync(vendor)) {
  console.log(`找不到 mermaid 库: ${vendor}`);
  process.exit(1);
}

const dom = new JSDOM(
  '<!DOCTYPE html><body><div id="host"></div></body>',
  { runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/' }
);

dom.window.structuredClone ??= (v) => structuredClone(v);

const script = dom.window.document.createElement('script');
script.textContent = fs.readFileSync(vendor, 'utf8');
dom.window.document.body.appendChild(script);

const mermaid = dom.window.mermaid;
if (!mermaid) {
  console.log('mermaid 库加载失败');
  process.exit(1);
}

mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

let fail = 0;
for (let i = 0; i < blocks.length; i++) {
  const code = blocks[i].trim();
  const kind = code.split('\n')[0].trim();
  try {
    await mermaid.parse(code);
    console.log(`  图 ${i + 1}  [${kind}]  OK`);
  } catch (e) {
    fail++;
    console.log(`  图 ${i + 1}  [${kind}]  FAIL -> ${String(e.message).split('\n').slice(0, 5).join(' | ')}`);
  }
}
console.log(fail === 0
  ? `\n${blocks.length} 张图全部通过语法校验`
  : `\n${fail} / ${blocks.length} 张图有语法错误`);
process.exit(fail === 0 ? 0 : 1);