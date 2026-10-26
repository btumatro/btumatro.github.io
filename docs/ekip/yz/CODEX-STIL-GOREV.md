# Codex görevi: MATRO ekip üyeleri için stilize karakter örnekleri ve referans sayfaları

Repo: /Users/wildgenie/Projects/btu-matro. Türkçe çalış, emoji yok, commit/push YAPMA, site dosyalarına (public/, src/) DOKUNMA.
Görselleri **Gemini** çizer (`gemini-3-pro-image`, REST generateContent). Anahtar: `source ~/.zshrc >/dev/null 2>&1` sonrası `GEMINI_API_KEY`; asla yazdırma, dosyaya ya da loga yazma.

## Önceki denemede ne bozuldu (agy)
- Çizimlerin çoğu gerçek kişiden uzaklaştı: yeni yüz uydurdu.
- Karakterleri zamanla **yaşlı** çizdi. Bunlar 19-24 yaşında üniversite öğrencileri; yaşlarını fotoğraftaki gibi tut, kırışık/olgunlaştırma/kilo ekleme yok. (İstisna: Doç. Dr. Mehmet Onur Genç ve Bilgehan Zeki Özaytaç yetişkin; onlar da fotoğraftaki yaşlarında.)
- Yalnız tek bir site karesi referans verilmişti.

## Referans kuralı (zorunlu)
Her kişi için **tek bir çok turlu Gemini sohbeti** kur ve ilk turda şu referansların HEPSİNİ ver, kişiyi metinle tarif ederek:
1. Kesilmemiş orijinaller: `docs/ekip/orijinal/<slug>*.jpg` (`-canva`, `-kare`, `-yakin`, `-yuz-N`, `-bilgehan-N` vb. ekler dahil). Grup fotoğraflarında (`-grup-N` gibi) kişinin hangisi olduğunu metinle belirt ya da kırparak ver.
2. Alternatif kare: `docs/ekip/alternatif/<slug>.jpg` (varsa).
3. Site karesi: `public/media/ekip/<slug>.jpg` (yalnız okuma).
4. Gri fon stüdyo portresi: `docs/ekip/yz/codex/gri-fon/<slug>.jpg`.
5. Kabul edilmiş kadraj: `docs/ekip/yz/codex/kadraj/<slug>.jpg` (varsa).
Ardından aynı sohbette stil isteğini yap; benzemezse aynı sohbette düzeltme iste. Her çıktıyı orijinallerle yan yana koyup yüz benzerliğini ve yaşı kendin kontrol et; benzemeyeni teslim etme.

## İş 1: stil örnekleri paftası (karar için)
Kişiler: adem-baglan, irmak-karaagac, muhammed-ataman. Her kişi × 6 stil, baş-omuz, 1:1:
- a) **Zeki'nin reels sahne tarzı** (kullanıcının asıl tercihi). Ref: /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/morph_07_yakin_plan_mimik.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/01_sahne_zeki_ve_ani_masada_00_00.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/10_sahne_zeki_kisisel_itiraf_cene_elde_05_38.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/11_sahne_universiteli_ela_macbook_06_20.jpg. Grafik roman illüstrasyonu, ince mürekkep kontur, boyalı yumuşak gölge, sinematik sıcak lamba ışığı + soğuk lacivert dolgu, koyu lacivert-gri fon. Stil referanslarındaki kişiyi (kel, gözlüklü adam) KOPYALAMA; yalnız çizim dilini al.
- b) Zeki'nin karakter paftası tarzı (ref: /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/KARAKTER_KIMLIK_PAFTASI_v1.jpg): düz 2B, temiz kontur, sıcak gri-bej fon.
- c) yumuşak 3B animasyon filmi karakteri
- d) düz vektör / flat
- e) suluboya portre
- f) çizgi roman (kalın kontur, halftone)
Kişi her stilde tanınır kalmalı (yüz hatları, saç, gözlük, başörtüsü, sakal, kıyafet). Büyük göz, güzelleştirme, yaşlandırma yok.
Çıktı: `docs/ekip/yz/codex/stil-ornekleri/<harf>-<slug>.jpg`. Pafta: `docs/ekip/kontrol/stil-ornekleri.jpg` — satır = kişi (en solda orijinal fotoğraf), sütun = stil, üstte Türkçe stil adı ve harfi.

## İş 2: karakter referans sayfaları (skill'lere uygun)
Önce şu skill dosyalarını OKU ve yöntemlerini uygula (salt okunur):
- /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/pafta-taslak-sozlugu/SKILL.md (özellikle "Kimlik paftası (karakter)": önden, yandan, arkadan, üç çeyrek; nötr/gülümseyen/şaşkın ifade; tam boy; aksesuar detayı; 3x3 ızgara; değişmez özellikleri her panelde aynı yaz; düz nötr fon)
- /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/gorsel-video-uretim-cekirdek/references/karakter-urun-tutarliligi.md (altı açılı yüz paftası, 2x2 ifade, "Model sayfası" düzeni; "Use the attached image only for the character's identity")
- /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/karakter-rig-ve-avatar/SKILL.md, /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/gorsel-istem-ve-duzenleme/SKILL.md
adem-baglan ve irmak-karaagac için a) stilinde (ve karşılaştırma için b) stilinde) 3x3 kimlik paftası üret: `docs/ekip/yz/codex/karakter-sheet/<harf>-<slug>.jpg` (16:9 ya da 3:2). İstemde yaşı açıkça yaz (ör. "a 21-year-old university student"). Paftayı panel panel kontrol et: tüm panellerde aynı kişi, aynı yaş, aynı kıyafet.

## Teslim
Önce İş 1'i 1 kişiyle dene, kendin kontrol et, sonra devam. Sonunda kısa Türkçe rapor: hangi stilde benzerlik iyi/kötü, hangi skill kuralını nasıl uyguladın. Zeynep için hiçbir kadraj üretme; `docs/ekip/yz/codex/kadraj/` ve `gri-fon/` klasörlerine yazma.
