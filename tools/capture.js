const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 800 });
  
  const htmlPath = path.join(__dirname, 'stickfigure-generator.html');
  await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`, { waitUntil: 'networkidle0' });
  
  // Wait for canvas to render
  await page.waitForSelector('#canvas');
  await new Promise(r => setTimeout(r, 1000));
  
  // Load conversation preset
  await page.evaluate(() => {
    loadPreset('conversation');
  });
  await new Promise(r => setTimeout(r, 500));
  
  // Set background to soft blue
  await page.evaluate(() => {
    setBg('#F0F4F8', '#E8EEF4');
  });
  await new Promise(r => setTimeout(r, 500));
  
  // Add text overlay
  await page.evaluate(() => {
    document.getElementById('overlayText').value = 'AI HALLUCINATION';
    document.getElementById('textColor').value = '#E53935';
    updateCanvas();
  });
  await new Promise(r => setTimeout(r, 500));
  
  // Take screenshot of just the canvas
  const canvas = await page.$('#canvas');
  const box = await canvas.boundingBox();
  
  await page.screenshot({
    path: path.join(__dirname, '..', 'output', 'sample-scene.png'),
    clip: {
      x: box.x,
      y: box.y,
      width: box.width,
      height: box.height
    }
  });
  
  console.log('Screenshot saved to output/sample-scene.png');
  
  // Also try other presets
  const presets = ['thinking', 'shocked', 'working'];
  for (const preset of presets) {
    await page.evaluate((p) => {
      loadPreset(p);
      document.getElementById('overlayText').value = '';
      document.getElementById('showThought').checked = false;
      updateCanvas();
    }, preset);
    await new Promise(r => setTimeout(r, 500));
    
    await page.screenshot({
      path: path.join(__dirname, '..', 'output', `sample-${preset}.png`),
      clip: {
        x: box.x,
        y: box.y,
        width: box.width,
        height: box.height
      }
    });
    console.log(`Screenshot saved to output/sample-${preset}.png`);
  }
  
  await browser.close();
})();
