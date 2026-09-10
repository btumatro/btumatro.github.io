/**
 * Site kök adresini (base path) hesaba katan bağlantı üretici.
 * GitHub Pages alt klasörde de, kendi alan adında da doğru çalışır.
 */
export function url(path = '/'): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, '');
  const clean = path.startsWith('/') ? path : `/${path}`;
  return `${base}${clean}` || '/';
}

/**
 * CMS'ten gelen görsel yolunu çözer. Boşsa null döner ki
 * bileşenler yer tutucu gösterebilsin.
 */
export function media(path?: string | null): string | null {
  if (!path || !path.trim()) return null;
  const p = path.trim();
  if (/^https?:\/\//i.test(p)) return p;
  return url(p);
}

export interface NavItem {
  label: string;
  href: string;
  children?: { label: string; href: string; description?: string }[];
}

/**
 * Üst menü. `children` verilen öğe açılır menü olur; ana bağlantı yine
 * kendi sayfasına gider, alt bağlantılar menüde listelenir.
 */
export const NAV: NavItem[] = [
  {
    label: 'Topluluk',
    href: '/hakkimizda',
    children: [
      { label: 'Hakkımızda', href: '/hakkimizda', description: 'Biz kimiz, vizyon, misyon, tarihçe' },
      { label: 'Ekibimiz', href: '/ekibimiz', description: 'Yönetim kurulu ve ekipler' },
      { label: 'Faaliyetlerimiz', href: '/faaliyetlerimiz', description: 'Eğitimler, geziler, sosyal sorumluluk' },
      { label: 'Galeri', href: '/galeri', description: 'Atölye ve yarışmalardan kareler' },
    ],
  },
  { label: 'Takımlarımız', href: '/takimlarimiz' },
  { label: 'Başarılarımız', href: '/basarilarimiz' },
  { label: 'Haberler', href: '/haberler' },
  { label: 'Sponsorluk', href: '/sponsorluk' },
  { label: 'İletişim', href: '/iletisim' },
];

/** Alt bilgideki düz site haritası. */
export const FOOTER_LINKS = [
  { label: 'Hakkımızda', href: '/hakkimizda' },
  { label: 'Ekibimiz', href: '/ekibimiz' },
  { label: 'Takımlarımız', href: '/takimlarimiz' },
  { label: 'Başarılarımız', href: '/basarilarimiz' },
  { label: 'Faaliyetlerimiz', href: '/faaliyetlerimiz' },
  { label: 'Haberler', href: '/haberler' },
  { label: 'Sponsorluk', href: '/sponsorluk' },
  { label: 'Galeri', href: '/galeri' },
  { label: 'Bize Katılın', href: '/bize-katilin' },
  { label: 'İletişim', href: '/iletisim' },
] as const;

/**
 * Haber ve duyuruları yeniden eskiye sıralar; taslakları eler.
 * `pinned` olanlar anasayfa şeridinde gösterilir, `expiresOn` geçince düşer.
 */
export function publishedNews<
  T extends { data: { draft: boolean; expiresOn: string; date: Date; pinned: boolean } },
>(entries: T[], opts: { onlyPinned?: boolean } = {}): T[] {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return entries
    .filter((e) => {
      if (e.data.draft) return false;
      if (opts.onlyPinned && !e.data.pinned) return false;
      const until = e.data.expiresOn?.trim();
      if (!until) return true;
      const end = new Date(until);
      return Number.isNaN(end.getTime()) ? true : end >= today;
    })
    .sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export interface AchievementRecord {
  year: number;
  competition: string;
  degree: string;
}

/** Başarı ekranlarında kullanılan ortak sayaç özeti. */
export function achievementSummary(items: AchievementRecord[]) {
  const years = items.map((item) => item.year);
  return {
    records: items.length,
    firstPlaces: items.filter((item) => /(^|[^0-9])1\./.test(item.degree)).length,
    finalists2026: items.filter((item) => item.year === 2026 && /finalist/i.test(item.degree)).length,
    international: items.filter((item) =>
      /dünya|singapore|france|nasa|italian|uluslararası|bölge/i.test(`${item.competition} ${item.degree}`),
    ).length,
    firstYear: Math.min(...years),
    lastYear: Math.max(...years),
  };
}

/** Sponsorluk paketine göre renk sınıfı */
export function packageTone(name: string): { ring: string; text: string; bg: string } {
  const n = name.toLocaleLowerCase('tr');
  if (n.includes('ana') || n.includes('platin'))
    return { ring: 'border-volt-400/45', text: 'text-volt-300', bg: 'bg-volt-400/10' };
  if (n.includes('altın'))
    return { ring: 'border-medal-400/45', text: 'text-medal-400', bg: 'bg-medal-400/10' };
  if (n.includes('gümüş'))
    return { ring: 'border-mist-300/35', text: 'text-mist-300', bg: 'bg-mist-300/10' };
  if (n.includes('bronz'))
    return { ring: 'border-ember-400/35', text: 'text-ember-400', bg: 'bg-ember-400/10' };
  return { ring: 'border-white/12', text: 'text-mist-500', bg: 'bg-white/5' };
}

/** Dereceyi madalya rengine eşler (1./2./3. ve özel ödüller) */
export function degreeTone(degree: string): string {
  const d = degree.toLocaleLowerCase('tr');
  if (d.includes('1.')) return 'text-medal-400';
  if (d.includes('2.') || d.includes('3.')) return 'text-mist-100';
  if (d.includes('ödül')) return 'text-volt-300';
  return 'text-mist-300';
}

/**
 * Instagram kullanıcı adını tam adrese çevirir.
 * "@btu_matris", "btu_matris" ve tam adres — üçü de kabul edilir.
 */
export function instagramUrl(handle?: string | null): string | null {
  if (!handle || !handle.trim()) return null;
  const h = handle.trim();
  if (/^https?:\/\//i.test(h)) return h;
  return `https://www.instagram.com/${h.replace(/^@/, '')}/`;
}

/**
 * Takım adı → takım sayfası eşlemesi.
 *
 * Başarı listesinde ve haberlerde geçen takım adları (LODOS, MATROVER, PRUSA…)
 * her zaman takım sayfasının başlığıyla birebir aynı olmuyor. Bu yüzden her
 * takımın frontmatter'ındaki `aliases` alanı da eşlemeye dahil edilir; böylece
 * yeni bir alt takım eklendiğinde koda dokunmadan panelden tanımlanabilir.
 */
export function teamIndex(
  teams: { id: string; data: { title: string; aliases?: string[] } }[]
): Map<string, string> {
  const index = new Map<string, string>();
  const key = (s: string) => s.trim().toLocaleLowerCase('tr');
  for (const t of teams) {
    index.set(key(t.data.title), t.id);
    for (const a of t.data.aliases ?? []) if (a.trim()) index.set(key(a), t.id);
  }
  return index;
}

/** Takım adına karşılık gelen sayfa yolu; eşleşme yoksa null. */
export function teamHref(index: Map<string, string>, name?: string | null): string | null {
  if (!name || !name.trim()) return null;
  const slug = index.get(name.trim().toLocaleLowerCase('tr'));
  return slug ? url(`/takimlarimiz/${slug}`) : null;
}
