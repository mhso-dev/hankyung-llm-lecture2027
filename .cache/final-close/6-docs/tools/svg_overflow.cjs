// 읽기 전용 측정: visual.cjs 와 같은 순서·같은 svgBounds 식으로 넘친 양(px)을 기록 (파일 쓰기 없음)
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const root=path.resolve(process.argv[2]);const only=process.argv.slice(3);
(async()=>{const b=await chromium.launch({headless:true});
for(const width of [1280,390]){const p=await b.newPage({viewport:{width,height:900},deviceScaleFactor:1});
for(const name of fs.readdirSync(root).filter(n=>n.endsWith('.html')).sort()){
 await p.goto(pathToFileURL(path.join(root,name)).href,{waitUntil:'load',timeout:60000});
 await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>document.querySelectorAll('details').forEach(e=>e.open=true));
 if(only.length&&!only.some(o=>name.startsWith(o)))continue;
 const r=await p.evaluate(()=>{const out=[];for(const svg of document.querySelectorAll('svg')){const fr=svg.getBoundingClientRect();
  for(const t of svg.querySelectorAll('text')){const bb=t.getBoundingClientRect();if(!bb.width)continue;
   const over=Math.max(fr.left-bb.left,fr.top-bb.top,bb.right-fr.right,bb.bottom-fr.bottom);
   if(over>0)out.push({text:t.textContent.slice(0,20),over:+over.toFixed(3),side:['left','top','right','bottom'][[fr.left-bb.left,fr.top-bb.top,bb.right-fr.right,bb.bottom-fr.bottom].indexOf(over)],svgW:+fr.width.toFixed(2)});}}return out});
 console.log(width,name,JSON.stringify(r));}
await p.close();}
await b.close();})().catch(e=>{console.error(e);process.exit(1)});
