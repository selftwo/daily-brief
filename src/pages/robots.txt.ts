import { withBase } from '../lib/content';

export function GET(context) {
  const site = context.site || new URL('https://example.github.io/daily-brief');
  const sitemap = new URL(withBase('/sitemap-index.xml'), site).href;
  return new Response(`User-agent: *\nAllow: /\n\nSitemap: ${sitemap}\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
}
