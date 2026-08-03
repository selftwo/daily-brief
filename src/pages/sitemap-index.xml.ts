import { getEditions, withBase } from '../lib/content';

const escapeXml = (value: string) => value.replace(/[<>&'\"]/g, (char) => ({
  '<': '&lt;',
  '>': '&gt;',
  '&': '&amp;',
  '\"': '&quot;',
  "'": '&apos;'
}[char] || char));

export function GET(context) {
  const site = context.site || new URL('https://example.github.io/daily-brief');
  const paths = ['/', '/archive/', '/editorial-standards/', '/lifestyle/quiet-route/', ...getEditions().map((edition) => `/editions/${edition.date}/`)];
  const urls = paths.map((path) => {
    const loc = new URL(withBase(path), site).href;
    return `\n  <url><loc>${escapeXml(loc)}</loc></url>`;
  }).join('');
  const xml = `<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">${urls}\n</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
