# Gemini API CLI değerlendirmesi

Google'ın google-gemini/gemini-api-cli deposu Gemini Interactions API için bir komut satırı aracı sunuyor. 27 Eylül 2026 tarihinde README, aracın hâlâ deneysel olduğunu ve üretim kullanımı için hazır olmadığını belirtiyor.

## Klip işinde olası kullanım

- GEMINI_API_KEY ortam değişkenini kullanabilir; anahtarı komut argümanına koyma.
- İstekleri göndermeden önce --dry-run ile gövdeyi ve hedefi gözden geçir.
- Uzun süren video üretiminde --async ve durum sorgulama seçenekleri var.
- Görsel/video üretimi dosya yolunu stdout'a yazar; sonraki kurgu adımı FFmpeg olabilir.

## Kullanım

CLI, görsel/video/TTS istekleri için doğrudan kullanılabilir. Komutlar, bayraklar ve model adları hızla değişebileceği için önce gemini-api --help, ilgili komutun --usage ve --schema çıktısını incele; API çağrısından önce --dry-run çalıştır ve sürümünü kaydet. Dosya çıktısını ffprobe ile doğrula, ardından sahneleri ve sesleri FFmpeg ile birleştir.

Kullanıcı ortamındaki kurulum 27 Eylül 2026'da kaynak commit 895be4d üzerinden Go ile derlenmiştir. İkili dosya ~/.local/bin/gemini-api konumundadır. API anahtarı GEMINI_API_KEY ortamından okunur; configure ile keychain'e ayrıca kaydetmek gerekmez.

Resmî kaynaklar:

- https://github.com/google-gemini/gemini-api-cli
- https://github.com/google-gemini/gemini-skills
