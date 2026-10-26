# Ekip görselleri: tüm üretimlerin talimat kaydı

Her görsel kümesi hangi betikle ve hangi talimatla üretildi. Betikler anahtarı ortamdan okur (`GEMINI_API_KEY`); hiçbirinde anahtar yok. Model her yerde `gemini-3-pro-image` (REST `generateContent`).

Betikler repo kökünden çalıştırılmak üzere yazıldı; çoğu tek seferlik olduğu için çıktı yolları içine gömülü.

## Claude, önceki oturum (Ekim 2026): `claude-onceki/`

| Çıktı | Betik | Not |
|---|---|---|
| `docs/ekip/stilize/ekip-*.png`, `ekip-pafta-*.jpg` (toplu ekip: vektör, animasyon, çizgi roman, suluboya) | `ekip_gorsel.py`, `toplu.py` | Tek tur; referans site kareleri ve toplu pafta. Stil metinleri `STIL` sözlüğünde |
| `docs/ekip/stilize/araclar-bant.png` | `toplu.py` | |
| `docs/ekip/stilize/portre/<slug>.jpg` (suluboya portre, ilk deneme) | `portre.py`, `portre2.py`, `duzelt.py` | `docs/ekip/orijinal/` referanslı |
| `docs/ekip/karikatur/kare-1..4.jpg` | `karikatur.py` | 4 karelik karikatür; Irmak ve Bilgehan, stilize portreler referans |
| Kişi kırpımları | `kisiler.py` | |
| `docs/ekip/yz/kadraj/`, `yz/vesikalik/` (tek tur kadraj ve vesikalık) | `yz_kare.py` | Reddedildi ve silindi (yüzler benzemedi) |
| `docs/ekip/yz/kadraj2/` (outpaint + orijinali geri yapıştırma) | `genislet.py` | Çerçeve izi yüzünden silindi |
| Kontrol paftaları | `stil_pafta.py` | |

## agy (Antigravity CLI): `agy/`

Görev metni: `docs/ekip/yz/CODEX-GOREV.md` (Ek istek 1-11). Çalıştırma: `agy --conversation 482501c3-... -p "<Ek istek N'yi uygula>" --dangerously-skip-permissions`.

| Çıktı | Betik |
|---|---|
| `docs/ekip/yz/codex/gri-fon/` (26 gri fon), silinen beyaz vesikalıklar | `codex_uret.py`, `iyilestir.py`, `uret_gri_fon_yeni.py` (Gülsiye, Melek, Nusret) |
| `docs/ekip/yz/codex/kadraj/` | `hazirla_kadraj.py`, `uret_26_kadraj_poisson.py`, `uret_ek9_8kadraj.py`, `fix_ek10_2kadraj.py`; denemeler `test_*.py` |
| `docs/ekip/yz/agy/stil-ornekleri/`, `agy/karakter-sheet/` | `uret_ek10_stil_ve_sheet.py`, `fix_ek10_13_stiller.py` |
| Paftalar | `pafta_uret.py`, `pafta_ek5.py`, `pafta_ek9.py`, `temizle_son.py` |

`agy/gemini_calls.jsonl`: agy'nin Gemini çağrı kaydı (151 satır; adım, deneme, süre ve istek metni; görsel verisi yok). Gri fon ve vesikalık sohbetlerinin tur tur istemleri burada.

## Codex: `docs/ekip/yz/CODEX-STIL-GOREV.md`

Görev yazıldı, ancak Codex üretime başlamadı (rıza kaydı istedi). Çıktısı yok.

## Claude, bu oturum: `docs/ekip/yz/claude/`

Ayrıntılar `docs/ekip/yz/claude/README.md` dosyasında; her görselin yanında `<ad>.istem.json` var.

| Çıktı | Betik ve sürüm |
|---|---|
| `claude/stil-ornekleri/tur1/` (3 kişi × 6 stil, 1. tur) | `claude/stil_uret.py`; stil örneği olarak agy çıktıları; `ilk-a-*` yaş belirtmeden ilk deneme |
| `claude/stil-ornekleri/` (güncel) | `claude/referans_uret.py` |
| `claude/referans-sayfasi/` | `claude/referans_uret.py sayfa` |
| `claude/elenen/` (değiştirilenler) | Bkz. aşağıdaki sürüm notu |

### `claude/elenen/` sürüm notu

- `elenen/stil-ornekleri-*`, `elenen/referans-sayfasi-*`: `referans_uret.py` ilk sürümü. Bilgehan'ın tarifinde "biraz kır sakal" vardı ve stil örneği olarak en çok 6 başka çizim veriliyordu.
- `elenen/tur2/`: kır sakal düzeltildi, kıyafet stüdyo portresine bağlandı. Bilgehan'ın kendi referans sayfası henüz yoktu.
- `elenen/tur3/`: Bilgehan'ın referans sayfası eklendi, stil örneği hâlâ 6. Reels sahne portresinde Bilgehan yerine Irmak çizildi.
- `elenen/tur4/`: stil örneği 2'ye indi ve "başka kişiler" uyarısı eklendi. Buradakiler kullanıcı ya da Claude kontrolünde elendi. `-alternatif` ekli olanlar ikinci denemelerdir.

Elenenlerin tam istemi saklanmadı; yukarıdaki farklar dışında güncel betikle aynıdır.
