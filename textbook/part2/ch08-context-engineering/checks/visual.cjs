const {chromium}=require('playwright');
const fs=require('fs'), path=require('path'), {pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
const reports=[];
for(const width of [1280,390]){
 const page=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});
 for(const name of fs.readdirSync(root).filter(n=>n.endsWith('.html')).sort()){
  await page.goto(pathToFileURL(path.join(root,name)).href,{waitUntil:'load',timeout:60000});
  await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>document.querySelectorAll('details').forEach(e=>e.open=true));
  const report=await page.evaluate(()=>{
   function rgb(s){return (s.match(/[\d.]+/g)||[]).map(Number)}
   function lum(c){return c.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0)}
   function bg(e){for(let p=e;p;p=p.parentElement){const c=rgb(getComputedStyle(p).backgroundColor);if(c.length>=3&&(c.length<4||c[3]===1))return c}return [255,255,255]}
   const small=[],contrast=[],clipped=[],outside=[],svgBounds=[];
   const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
   let n;
   while(n=walker.nextNode()){
    if(!n.textContent.trim())continue;const e=n.parentElement;
    if(e.closest('script,style,svg'))continue;
    const s=getComputedStyle(e);if(s.display==='none'||s.visibility==='hidden'||!e.getClientRects().length)continue;
    const sample=n.textContent.trim().slice(0,70);
    if(!e.closest('.page'))outside.push(sample);
    const supplemental=!!e.closest('code,pre,figcaption,.meta,.crumb,.file,.tag');
    const font=parseFloat(s.fontSize),min=supplemental?14:16;
    if(font<min-.01)small.push({sample,font,min});
    const c=rgb(s.color),background=bg(e);const a=lum(c),b=lum(background);const ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
    const need=font>=24||(font>=18.66&&parseInt(s.fontWeight)>=700)?3:4.5;
    if(ratio<need-.01)contrast.push({sample,ratio:+ratio.toFixed(2),color:s.color,background,need});
   }
   for(const e of document.querySelectorAll('.page *')){
    const s=getComputedStyle(e);if(!e.getClientRects().length)continue;
    if((['hidden','clip'].includes(s.overflowY)&&e.scrollHeight>e.clientHeight+1)||(['hidden','clip'].includes(s.overflowX)&&e.scrollWidth>e.clientWidth+1))clipped.push(e.outerHTML.slice(0,140));
   }
   for(const svg of document.querySelectorAll('svg')){
    const box=svg.viewBox.baseVal;
    const scale=svg.getBoundingClientRect().width/box.width;
    for(const e of svg.querySelectorAll('text')){const b=e.getBBox();if(b.x<-.5||b.y<-.5||b.x+b.width>box.width+.5||b.y+b.height>box.height+.5)svgBounds.push(e.textContent);const font=parseFloat(getComputedStyle(e).fontSize)*scale;if(font<14-.01)small.push({sample:e.textContent,font,min:14});}
   }
   return {small,contrast,clipped,outside,svgBounds,horizontal:document.documentElement.scrollWidth>innerWidth+1,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt)};
  });
  const passed=!report.horizontal&&Object.values(report).every(x=>!Array.isArray(x)||x.length===0);
  reports.push({file:name,width,passed,...report});
  if(name==='index.html'||name.startsWith('01-'))await page.screenshot({path:path.join(__dirname,`${name.replace('.html','')}-${width}.png`),fullPage:false});
 }
 await page.close();
}
await browser.close();
fs.writeFileSync(path.join(__dirname,'visual-results.json'),JSON.stringify(reports,null,2));
console.log(JSON.stringify(reports.map(r=>({file:r.file,width:r.width,pass:r.passed,small:r.small.length,contrast:r.contrast.length,clipped:r.clipped.length,outside:r.outside.length,svgBounds:r.svgBounds.length,horizontal:r.horizontal,brokenImages:r.brokenImages.length})),null,2));
if(reports.some(r=>!r.passed))process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
