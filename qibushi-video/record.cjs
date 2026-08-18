// Record index.html with Playwright for 106 seconds
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({
    args: ['--autoplay-policy=no-user-gesture-required', '--mute-audio'],
  });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
    recordVideo: { dir: path.join(__dirname, 'renders'), size: { width: 1920, height: 1080 } },
  });
  const page = await context.newPage();
  const fileUrl = 'file:///' + path.join(__dirname, 'index.html').replace(/\\/g, '/') + '?autoplay=true';
  console.log('Loading:', fileUrl);
  await page.goto(fileUrl);
  console.log('Recording 106s...');
  await page.waitForTimeout(106000);
  await context.close();
  await browser.close();
  console.log('Done.');
})();
