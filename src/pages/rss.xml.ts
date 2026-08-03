import { getEditions, withBase } from '../lib/content';

const escapeXml = (value: string) => value.replace(/[<>&'\"]/g, (char) => ({
  '<': '&lt;',
  '>': '&gt;',
  '&': '&amp;',
  '\"': '&quot;',
  "'": '&apos;'
}[char] || char));

export function GET(context) {
  const editions = getEditions();
  const site = context.site || new URL('https://example.github.io/daily-brief');
  const items = editions.map((edition) => {
    const link = new URL(withBase(`/editions/${edition.date}/`), site).href;
    return `\n    <item>\n      <title>${escapeXml(`Issue ${String(edition.issue).padStart(3, '0')} · ${edition.title}`)}</title>\n      <link>${escapeXml(link)}</link>\n      <guid isPermaLink=\"true\">${escapeXml(link)}</guid>\n      <pubDate>${new Date(`${edition.date}T09:00:00Z`).toUTCString()}</pubDate>\n      <description>${escapeXml(edition.subtitle)}</description>\n    </item>`;
  }).join('');
  const xml = `<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<rss version=\"2.0\"><channel>\n  <title>The Daily Brief</title>\n  <link>${escapeXml(site.href)}</link>\n  <description>A public, source-grounded newspaper of signals, papers, essays, podcasts, and field notes.</description>${items}\n</channel></rss>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
