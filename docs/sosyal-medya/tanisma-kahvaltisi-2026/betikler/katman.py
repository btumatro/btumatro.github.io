#!/usr/bin/env python3
"""Reels yazı katmanları (saydam PNG, 1080x1920). Güvenli alan: üst 250, alt 340 px boş."""
from pathlib import Path
from playwright.sync_api import sync_playwright
B = Path(__file__).parent.resolve(); K = Path("/tmp/kahvalti"); F = K / "node_modules/@fontsource"
FONT = "".join(
    f"@font-face{{font-family:'{ad}';font-weight:{w};src:url('file://{F}/{pk}/files/{pk}-{alt}-{w}-normal.woff2') format('woff2');unicode-range:{ur}}}"
    for ad, pk in (("Barlow", "barlow"), ("BarlowC", "barlow-condensed")) for w in (500, 700, 800)
    for alt, ur in (("latin", "U+0000-00FF"), ("latin-ext", "U+0100-024F,U+1E00-1EFF")))
CSS = f"""<style>{FONT}*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:transparent;font-family:Barlow;color:#f0f0e9;overflow:hidden}}
.ust{{position:absolute;left:80px;top:270px;display:flex;align-items:center;gap:22px}}
.ust img.m{{height:116px}} .ust img.b{{height:64px}} .cz{{width:2px;height:80px;background:rgba(240,240,233,.4)}}
.kick{{font-family:BarlowC;font-weight:700;font-size:32px;letter-spacing:.32em;color:#75d5d0;text-transform:uppercase}}
.baslik{{font-family:BarlowC;font-weight:800;font-size:170px;line-height:.9;text-transform:uppercase;text-shadow:0 6px 30px rgba(0,0,0,.45)}}
.baslik span{{color:#ffc247}}
.satir{{font-family:BarlowC;font-weight:700;font-size:62px;text-transform:uppercase;letter-spacing:.05em;text-shadow:0 4px 20px rgba(0,0,0,.5)}}
.satir b{{color:#ffc247;font-weight:800}} .satir.k{{font-size:46px}}
.cubuk{{width:96px;height:6px;background:#4cbab7;border-radius:3px;margin-bottom:14px}}
.sis-ust{{position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(180deg,rgba(16,23,25,.88),rgba(16,23,25,.55) 55%,rgba(16,23,25,0))}}
.sis-alt{{position:absolute;left:0;right:0;bottom:0;height:820px;background:linear-gradient(0deg,rgba(16,23,25,.92),rgba(16,23,25,.6) 50%,rgba(16,23,25,0))}}
.sis-tam{{position:absolute;inset:0;background:rgba(16,23,25,.55)}}
</style>"""
L = {
 "l0-sis": '<div class="sis-ust" style="height:560px"></div>',
 "l0-logo": '<div class="ust"><img class="m" src="file://K/logo-matro-beyaz.png"><div class="cz"></div><img class="b" src="file://K/logo-btu-beyaz.png"></div>',
 "l1-baslik": '<div class="sis-ust"></div><div style="position:absolute;left:80px;top:470px"><div class="kick" style="margin-bottom:22px">Geleneksel</div><div class="baslik">Tanışma<br><span>Kahvaltısı</span></div></div>',
 "l2-bilgi": '<div class="sis-alt"></div><div style="position:absolute;left:80px;bottom:380px"><div class="cubuk"></div><div class="satir"><b>29 Kasım</b> Pazar · 10.30</div><div class="satir k" style="margin-top:8px">Mahfel Lounge · Bursa</div></div>',
 "l3-son": '<div class="sis-tam"></div><div style="position:absolute;left:0;right:0;top:760px;text-align:center"><div class="kick">MATRO · BTÜ</div><div class="baslik" style="font-size:150px;margin-top:24px">Seni de<br><span>bekliyoruz</span></div><div class="satir k" style="margin-top:46px">29 Kasım · 10.30 · Mahfel Lounge</div><div class="kick" style="margin-top:40px;letter-spacing:.14em">@BTUMATRO</div></div>',
}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1920})
    for ad, g in L.items():
        f = B / f"{ad}.html"; f.write_text(CSS + g.replace("file://K/", f"file://{K}/"), encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(400); pg.screenshot(path=str(B / f"{ad}.png"), omit_background=True)
    br.close()
print("tamam")
