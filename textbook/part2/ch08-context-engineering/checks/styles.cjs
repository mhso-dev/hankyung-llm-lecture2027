// 외부 리소스가 초기 CSS와 본문 표시를 막지 않는지 검사합니다.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const reports = [];
for (const name of fs.readdirSync(root).filter(n => n.endsWith('.html'))) {
  const html = fs.readFileSync(path.join(root, name), 'utf8');
  const head = html.match(/<head>([\s\S]*?)<\/head>/)[1];
  const css = head.match(/<style id="chapter-styles">([\s\S]*?)<\/style>/)[1];
  assert(css.includes('body{margin:0;background:var(--ivory)'));
  assert(css.includes('.page{max-width:var(--max-width)'));
  assert(css.includes('@media (max-width:640px)'));
  assert(!/<script\b[^>]*\bsrc\s*=/i.test(head), name);
  assert(!/<link\b[^>]*\brel=["']stylesheet/i.test(head), name);
  assert(head.indexOf('<style') < head.indexOf('<script'), name);
  const resources = [];
  const callbacks = {};
  const sandbox = {
    window: {addEventListener: (event, callback) => { callbacks[event] = callback; }},
    document: {
      createElement: tag => ({tag}),
      head: {appendChild: node => resources.push(node)},
      querySelectorAll: () => [{sample: true}],
    },
  };
  const javascript = head.match(/<script>([\s\S]*?)<\/script>/)[1];
  vm.runInNewContext(javascript, sandbox);
  assert.equal(resources.length, 0, '초기 표시 전에 외부 요청이 없어야 합니다.');
  callbacks.load();
  assert.equal(resources.length, 2);
  const loader = resources.find(r => r.tag === 'script');
  assert.equal(loader.async, true);
  // 라이브러리가 없거나 로딩이 실패해도 초기 스타일은 자체 포함되어 있습니다.
  assert.doesNotThrow(() => loader.onload());
  let highlighted = 0;
  sandbox.hljs = sandbox.window.hljs = {highlightElement: () => highlighted++};
  loader.onload();
  assert.equal(highlighted, 1);
  assert.equal(resources.length, 3);
  reports.push({file: name, embedded_css_chars: css.length, initial_external_resources: 0, passed: true});
}
fs.writeFileSync(path.join(__dirname, 'styles-results.json'), JSON.stringify(reports, null, 2) + '\n');
console.log(`PASS: ${reports.length}개 HTML의 자체 CSS·지연 로딩·외부 라이브러리 미가용 처리`);
