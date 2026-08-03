export type Link = {
  label: string;
  url: string;
  kind?: string;
};

export type Item = {
  id: string;
  section: string;
  kind: 'article' | 'paper' | 'social' | 'repository' | 'podcast' | 'video' | 'special';
  kicker: string;
  title: string;
  dek: string;
  summary: string;
  deskNote: string;
  source: string;
  sourceUrl: string;
  published: string;
  status: 'checked' | 'reported' | 'contested' | 'moving' | 'thin';
  tags: string[];
  links: Link[];
  readTime?: string;
  image?: string;
};

export type Edition = {
  date: string;
  issue: number;
  title: string;
  subtitle: string;
  note: string;
  items: Item[];
};

const modules = import.meta.glob('../data/editions/*.json', {
  eager: true,
  import: 'default'
});

export function getEditions(): Edition[] {
  return Object.values(modules as Record<string, Edition>).sort((a, b) =>
    b.date.localeCompare(a.date)
  );
}

export function getEdition(date: string): Edition | undefined {
  return getEditions().find((edition) => edition.date === date);
}

export function formatDate(date: string, long = false): string {
  return new Date(`${date}T00:00:00Z`).toLocaleDateString('en-US', long
    ? { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }
    : { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
}

export function withBase(path: string): string {
  const base = import.meta.env.BASE_URL || '/';
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBase}${cleanPath}` || '/';
}

export function sourceKindLabel(kind: Item['kind']): string {
  return {
    article: 'Article',
    paper: 'Paper',
    social: 'Social',
    repository: 'Repository',
    podcast: 'Podcast',
    video: 'Video',
    special: 'Special'
  }[kind];
}
