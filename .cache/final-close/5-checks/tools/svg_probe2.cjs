const {chromium}=require('playwright');const path=require('path');const {pathToFileURL}=require('url');
(async()=>{const b=await chromium.launch({headless:true});
for(const w of [1280,390]){const p=await b.newPage({viewport:{width:w,height:900}});
for(const f of process.argv.slice(2)){await p.goto(pathToFileURL(path.resolve(f)).href,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>document.querySelectorAll("details").forEach(e=>e.open=true));
const r=await p.evaluate(()=>{const out=[];for(const svg of document.querySelectorAll('svg')){const fr=svg.getBoundingClientRect();for(const t of svg.querySelectorAll('text')){const bb=t.getBoundingClientRect();if(bb.width&&(bb.left<fr.left-.5||bb.top<fr.top-.5||bb.right>fr.right+.5||bb.bottom>fr.bottom+.5))out.push({text:t.textContent,over_right:+(bb.right-fr.right).toFixed(2),over_bottom:+(bb.bottom-fr.bottom).toFixed(2),over_left:+(fr.left-bb.left).toFixed(2),id:svg.id,used:[...document.fonts].filter(x=>x.status==='loaded').map(x=>x.family).join(',')})}}return out});
console.log(w,path.basename(f),JSON.stringify(r));}
await p.close();}
await b.close();})();
