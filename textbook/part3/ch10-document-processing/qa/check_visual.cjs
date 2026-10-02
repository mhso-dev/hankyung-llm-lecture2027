// 2026-09-18(09절 실습 추가): 14px 허용 목록을 공용 textbook/_notebook/visual.cjs 와 같게 맞췄다.
// 개선된 절 본문에는 노트북 블록(.nb-toolbar·.nb-prompt·복사 button·.copy-status)이 들어가고 그 글자가 14px 이다.
// 공용 visual.cjs 는 이 네 가지를 보조 글로 보아 14px 를 통과시키는데, 이 파일의 옛 목록에는 없어 개선본 9절 전부가 badSize 로 걸렸다.
const { chromium } = require('/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs'); const path = require('path');
const base = path.resolve(__dirname, '..');
(async () => {
 const browser = await chromium.launch({headless:true}); const rows=[];
 for(const width of [1280,390]) {
  const page = await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});
  for(const name of fs.readdirSync(base).filter(n=>n.endsWith('.html'))) {
   await page.goto('file://'+path.join(base,name),{waitUntil:'networkidle'});
   await page.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('details').forEach(d=>d.open=true)});
   const result=await page.evaluate(()=>{
    const visible=e=>!!(e.getClientRects().length)&&getComputedStyle(e).visibility!=='hidden';
    const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
    const lum=c=>c.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
    const blend=(a,b)=>{const t=a.length>3?a[3]:1;return a.slice(0,3).map((x,i)=>x*t+b[i]*(1-t));};
    const bg=e=>{if(!e)return [255,255,255];return blend(rgb(getComputedStyle(e).backgroundColor),bg(e.parentElement));};
    const badSize=[],badContrast=[],clipped=[],outside=[];
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    while(walker.nextNode()) {
     const n=walker.currentNode,e=n.parentElement;
     if(!n.textContent.trim()||!visible(e)||e.closest('script,style,svg'))continue;
     const st=getComputedStyle(e);const size=parseFloat(st.fontSize);
     const detail=!!e.closest('figcaption,pre,code,.file,.crumb,.meta,.tag,.no,.nb-toolbar,.nb-prompt,button,.copy-status');
     if(size<(detail?14:16)-.01)badSize.push({text:n.textContent.slice(0,70),size});
     const b=bg(e),f=blend(rgb(st.color),b);const l=[lum(f),lum(b)].sort((a,b)=>b-a);const ratio=(l[0]+.05)/(l[1]+.05);
     const large=size>=24||(size>=18.66&&Number(st.fontWeight)>=700);if(ratio<(large?3:4.5)-.01)badContrast.push({text:n.textContent.slice(0,70),ratio});
     if(!e.closest('.page'))outside.push(n.textContent.slice(0,70));
    }
    for(const e of document.querySelectorAll('body *')){if(!visible(e)||e.closest('svg'))continue;const st=getComputedStyle(e);if(['hidden','clip'].includes(st.overflowY)&&e.scrollHeight>e.clientHeight+1)clipped.push(e.tagName+':vertical');if(['hidden','clip'].includes(st.overflowX)&&e.scrollWidth>e.clientWidth+1)clipped.push(e.tagName+':horizontal');}
    const horizontal=document.documentElement.scrollWidth>innerWidth;
    return {badSize,badContrast,clipped,outside,horizontal,pass:!badSize.length&&!badContrast.length&&!clipped.length&&!outside.length&&!horizontal};
   });
   rows.push({name,width,...result});
   if(name==='index.html'||name.startsWith('02-')||name.startsWith('07-'))await page.screenshot({path:path.join(__dirname,`${width}-${name.replace('.html','.png')}`),fullPage:false});
  }
  await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'visual-results.json'),JSON.stringify(rows,null,2));
 console.log(JSON.stringify({pages:rows.length,passed:rows.filter(r=>r.pass).length,failures:rows.filter(r=>!r.pass)},null,2));
 process.exitCode=rows.every(r=>r.pass)?0:1;
})().catch(e=>{console.error(e);process.exit(1)});
