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