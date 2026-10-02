const {chromium} = require('playwright');
const path = require('path');
const fs = require('fs');
const {pathToFileURL} = require('url');
(async () => {
  const out = path.join(__dirname, 'continuity-evidence', 'screens');
  fs.mkdirSync(out, {recursive: true});
  const chapter = path.resolve(__dirname, '../ch12-retrieval-tuning');
  const browser = await chromium.launch({headless: true});
  for (const width of [1280, 390]) {
    const page = await browser.newPage({viewport: {width, height: 900}});
    for (const name of ['08-후보-수와-리랭커-비교.html', '12-종합-튜닝과-실험-로그.html']) {
      await page.goto(pathToFileURL(path.join(chapter, name)).href);
      await page.evaluate(() => document.fonts.ready);
      const diagram = page.locator('svg').first();
      await diagram.scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(out, name.slice(0, 2) + '-' + width + '.png')});
      if (name.startsWith('12-')) {
        await page.locator('svg').nth(1).screenshot({path: path.join(out, '12-integrated-' + width + '.png')});
      }
    }
    await page.close();
  }
  await browser.close();
})();
