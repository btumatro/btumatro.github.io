/**
 * Görsel açıklamalarının tek kaynağı: `src/data/gallery.json`.
 *
 * Galeriye açıklamasıyla eklenen bir görsel sitenin başka bir yerinde (takım, haber,
 * faaliyet sayfası, ana sayfa, önizleme) kullanıldığında alt metni ve önizleme
 * açıklaması otomatik olarak buradan gelir. Galeride olmayan görsellerde sayfanın
 * verdiği yedek metin kullanılır.
 */
import galeri from '../data/gallery.json';

const aciklamalar = new Map<string, string>();
for (const g of galeri.images as { image: string; caption?: string }[]) {
  if (g.image && g.caption?.trim()) aciklamalar.set(yolAnahtari(g.image), g.caption.trim());
}

/** "/media/x.jpg", "media/x.jpg" ve tam adres aynı anahtara iner. */
function yolAnahtari(yol: string): string {
  const temiz = yol.split('?')[0].split('#')[0];
  const i = temiz.indexOf('/media/');
  return i >= 0 ? temiz.slice(i) : temiz.startsWith('media/') ? `/${temiz}` : temiz;
}

/** Görselin galerideki açıklaması; yoksa yedek metin. */
export function gorselAciklama(yol?: string | null, yedek = ''): string {
  if (!yol) return yedek;
  return aciklamalar.get(yolAnahtari(yol)) ?? yedek;
}
