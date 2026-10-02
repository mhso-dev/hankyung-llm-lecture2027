const {chromium}=require('playwright');const path=require('path');const {pathToFileURL}=require('url');
(async()=>{const b=await chromium.launch({headless:true});
const p=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1});
for(const f of process.argv.slice(2)){await p.goto(pathToFileURL(path.resolve(f)).href,{waitUntil:'load',timeout:60000});await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>document.querySelectorAll('details').forEach(e=>e.open=true));
const r=await p.evaluate(()=>{const out=[];for(const svg of document.querySelectorAll('svg')){const fr=svg.getBoundingClientRect();for(const t of svg.querySelectorAll('text')){if(!t.textContent.includes('자리 3'))continue;const bb=t.getBoundingClientRect();out.push({t:t.textContent.slice(0,20),svgid:svg.id,frameR:+fr.right.toFixed(3),boxR:+bb.right.toFixed(3),boxL:+bb.left.toFixed(3),frameL:+fr.left.toFixed(3),frameB:+fr.bottom.toFixed(2),boxB:+bb.bottom.toFixed(2),bw:bb.width})}}return out});
console.log(path.basename(f).slice(0,3),JSON.stringify(r));}
await b.close();})();
