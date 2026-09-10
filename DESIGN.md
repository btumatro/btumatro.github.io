# DESIGN.md — BTÜ MATRO görsel dil ve bileşen sözleşmesi

Amaç: yeni bir sayfa veya bileşen eklerken mevcut siteyle görsel/kod tutarlılığını korumak.
Token'lar `src/styles/global.css` içindeki `@theme` bloğunda tanımlı; burada onları nasıl
kullanacağını anlatıyoruz.

## Renk paleti

Karanlık zeminli, tek tema (site her zaman koyu — light mode yok, `color-scheme: dark`).

| Token | Değer | Kullanım |
| --- | --- | --- |
| `ink-950` | `#04070d` | Sayfa arka planı |
| `ink-900` / `ink-850` / `ink-800` | koyudan açığa | Kart/panel katmanları, header |
| `ink-700` / `ink-600` | | Border, hover zemin |
| `mist-100` | `#eef3fb` | Ana metin (başlıklar) |
| `mist-300` | `#b9c6dc` | Gövde metni |
| `mist-500` | `#8496b3` | İkincil/etiket metni |
| `volt-300..600` | camgöbeği | **Marka rengi.** CTA, link, aktif durum, vurgu glow |
| `medal-400/500` | altın sarısı | Ödül/derece, rozet ("2026 Finalisti" gibi) |
| `ember-400/500` | kırmızı | Bronz/uyarı tonları (nadiren kullanılır) |

Kural: yeni bir vurgu rengi icat etme. Marka aksiyonu → `volt`, başarı/ödül → `medal`,
tehlike/bronz → `ember`. `packageTone()`/`degreeTone()` (`src/lib/utils.ts`) bu eşlemeyi
otomatik yapar — sponsorluk paketi veya derece metni yazarken bunları kullan, renk sınıfını elle
seçme.

## Tipografi

- **Barlow** (`--font-display`) — BTÜ kurumsal kimlik fontu, sadece başlıklarda (`h1`-`h3`
  civarı, `font-display` sınıfı gerekmiyorsa bile Section/PageHero başlıkları bunu kullanıyor).
- **Inter Variable** (`--font-sans`) — gövde metni, varsayılan `body` fontu.
- **JetBrains Mono Variable** (`--font-mono`) — etiketler, rakamlar, "eyebrow" metinler
  (`font-mono text-[0.65rem] tracking-[0.2em] uppercase` kalıbı sitede çok tekrar eder).

Üç fontu da `@fontsource*` paketleriyle self-host ediyoruz — CDN'e çıkma.

## Yerleşim iskeleti

- `container-matro` — sayfa genişliği sınırlayıcı (global.css'de tanımlı), her section bunu
  kullanır.
- `Section.astro` — `eyebrow` + `title` + opsiyonel `description`, standart üst boşluk. Yeni bir
  içerik bloğu eklerken çıplak `<section>` yazma, `Section`'ı kullan.
- `PageHero.astro` — her alt sayfanın en üstündeki büyük başlık alanı.
- `CtaBand.astro` — sayfa sonu çağrı kutusu; `<slot />` destekler (ör. `BasvuruButonlari` içine
  geçirilebilir).
- `.card` / `.card-hover` — koyu panel, `rounded-2xl border border-white/10`; hover'da hafif
  yükselme. Yeni bir kutu tasarlarken bu sınıftan başla.
- `.reveal` (+ `data-delay`) — scroll'da fade/slide-in. Listelerde `data-delay={i * 50}` gibi
  kademeli gecikme ver.
- `grid-bg` — noktalı/gridli arka plan deseni, hero ve boş-durum kutularında kullanılır.

## Görsel bileşenleri

### `MediaGaleri.astro` (yeni, çoklu görsel desteği)

Tek görevi: bir `cover` + opsiyonel `gallery: string[]` alıp, tek görsel varsa düz `<img>`,
birden fazla varsa kapağın altında tıklanabilir küçük resim şeridi basmak. **Tüm çoklu görsel
ihtiyaçları bu bileşenden geçmeli** — kendi thumbnail/lightbox mantığını yazma.

```astro
<MediaGaleri
  cover={team.data.image}
  gallery={team.data.gallery}
  alt={`${team.data.title} takımı`}
  imgClass="aspect-[16/9] w-full rounded-2xl border border-white/10 object-cover"
/>
```

İki yerleşim modu var:

- **Sabit oranlı, blok akışı** (varsayılan, `stretch` verilmez) — takım detay sayfasındaki gibi
  ortalanmış, sabit `aspect-[…]` ile. `imgClass` boyutu tamamen belirler.
- **`stretch` (grid hücresini doldur)** — haber/faaliyet kartlarındaki gibi, sarmalayıcı
  `flex h-full flex-col` olur, `imgClass`'a `flex-1` eklenir; ana görsel kalan tüm yüksekliği
  kaplar, şerit varsa altına oturur. Bunu yalnızca ebeveyn zaten bir grid/flex ile yükseklik
  veriyorsa kullan (aksi halde `flex-1` hiçbir şeye büyümez).

Diğer prop'lar: `placeholderLabel` (görsel yoksa gösterilecek metin — haber tipi gibi),
`renderEmpty={false}` (görsel yoksa hiçbir şey basma; takım detay sayfası bunu kullanıyor çünkü
görsel yoksa orada boşluk bırakmak istemiyoruz).

Tıklama mantığı tek bir global `<script>` ile event delegation üzerinden çalışır — sayfada kaç
tane `MediaGaleri` olursa olsun ek JS yükü olmaz. Yeni bir kullanım eklerken script'e dokunmana
gerek yok.

### `FotoSerit.astro`

Galeri verisinden (`src/data/gallery.json`) beslenen, sayfa altına konan yatay foto şeridi
(hakkımızda, ekibimiz, bize katılın, iletişim sayfalarında kullanılıyor). `MediaGaleri`'den
farkı: tek bir içeriğin görselleri değil, tüm siteden **kategoriye göre filtrelenmiş** bir
seçki gösterir ve tıklayınca `/galeri` sayfasına götürür (büyütme yapmaz).

```astro
<FotoSerit categories={['Yarışma']} limit={6} class="mt-10" />
```

### `TeamCard.astro`

Takım listesi kartı — kapak, kategori rozeti, `badge` (ör. "2026 Finalisti"), `isNew` durumu,
odak alanları (ilk 3). Bu kartın **kendi galerisi yok** — liste görünümünde tek kapak yeterli,
çoklu görsel yalnızca detay sayfasında (`MediaGaleri` ile) gösterilir.

### `BasvuruButonlari.astro`

`src/data/join.json`'daki `applications[]` dizisinden beslenir. `variant="kart"` (açıklamalı,
Bize Katılın sayfası) veya `variant="satir"` (yalnızca buton, CTA bantları/iletişim). Yeni bir
başvuru formu eklerken bu bileşene dokunma — sadece JSON'a ekle, her yerde otomatik çıkar.

## Görsel oranları — hangi bağlamda ne kullanılır

| Bağlam | Oran/sınıf |
| --- | --- |
| Takım/haber/faaliyet kartı (liste) | `aspect-[16/9]` (TeamCard) veya `stretch` + grid hücresi (haber/faaliyet) |
| Takım detay kapak görseli | `aspect-[16/9]`, `max-w-3xl`, `rounded-2xl` |
| Sponsor logosu | kare, `rounded-full`, `h-20 w-20` (dairesel rozet — `crop-sponsor-logos.mjs` çıktısı zaten kare+saydam) |
| Galeri şeridi kareleri (`FotoSerit`) | `aspect-square` |
| `MediaGaleri` küçük resim | `h-12 w-16` (sabit, oranı önemli değil, `object-cover`) |

## Yeni bir içerik türüne görsel eklerken

1. Görseli `public/media/` altına, isim deseni `takim-…` / `haber-…` / `galeri-…` /
   `sponsor-…` / `logolar/…` ile koy (var olan adlandırmayı takip et).
2. `sharp` ile optimize et (bkz. AGENTS.md → Görsel kuralları).
3. Frontmatter'da `image` (kapak) ve varsa `gallery: [...]` alanlarını doldur — ekstra
   markup/bileşen yazmana gerek yok, sayfalar zaten `MediaGaleri`'yi çağırıyor.
4. `.pages.yml`'de karşılık gelen alan zaten tanımlı (`image` + `gallery` üç koleksiyonda da
   var); yeni bir koleksiyon eklersen aynı ikiliyi oraya da ekle.
