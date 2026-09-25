// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import { SITE_URL, BASE_PATH } from './site.config.mjs';

import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: SITE_URL,
  base: BASE_PATH,
  trailingSlash: 'ignore',

  // Eylül 2026'da takım sayfaları özel adlar yerine takım türüne göre adlandırıldı.
  // Eski adresler (paylaşılmış bağlantılar, arama sonuçları) yeni sayfalara yönlenir.
  redirects: {
    '/takimlarimiz/ashina-inovasyon': '/takimlarimiz/tarim-teknolojileri',
    '/takimlarimiz/ashina-h': '/takimlarimiz/hava-savunma-sistemleri',
    '/takimlarimiz/ashina': '/takimlarimiz/insansiz-hava-araclari',
    '/takimlarimiz/burkut': '/takimlarimiz/ucan-araba-simulasyonu',
    '/takimlarimiz/cagri': '/takimlarimiz/kablosuz-haberlesme',
    '/takimlarimiz/cevre-enerji': '/takimlarimiz/cevre-enerji-teknolojileri',
    '/takimlarimiz/girisimcilik': '/takimlarimiz/teknoloji-girisimciligi',
    '/takimlarimiz/insansiz-su-alti': '/takimlarimiz/insansiz-su-alti-sistemleri',
    '/takimlarimiz/su-alti-roketi': '/takimlarimiz/su-alti-roket-sistemleri',
    '/takimlarimiz/suru-iha': '/takimlarimiz/suru-insansiz-hava-araci',
    '/takimlarimiz/tika-ika': '/takimlarimiz/insansiz-kara-araci',
    '/takimlarimiz/sanayide-dijital': '/takimlarimiz/sanayide-robotik-ve-dijital',
  },

  build: {
    format: 'directory',
  },

  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [
    // /varliklar iç kullanım sayfasıdır; site haritasına ve aramalara girmez.
    sitemap({ filter: (page) => !page.includes('/varliklar') }),
  ],
});