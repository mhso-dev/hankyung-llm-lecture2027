const { chromium } = require("playwright");
const path = require("path");
const { pathToFileURL } = require("url");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 390, height: 900 } });
  for (const name of ["01-대화-히스토리와-질문-재작성.html", "09-패턴-비교와-선택.html"]) {
    const target = path.resolve(__dirname, "..", name);
    await page.goto(pathToFileURL(target).href);
    const items = await page.evaluate(() => [...document.querySelectorAll("body *")]
      .map((element) => ({ tag: element.tagName, cls: element.className, width: element.getBoundingClientRect().width, scroll: element.scrollWidth, text: element.textContent.slice(0, 60) }))
      .filter((item) => item.width > innerWidth + 1 || item.scroll > innerWidth + 1)
      .sort((a, b) => Math.max(b.width, b.scroll) - Math.max(a.width, a.scroll))
      .slice(0, 12));
    console.log(name, items);
  }
  await browser.close();
})();
