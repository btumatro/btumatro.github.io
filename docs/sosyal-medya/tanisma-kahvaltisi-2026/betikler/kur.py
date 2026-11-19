#!/usr/bin/env python3
"""MATRO Tanışma Kahvaltısı 2026: Instagram gönderisi (1080x1350) ve site kapak görseli (1920x1080).
Renk ve yazı tipi sitenin kendi belirteçlerinden: ink #101719, volt #4cbab7, medal #ffc247, mist #f0f0e9, Barlow."""
from pathlib import Path
from playwright.sync_api import sync_playwright

B = Path(__file__).parent.resolve()
F = B / "node_modules/@fontsource"
FONT = "".join(
    f"@font-face{{font-family:'{ad}';font-weight:{w};src:url('file://{F}/{pk}/files/{pk}-{alt}-{w}-normal.woff2') format('woff2');unicode-range:{ur}}}"
    for ad, pk in (("Barlow", "barlow"), ("BarlowC", "barlow-condensed"))
    for w in (500, 700, 800)
    for alt, ur in (("latin", "U+0000-00FF"), ("latin-ext", "U+0100-024F,U+1E00-1EFF"))
)
ORTAK = f"""<style>{FONT}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);overflow:hidden;background:#101719;font-family:Barlow;color:#f0f0e9}}
.foto{{position:absolute;inset:0;background-size:cover;background-position:center}}
.ust{{display:flex;align-items:center;gap:22px}}
.ust img.m{{height:calc(var(--logo)*1.45)}} .ust img.b{{height:calc(var(--logo)*.8)}}
.cz{{width:2px;align-self:stretch;background:rgba(240,240,233,.35)}}
.kick{{font-family:BarlowC;font-weight:700;letter-spacing:.32em;color:#75d5d0;text-transform:uppercase}}
.baslik{{font-family:BarlowC;font-weight:800;line-height:.9;text-transform:uppercase;letter-spacing:.01em}}
.baslik span{{color:#ffc247}}
.bilgi{{display:flex;flex-direction:column;gap:10px}}
.satir{{display:flex;align-items:baseline;gap:18px;font-family:BarlowC;font-weight:700;text-transform:uppercase;letter-spacing:.06em}}
.satir b{{color:#ffc247;font-weight:800}}
.cubuk{{width:96px;height:6px;background:#4cbab7;border-radius:3px}}
.alt{{font-weight:500;color:#bdc8c9}}
</style>"""

POST = ORTAK + """<style>
:root{--w:1080px;--h:1350px;--logo:78px}
.sis{position:absolute;inset:0;background:linear-gradient(180deg,rgba(16,23,25,.94) 0%,rgba(16,23,25,.8) 34%,rgba(16,23,25,0) 50%),linear-gradient(0deg,rgba(16,23,25,.96) 0%,rgba(16,23,25,.7) 20%,rgba(16,23,25,0) 36%)}
.bas{position:absolute;left:80px;right:80px;top:76px}
.kick{font-size:28px;margin:58px 0 18px}
.baslik{font-size:150px}
.ozet{font-size:30px;line-height:1.35;color:#f0f0e9;max-width:820px;margin-top:26px}
.son{position:absolute;left:80px;right:80px;bottom:72px;display:flex;justify-content:space-between;align-items:flex-end}
.satir{font-size:52px}.satir.k{font-size:40px}
.etiket{font-family:BarlowC;font-weight:700;font-size:28px;letter-spacing:.12em;color:#75d5d0;text-align:right}
</style>
<div class="foto" style="background-image:url('file://B/foto45.jpg')"></div><div class="sis"></div>
<div class="bas">
  <div class="ust"><img class="m" src="file://B/logo-matro-beyaz.png"><div class="cz"></div><img class="b" src="file://B/logo-btu-beyaz.png"></div>
  <div class="kick">Geleneksel</div>
  <div class="baslik">Tanışma<br><span>Kahvaltısı</span></div>
</div>
<div class="son">
  <div class="bilgi"><div class="cubuk"></div>
    <div class="satir"><b>29 Kasım</b> Pazar · 10.30</div>
    <div class="satir k">Mahfel Lounge · Bursa</div></div>
  <div class="etiket">@BTUMATRO</div>
</div>"""

KAPAK = ORTAK + """<style>
:root{--w:1920px;--h:1080px;--logo:84px}
.sis{position:absolute;inset:0;background:linear-gradient(90deg,rgba(16,23,25,.96) 0%,rgba(16,23,25,.86) 34%,rgba(16,23,25,.2) 62%,rgba(16,23,25,0) 75%)}
.bas{position:absolute;left:120px;top:110px;width:900px}
.kick{font-size:30px;margin:70px 0 20px}
.baslik{font-size:168px}
.bilgi{position:absolute;left:120px;bottom:110px}
.satir{font-size:58px}.satir.k{font-size:44px}
</style>
<div class="foto" style="background-image:url('file://B/foto169.jpg')"></div><div class="sis"></div>
<div class="bas">
  <div class="ust"><img class="m" src="file://B/logo-matro-beyaz.png"><div class="cz"></div><img class="b" src="file://B/logo-btu-beyaz.png"></div>
  <div class="kick">Geleneksel</div>
  <div class="baslik">Tanışma<br><span>Kahvaltısı</span></div>
</div>
<div class="bilgi"><div class="cubuk"></div>
  <div class="satir"><b>29 Kasım</b> Pazar · 10.30</div>
  <div class="satir k">Mahfel Lounge · Bursa</div></div>"""


HIKAYE = ORTAK + """<style>
:root{--w:1080px;--h:1920px;--logo:80px}
.sis{position:absolute;inset:0;background:linear-gradient(180deg,rgba(16,23,25,.95) 0%,rgba(16,23,25,.82) 30%,rgba(16,23,25,0) 46%),linear-gradient(0deg,rgba(16,23,25,.97) 0%,rgba(16,23,25,.8) 24%,rgba(16,23,25,0) 40%)}
.bas{position:absolute;left:80px;right:80px;top:270px}
.kick{font-size:30px;margin:60px 0 20px}
.baslik{font-size:164px}
.son{position:absolute;left:80px;right:80px;bottom:370px}
.satir{font-size:58px}.satir.k{font-size:44px}
.wa{margin-top:26px;font-size:30px;font-weight:500;color:#bdc8c9}
</style>
<div class="foto" style="background-image:url('file://B/foto916.jpg')"></div><div class="sis"></div>
<div class="bas">
  <div class="ust"><img class="m" src="file://B/logo-matro-beyaz.png"><div class="cz"></div><img class="b" src="file://B/logo-btu-beyaz.png"></div>
  <div class="kick">Geleneksel</div>
  <div class="baslik">Tanışma<br><span>Kahvaltısı</span></div>
</div>
<div class="son"><div class="bilgi"><div class="cubuk"></div>
  <div class="satir"><b>29 Kasım</b> Pazar · 10.30</div>
  <div class="satir k">Mahfel Lounge · Bursa</div></div>
  <div class="wa">Katılım için WhatsApp grubumuza göz at</div></div>"""
POST34 = POST.replace("--h:1350px", "--h:1440px")

with sync_playwright() as p:
    br = p.chromium.launch()
    for ad, html, w, h in (("post", POST, 1080, 1350), ("post34", POST34, 1080, 1440), ("hikaye", HIKAYE, 1080, 1920), ("kapak", KAPAK, 1920, 1080)):
        f = B / f"{ad}.html"; f.write_text(html.replace("file://B/", f"file://{B}/"), encoding="utf-8")
        pg = br.new_page(viewport={"width": w, "height": h})
        pg.goto(f"file://{f}"); pg.wait_for_timeout(600)
        pg.screenshot(path=str(B / f"{ad}.png"))
        pg.close()
    br.close()
print("tamam")
