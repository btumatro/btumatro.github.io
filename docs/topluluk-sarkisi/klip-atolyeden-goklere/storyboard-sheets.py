"""Atölyeden Göklere klibi için kaynak etiketli üç storyboard sheet üretir."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MEDIA = ROOT / "public/media"
OUT = HERE / "sheets"
OUT.mkdir(exist_ok=True)

REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
font = lambda size, bold=False: ImageFont.truetype(BOLD if bold else REG, size)

def make_final_card():
    card = Image.new("RGB", (1600, 900), "#102a35")
    cd = ImageDraw.Draw(card)
    cd.rectangle((0, 0, 1600, 11), fill="#c46e3d")
    cd.text((92, 123), "ATÖLYEDEN GÖKLERE", font=font(48, True), fill="#b8d7dd")
    cd.text((88, 216), "ATÖLYEDE BAŞLAR", font=font(81, True), fill="white")
    cd.text((88, 308), "SAHADA KANITLANIR", font=font(81, True), fill="white")
    cd.line((92, 494, 1508, 494), fill="#68838b", width=2)
    for path, box in [
        (ROOT / "public/logo-matro-beyaz.png", (120, 556, 333, 769)),
        (ROOT / "public/logo-btu-beyaz.png", (840, 610, 1460, 755)),
    ]:
        logo = Image.open(path).convert("RGBA")
        logo.thumbnail((box[2]-box[0], box[3]-box[1]), Image.Resampling.LANCZOS)
        card.paste(logo, (box[0], box[1]), logo)
    card.save(HERE / "assets" / "final-card.png", optimize=True)

make_final_card()

def make_team_triptych():
    names = ["konsept-ashina-kalkis.png", "konsept-lodos-seyir.png", "konsept-prusa-sualti.png"]
    labels = ["ASHİNA", "LODOS 2026", "PRUSA"]
    trip = Image.new("RGB", (1800, 1000), "#102a35")
    td = ImageDraw.Draw(trip)
    for i, (name, label) in enumerate(zip(names, labels)):
        x = i * 600
        im = Image.open(HERE / "assets" / name).convert("RGB")
        trip.paste(ImageOps.fit(im, (600, 1000), method=Image.Resampling.LANCZOS), (x, 0))
        td.rectangle((x, 910, x+600, 1000), fill="#102a35")
        td.text((x+25, 928), label, font=font(42, True), fill="white")
        if i: td.line((x, 0, x, 1000), fill="white", width=5)
    trip.save(HERE / "assets" / "konsept-takimlar-ucleme.png", optimize=True)

make_team_triptych()

SHEETS = [
    (
        "01 / KIVILCIM",
        "0:00—1:00  ·  gece / atölye / prototip / ilk saha",
        "Atölye temposu; gerçek doku, kısa ayrıntı kesmeleri, yükselen enerji.",
        [
            ("00:00–00:10", "Başlıyoruz", "Gece iskelesi: karanlıktan tek pratik ışığa açıl.", "konsept-gece-iskele.png", "AI KONSEPT"),
            ("00:10–00:20", "Gece yarısı atölyede", "Gerçek saha montajı; el ve bağlantı ayrıntısına kes.", "galeri-ashina-sunum-gece-montaj.jpg", "ARŞİV"),
            ("00:20–00:28", "Bir lehim, bir vida", "Elektronik ayrıntısından el işçiliğine ritmik kesme.", "galeri-ashina-sunum-elektronik-masa.jpg", "ARŞİV"),
            ("00:28–00:40", "İlk adım / ileri", "Yıl için tipografi; fotoğrafı 2013 diye sunma.", "galeri-ashina-atolye-iha.jpg", "ARŞİV"),
            ("00:40–00:52", "Çizgi sahada iz olur", "Üretim fotoğrafından gerçek pist testine eşleştirme.", "galeri-ashina-pist-testi.jpg", "ARŞİV"),
            ("00:52–01:00", "Dün hayaldi, bugün gerçek", "Alçak açı kalkış taslağı; gerçek uçuşla karşılaştır.", "konsept-ashina-kalkis.png", "AI KONSEPT"),
        ],
    ),
    (
        "02 / SAHADA KANIT",
        "1:00—2:00  ·  ilk nakarat / beş takım / gerçek araçlar",
        "Nakaratta geniş plan; takım adlarında araç ve insan aynı kadrajda.",
        [
            ("01:00–01:10", "Atölyede başlar", "Gerçek ZEMHERİ gövde montajından su testine kes.", "galeri-zemheri-sunum-govde-montaj.jpg", "ARŞİV"),
            ("01:10–01:20", "Mavi vatandan göklere", "PRUSA'nın referanslı su altı hareket taslağı.", "konsept-prusa-sualti.png", "AI KONSEPT"),
            ("01:20–01:32", "MATRO / daima ileri", "Kalabalık ekip, kısa gerçek yüzler; tipografi tek vuruş.", "galeri-ashina-2026-ekip.jpg", "ARŞİV"),
            ("01:32–01:40", "ASHİNA / LODOS / PRUSA", "Üç kesme: İHA, güncel İDA, su altı aracı.", "konsept-takimlar-ucleme.png", "AI KONSEPT"),
            ("01:40–01:48", "ZEMHERİ / MATRİS", "Gece su testi ve sürü uçuşu iki ayrı kesme.", "galeri-zemheri-sunum-gece-su-testi.jpg", "ARŞİV"),
            ("01:48–02:00", "Bursa'dan yola çıktık", "MATRİS araçlarını sahada geniş planda göster.", "konsept-matris-suru-ucus.png", "AI KONSEPT"),
        ],
    ),
    (
        "03 / YENİDEN DENE",
        "2:00—3:00  ·  test / dayanışma / son nakarat / final",
        "En güçlü bitiş: başarısızlık hissi, yeniden kurma ve toplu final.",
        [
            ("02:00–02:12", "Bir test daha kırılsa", "MATRİS'in gerçek yakın montajı; sahte kaza üretme.", "galeri-matris-sunum-yakin-montaj.jpg", "ARŞİV"),
            ("02:12–02:20", "Birlikte güçlüyüz", "ZEMHERİ'nin gerçek yarışma kontrol anı.", "galeri-zemheri-sunum-yarisma-kontrol.jpg", "ARŞİV"),
            ("02:20–02:34", "Sahada kanıtlanır", "Güncel LODOS gövdesi ve doğal su izi.", "konsept-lodos-seyir.png", "AI KONSEPT"),
            ("02:34–02:46", "Mavi vatandan göklere", "Su üstü → su altı → hava; sert ama temiz geçiş.", "galeri-zemheri-havuz-testi.jpg", "ARŞİV"),
            ("02:46–02:56", "MA-TRO! MA-TRO!", "Takım ve araçlardan 1–2 sn'lik ortak yükseliş.", "galeri-ashina-teknofest-grup.jpg", "ARŞİV"),
            ("02:56–03:00", "Atölyede başlar", "Koyu zemin, özgün MATRO + BTÜ logoları, temiz kapanış.", "final-card.png", "GRAFİK"),
        ],
    ),
]

CAMERAS = [
    ["24 mm · su hizası · kilitli plan", "35 mm · saha hizası · hafif yaklaş", "85 mm · masa ayrıntısı · kilitli", "50 mm · masa yüksekliği · hafif pan", "35 mm · geniş pist · yanal takip", "35 mm · asfalt hizası · sabit"],
    ["35 mm · omuz üstü · doğal ışık", "50 mm · alçak araç açısı · sabit", "35 mm · geniş ekip · kısa bekleme", "50 mm · üç sert kesme · aynı ölçek", "35 mm · su hizası · kilitli", "50 mm · asfalt hizası · sabit"],
    ["50 mm · yakın montaj · sabit", "50 mm · yakın kontrol · sabit", "35 mm · su hizası · hafif takip", "24 mm · havuz geniş · temiz eşleme", "35 mm · kısa ekip kesmeleri", "50 mm · sabit final kartı"],
]

def image_for(name):
    return (HERE / "assets" / name) if name.startswith(("konsept-", "final-")) else (MEDIA / name)

def cover(im, box):
    w, h = box
    return ImageOps.fit(im, (w, h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def wrap(draw, s, f, maxw, maxlines=2):
    words = s.split()
    lines, line = [], ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test, font=f)[2] <= maxw:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines[:maxlines]

for index, (title, subtitle, note, panels) in enumerate(SHEETS, 1):
    W, H = 2100, 1430
    sheet = Image.new("RGB", (W, H), "#e8e6e0")
    d = ImageDraw.Draw(sheet)
    navy, warm = "#102a35", "#c46e3d"
    d.rectangle((0, 0, W, 174), fill=navy)
    d.text((60, 31), "ATÖLYEDEN GÖKLERE", font=font(24, True), fill="#b8d7dd")
    d.text((60, 68), title, font=font(54, True), fill="white")
    d.text((1020, 92), subtitle, font=font(26), fill="#d9e4e4")
    cw, ih, cardh, gap = 630, 345, 545, 42
    x0, y0 = 64, 216
    for i, (tc, lyric, action, source, tag) in enumerate(panels):
        col, row = i % 3, i // 3
        x, y = x0 + col * (cw + gap), y0 + row * (cardh + 36)
        d.rounded_rectangle((x, y, x+cw, y+cardh), radius=18, fill="white")
        img = Image.open(image_for(source)).convert("RGB")
        img = cover(img, (cw, ih))
        # Hafif ortak ton: görüntünün gerçek içeriğini değiştirmez.
        img = ImageEnhance.Color(img).enhance(0.86)
        sheet.paste(img, (x, y))
        d.rectangle((x, y, x+cw, y+42), fill=navy)
        d.text((x+16, y+7), f"{i+1:02d}   {tc}", font=font(25, True), fill="white")
        badgew = 160 if tag == "AI KONSEPT" else 105
        badge_y = y+ih-104 if source == "konsept-takimlar-ucleme.png" else y+ih-40
        d.rounded_rectangle((x+cw-badgew-10, badge_y, x+cw-10, badge_y+30), radius=9, fill=warm if tag == "AI KONSEPT" else navy)
        d.text((x+cw-badgew+1, badge_y+5), tag, font=font(19, True), fill="white")
        d.text((x+17, y+ih+14), lyric, font=font(27, True), fill=navy)
        for li, line in enumerate(wrap(d, action, font(21), cw-34)):
            d.text((x+17, y+ih+55+li*26), line, font=font(21), fill="#384b50")
        d.text((x+17, y+cardh-78), CAMERAS[index-1][i], font=font(19, True), fill="#a45632")
        d.line((x+17, y+cardh-55, x+cw-17, y+cardh-55), fill="#d7d8d4", width=2)
        d.text((x+17, y+cardh-43), source, font=font(18), fill="#66757a")
    d.text((64, H-40), note, font=font(23), fill=navy)
    d.text((W-142, H-40), f"{index} / 3", font=font(22, True), fill=navy)
    sheet.save(OUT / f"storyboard-{index:02d}.png", optimize=True)

pages = [Image.open(OUT / f"storyboard-{i:02d}.png").convert("RGB") for i in (1, 2, 3)]
pages[0].save(OUT / "storyboard-tumu.pdf", save_all=True, append_images=pages[1:], resolution=160)
