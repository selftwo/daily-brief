// @ts-check
import { defineConfig } from 'astro/config';

const base = process.env.BASE_PATH || '/daily-brief';
const site = process.env.SITE_URL || 'https://example.github.io/daily-brief';

export default defineConfig({
  site,
  base,
  output: 'static',
  build: { format: 'directory' },
  compressHTML: true
});
