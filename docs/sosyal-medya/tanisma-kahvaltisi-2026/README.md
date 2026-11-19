# Geleneksel Tanışma Kahvaltısı 2026: içerik ana dosyaları

Etkinlik: 29 Kasım 2026 Pazar, 10.30, Mahfel Lounge (yer adı yayından önce Begüm'den teyit edilecek).
Sitedeki haber: `src/content/haberler/tanisma-kahvaltisi-2026.md`.

## Klasörler

**ham/**: üretilen işlenmemiş kaynaklar. `omni-c1-sofra-kusbakisi.mp4`, `omni-c2-cay-dokme.mp4`, `omni-c3-ogrenciler-masada.mp4` Gemini Omni çekimleri (9:16, 1080p, 10 sn, yazısız). `foto-ham-4x5.jpg`, `foto-ham-16x9.jpg`, `foto-ham-9x16.jpg` Gemini görsel üretimi kahvaltı fotoğrafları (yazısız).

**katmanlar/**: Reels yazı katmanları, saydam PNG, 1080x1920. Hikâye güvenli alanı: üst 250 px, alt 340 px boş.

**ses/**: Zeki Özaytaç klon sesiyle seslendirme. `r-00..02.txt` metinler, `r-0?.mp3` ham parçalar, `reels-ses.mp3` birleştirilmiş ve temizlenmiş ses. Marka adı metinde "Matro" diye yazılır; büyük harf "MATRO" yazımı "Madro" okunuyor.

**cikti/**: teslim edilen dosyalar. Reels üç sürüm: yazılı ve seslendirmeli, yalnız seslendirmeli (yazısız), yalnız yazılı (sessiz ses izi, müzik Instagram'da eklenir). Ayrıca Instagram gönderi (4:5 ve 3:4), hikâye ve site kapağı.

**betikler/**: yeniden üretim. `omni-uret.sh` çekimleri, `katman.py` yazı katmanlarını, `birlestir.sh` ve `iki-surum.sh` Reels sürümlerini, `kur.py` ve `*.html` gönderi/hikâye görsellerini üretir. Betikler `/tmp/reels` ve `/tmp/kahvalti` çalışma klasörlerine göre yazıldı; yeniden çalıştırırken yolları güncelle.

İstemler için `PROMPTLAR.md` dosyasına bak.
