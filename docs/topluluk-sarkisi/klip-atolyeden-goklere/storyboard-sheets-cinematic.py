#!/usr/bin/env python3
"""Üretilen sinematik klip örneği için okunaklı prodüksiyon storyboard sheet'i."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'sheets' / 'storyboard-sinematik-ornek.png'
W, H = 2400, 1660
im = Image.new('RGB', (W, H), '#111820')
d = ImageDraw.Draw(im)
font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
bold_path = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(size, bold=False): return ImageFont.truetype(bold_path if bold else font_path, size)
d.text((90, 60), 'ATÖLYEDEN GÖKLERE', font=font(62, True), fill='#f5f0e6')
d.text((92, 140), 'SİNEMATİK ÖRNEK  /  TAKIMLARIN ARAÇLARI GERÇEK REFERANSLARINDAN', font=font(28, True), fill='#d6a85f')
d.text((92, 190), '16:9  •  24 fps  •  20 sn  •  Omni Flash image-to-video  •  şarkının özgün ses kaydı', font=font(24), fill='#bdc7cc')

shots = [
 ('01', 'ASHİNA · ATÖLYE', '00:00–00:04', '50 mm · tezgâh hizası · yavaş ileri kayış', 'ana-kareler/ashina-sinematik.png'),
 ('02', 'LODOS · KIYI', '00:04–00:08', '35 mm · üç çeyrek ön · yavaş yaklaşma', 'ana-kareler/lodos-sinematik.png'),
 ('03', 'PRUSA · GÖVDE', '00:08–00:12', '50 mm · alçak yakın plan · yanal kayış', 'ana-kareler/prusa-sinematik.png'),
 ('04', 'ZEMHERİ · GECE TESTİ', '00:12–00:16', '35 mm · iskele hizası · yavaş yanal hareket', 'ana-kareler/zemheri-sinematik.png'),
 ('05', 'MATRİS · SÜRÜ İHA', '00:16–00:20', '50 mm · çim hizası · yavaş yanal izleme', 'ana-kareler/matris-sinematik.png'),
]
x0, gap, cw, ch = 90, 22, 420, 700
for i, (n, title, tc, cam, fname) in enumerate(shots):
    x = x0 + i * (cw + gap); y = 270
    d.rounded_rectangle((x, y, x+cw, y+ch), radius=14, fill='#1b252d', outline='#52616a', width=2)
    img = Image.open(ROOT / fname).convert('RGB')
    img = ImageOps.fit(img, (cw-16, 260), method=Image.Resampling.LANCZOS, centering=(0.5,0.5))
    im.paste(img, (x+8, y+8))
    d.rounded_rectangle((x+20, y+20, x+154, y+54), radius=8, fill='#d6a85f')
    d.text((x+29, y+24), 'AI KONSEPT', font=font(16, True), fill='#172028')
    d.text((x+20, y+286), n + '   ' + title, font=font(24, True), fill='#f5f0e6')
    d.text((x+20, y+330), tc, font=font(22, True), fill='#d6a85f')
    words = cam.split(); lines=[]; line=''
    for word in words:
        test=(line+' '+word).strip()
        if d.textbbox((0,0), test, font=font(19))[2] > cw-42:
            lines.append(line); line=word
        else: line=test
    if line: lines.append(line)
    for j, line in enumerate(lines): d.text((x+20, y+375+j*26), line, font=font(19), fill='#c5d0d4')
    d.line((x+20,y+466,x+cw-20,y+466),fill='#394852',width=2)
    notes = ['Hareket: sahneye göre yalnız kamera.', 'Nesne: araç geometrisi sabit kalır.', 'Işık: doğal, ölçülü, aynı ton ailesi.']
    for j, line in enumerate(notes): d.text((x+20,y+486+j*35),line,font=font(17),fill='#a8b5bb')

d.rounded_rectangle((90, 1015, W-90, 1550), radius=18, fill='#182229', outline='#465660', width=2)
d.text((125, 1050), 'GÖRSEL DEVAMLILIK VE MONTAJ NOTLARI', font=font(31, True), fill='#f5f0e6')
notes = [
 'Kesme sırası şarkıdaki adları izler: ASHİNA → LODOS → PRUSA → ZEMHERİ → MATRİS.',
 'Araçlar hareket etmez; hareketi kamera verir. Ek parça, değişen gövde, fazladan rotor/pervane görülürse plan çıkarılır.',
 'Geçişler kısa ve sade; tüm planlarda doğal renk, ölçülü kontrast ve gerçekçi ışık korunur.',
 'Referanslar: takım sunumları ve site arşivindeki gerçek araç fotoğrafları. Sinematik kareler yeniden oluşturulmuş görseldir.',
 'Klip örneği: 20 sn, 1280×720, 24 fps. Kurguda şarkı 01:30.667’den başlar; yapay üretilmiş ses kullanılmaz.',
]
for i,line in enumerate(notes): d.text((130, 1115+i*66), '—  '+line, font=font(23), fill='#c5d0d4')
OUT.parent.mkdir(parents=True, exist_ok=True)
im.save(OUT, quality=95)
print(OUT)
