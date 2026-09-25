/** Playwright browser_run_code_unsafe aracının filename alanıyla çalıştırılır.
 * Salt okunur canlı site denetimi; formları göndermez. Ekran görüntüleri yereldir.
 */
async (page) => {
  const routes = ['/', '/hakkimizda/', '/ekibimiz/', '/bize-katilin/', '/iletisim/', '/basarilarimiz/', '/faaliyetlerimiz/', '/galeri/', '/haberler/', '/sponsorluk/', '/takimlarimiz/', '/varliklar/', ...['insansiz-hava-araclari', 'hava-savunma-sistemleri', 'tarim-teknolojileri', 'ucan-araba-simulasyonu', 'kablosuz-haberlesme', 'cevre-enerji-teknolojileri', 'teknoloji-girisimciligi', 'insansiz-deniz-araci', 'insansiz-su-alti-sistemleri', 'sanayide-robotik-ve-dijital', 'su-alti-roket-sistemleri', 'suru-insansiz-hava-araci', 'insansiz-kara-araci'].map(x => '/takimlarimiz/' + x + '/')];
  const results = [];
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of routes) {
      const response = await page.goto('https://btumatro.com' + route, { waitUntil: 'load' });
      const state = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth > innerWidth,
        h1: document.querySelectorAll('h1').length,
        hiddenArticles: [...document.querySelectorAll('article')].filter(x => getComputedStyle(x).opacity === '0').length,
      }));
      results.push({ route, width, status: response.status(), ...state });
    }
  }
  return results;
};
