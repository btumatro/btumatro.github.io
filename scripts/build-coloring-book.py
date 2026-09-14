"""A4 boyama kitabı. Kaynak çizimler değişmez; başlık ve yerleşim buradan düzenlenir."""
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json,zipfile
R=Path(__file__).resolve().parents[1]; D=R/'docs/boyama-kitabi'; O=R/'public/media/boyama-kitabi'
font='/System/Library/Fonts/Supplemental/Arial.ttf';pdfmetrics.registerFont(TTFont('Turkce',font))
jobs=[('matris','MATRİS','Gökyüzüne renk kat.',1,0),('matrover','MATROVER','Keşif yolunu sen renklendir.',1,1),('lodos','LODOS','Dalgaların rengini sen seç.',3,0),('prusa','PRUSA','Suyun altındaki dünyayı keşfet.',1,3),('luna','LUNA','Kendi kamuflaj desenini boya.',2,0),('zemheri','ZEMHERİ / SARA','Derinliklere renk kat.',2,1),('iss-auv','İSS / AUV TASARIMI','Hayalindeki su altı aracını renklendir.',2,2),('iss-arsiv','İSS / ARŞİV SERİSİ','Robotun parçalarına renk ver.',2,3)]
pdf=canvas.Canvas(str(O/'matro-boyama-kitabi-a4.pdf'),pagesize=A4);W,H=A4;pdf.setTitle('MATRO Araçları — Boyama Kitabı'); manifest=[]
for i,(slug,title,line,master,q) in enumerate(jobs,1):
 im=Image.open(D/'kaynaklar'/('03-lodos.png' if master==3 else f'{master:02}-master.png')).convert('RGB')
 if master!=3:
  w,h=im.size; col=q%2;row=q//2
  # Orta ayırıcı çizgiler kırpılır; araçlar kadraj içinde korunur.
  im=im.crop((col*w//2+10,row*h//2+10,(col+1)*w//2-10,(row+1)*h//2-10))
 path=O/f'{i:02}-{slug}-cizim.png';im.save(path)
 pdf.setFont('Turkce',10);pdf.drawString(36,H-35,'BTÜ MATRO  /  BOYAMA KİTABI')
 pdf.setFont('Turkce',26);pdf.drawString(36,H-72,title)
 pdf.setFont('Turkce',11);pdf.drawString(36,H-95,line)
 boxw,boxh=W-72,H-170;scale=min(boxw/im.width,boxh/im.height);dw,dh=im.width*scale,im.height*scale
 pdf.drawImage(str(path),(W-dw)/2,58+(boxh-dh)/2,width=dw,height=dh)
 pdf.setFont('Turkce',10);pdf.drawString(36,30,'Adım: __________________________');pdf.drawRightString(W-36,30,f'MATRO  /  {i:02}')
 pdf.showPage();manifest.append({'page':i,'title':title,'image':path.name,'source':master,'quadrant':q})
# Etkinlik sayfaları: vektör çizimler ve düzenlenebilir yönergeler.
import random, math
random.seed(2026)
def head(title,sub):
 pdf.setFont('Turkce',10);pdf.drawString(36,H-35,'BTÜ MATRO / ETKİNLİK ZAMANI')
 pdf.setFont('Turkce',24);pdf.drawString(36,H-75,title)
 pdf.setFont('Turkce',11);pdf.drawString(36,H-100,sub)
def foot(n):
 pdf.setFont('Turkce',10);pdf.drawString(36,30,'Adım: __________________________');pdf.drawRightString(W-36,30,f'MATRO / {n}');pdf.showPage()
head('Atölyeye giden yol','Girişten başla. Duvarları geçmeden atölyeye ulaş!')
n=9;cell=52;ox=62;oy=190;walls=[set(range(4)) for _ in range(n*n)];visited={0};stack=[0]
while stack:
 u=stack[-1];x=u%n;y=u//n;opts=[(d,v) for d,v in [(0,u-n),(1,u+1),(2,u+n),(3,u-1)] if 0<=v<n*n and (d!=1 or x<n-1) and (d!=3 or x>0) and v not in visited]
 if not opts:stack.pop();continue
 d,v=random.choice(opts);walls[u].remove(d);walls[v].remove((d+2)%4);visited.add(v);stack.append(v)
assert len(visited)==n*n
walls[0].discard(3);walls[-1].discard(1);pdf.setLineWidth(2)
for u,ws in enumerate(walls):
 x=ox+(u%n)*cell;y=oy+(n-1-u//n)*cell
 for d in ws:
  seg=[(x,y+cell,x+cell,y+cell),(x+cell,y,x+cell,y+cell),(x,y,x+cell,y),(x,y,x,y+cell)][d];pdf.line(*seg)
pdf.setFont('Turkce',11);pdf.drawString(ox,oy+n*cell+18,'GİRİŞ');pdf.drawRightString(ox+n*cell,oy-24,'ATÖLYE');foot(9)
head('Nerede görev yapar?','Her aracı görev yaptığı yerle bir çizgi çizerek eşleştir.')
for j,(file,label) in enumerate([('01-matris-cizim.png','MATRİS'),('05-luna-cizim.png','LUNA'),('03-lodos-cizim.png','LODOS'),('04-prusa-cizim.png','PRUSA')]):
 y=H-280-j*145;pdf.drawImage(str(O/file),50,y,width=145,height=120,preserveAspectRatio=True,anchor='c');pdf.setFont('Turkce',12);pdf.drawString(55,y-12,label);pdf.circle(235,y+55,4)
for j,label in enumerate(['SU ALTI','GÖKYÜZÜ','DENİZ YÜZEYİ','KARA']):
 y=H-225-j*145;pdf.circle(335,y,4);pdf.setFont('Turkce',15);pdf.drawString(355,y-5,label)
foot(10)
head('Bul, say ve boya','Yıldızları, dişlileri ve pervaneleri say. Sonra dilediğin gibi boya.')
kinds=['yildiz']*5+['disli']*7+['pervane']*6;random.shuffle(kinds)
for i,kind in enumerate(kinds):
 x=100+(i%3)*190;y=H-190-(i//3)*85;pdf.setLineWidth(1.8)
 if kind=='yildiz':
  p=pdf.beginPath()
  for j in range(10):
   a=math.pi/2+j*math.pi/5;r=28 if j%2==0 else 12;px=x+math.cos(a)*r;py=y+math.sin(a)*r
   if j==0:p.moveTo(px,py)
   else:p.lineTo(px,py)
  p.close();pdf.drawPath(p)
 elif kind=='disli':
  p=pdf.beginPath()
  for j in range(32):
   a=j*math.pi/16;r=27 if j%4 in [0,1] else 21;px=x+math.cos(a)*r;py=y+math.sin(a)*r
   if j==0:p.moveTo(px,py)
   else:p.lineTo(px,py)
  p.close();pdf.drawPath(p);pdf.circle(x,y,9)
 else:
  pdf.saveState();pdf.translate(x,y)
  for j in range(3):pdf.rotate(120);pdf.ellipse(3,-9,31,9)
  pdf.circle(0,0,6);pdf.restoreState()
pdf.setFont('Turkce',12);pdf.drawString(60,95,'Yıldız: ____       Dişli: ____       Pervane: ____');foot(11)
head('Benim robotum','Robotuna kollar, tekerlekler veya kanatlar ekle. Sonra boya!')
pdf.setLineWidth(2);pdf.roundRect(205,410,180,160,15);pdf.roundRect(230,590,130,90,15);pdf.circle(266,635,10);pdf.circle(323,635,10);pdf.line(275,610,315,610);pdf.line(295,680,295,710);pdf.circle(295,718,8)
pdf.setFont('Turkce',13);pdf.drawString(60,170,'Robotumun adı: _________________________________');pdf.drawString(60,120,'Görevi: _________________________________________');foot(12)
(D/'cevaplar.txt').write_text('Eşleştirme: MATRİS–gökyüzü; LUNA–kara; LODOS–deniz yüzeyi; PRUSA–su altı. Sayma: 5 yıldız, 7 dişli, 6 pervane. Labirent DFS ile üretildi; 81 hücrenin tamamı bağlıdır.')
pdf.save();(D/'sayfalar.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# PyMuPDF gerektirmeyen PDF render: pypdfium2.
import pypdfium2 as pdfium
doc=pdfium.PdfDocument(str(O/'matro-boyama-kitabi-a4.pdf'))
thumbs=[]
for i,page in enumerate(doc):
 img=page.render(scale=2).to_pil();img.save(O/f'{i+1:02}-{jobs[i][0] if i<8 else ["labirent","eslestirme","bul-say","robot-tasarla"][i-8]}-a4.png');img.thumbnail((297,420));thumbs.append(img)
contact=Image.new('RGB',(4*317,3*440),'#dddddd')
for i,img in enumerate(thumbs):contact.paste(img,((i%4)*317+10,(i//4)*440+10))
contact.save(O/'onizleme.jpg',quality=90)
with zipfile.ZipFile(D/'matro-boyama-kitabi.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():
  if p.is_file():z.write(p,'sayfalar/'+p.name)
 for p in D.rglob('*'):
  if p.is_file() and p.suffix!='.zip':z.write(p,'kaynaklar/'+str(p.relative_to(D)))
 z.write(__file__,'scripts/build-coloring-book.py')
print('12 A4 sayfa, PDF, PNG ve kaynak ZIP hazır.')
