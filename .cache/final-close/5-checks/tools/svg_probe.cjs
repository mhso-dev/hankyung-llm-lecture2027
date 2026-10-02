const {chromium}=require('playwright');const path=require('path');const {pathToFileURL}=require('url');
(async()=>{const b=await chromium.launch({headless:true});const p=await b.newPage({viewport:{width:1280,height:900}});
for(const f of process.argv.slice(2)){await p.goto(pathToFileURL(path.resolve(f)).href,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
const r=await p.evaluate(()=>{const out=[];for(const svg of document.querySelectorAll('svg')){const fr=svg.getBoundingClientRect();for(const t of svg.querySelectorAll('text')){if(t.textContent.includes('자리 3')){const bb=t.getBoundingClientRect();out.push({text:t.textContent,frame:[fr.left,fr.top,fr.right,fr.bottom].map(Math.round),box:[bb.left,bb.top,bb.right,bb.bottom].map(x=>+x.toFixed(1)),font:getComputedStyle(t).fontFamily,fs:getComputedStyle(t).fontSize,anchor:t.getAttribute('text-anchor'),x:t.getAttribute('x'),vb:svg.getAttribute('viewBox'),fig:(svg.closest('figure')||{}).id||'',src:(svg.closest('figure')?.querySelector('figcaption')?.textContent||'').slice(0,60)})}}}return out});
console.log(path.basename(f),JSON.stringify(r,null,0));}
await b.close();})();
