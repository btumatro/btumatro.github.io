from pathlib import Path
import cv2,numpy as np,json,shutil,zipfile
base=Path('public/media/stickers');out=base/'secili-final';out.mkdir(exist_ok=True)
items=[]
def save(im,name,group):
 d=out/group;d.mkdir(exist_ok=True);im[im[:,:,3]==0,:3]=0;cv2.imwrite(str(d/(name+'.png')),im);items.append({'name':name,'group':group,'file':str(d/(name+'.png'))})
def extract(path,cols,names,group,selected=None):
 im=cv2.imread(str(path));gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);mask=(gray<150).astype(np.uint8)*255
 cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);cs=[c for c in cs if cv2.contourArea(c)>15000];cs.sort(key=lambda c:cv2.boundingRect(c)[1]+cv2.boundingRect(c)[3]/2)
 ordered=[]
 for r in range(0,len(cs),cols):ordered+=sorted(cs[r:r+cols],key=lambda c:cv2.boundingRect(c)[0])
 assert len(ordered)==len(names),(path,len(ordered),len(names))
 for name,c in zip(names,ordered):
  if selected and name not in selected:continue
  m=np.zeros(gray.shape,np.uint8);cv2.drawContours(m,[c],-1,255,-1);rgba=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA);rgba[:,:,3]=m;x,y,w,h=cv2.boundingRect(c);save(cv2.copyMakeBorder(rgba[y:y+h,x:x+w],12,12,12,12,cv2.BORDER_CONSTANT,value=(0,0,0,0)),name,group)
for group in ['atolye','kampus','takimlar']:
 for p in (base/'v2/tekil'/group).glob('*.png'):
  if p.stem in ['matris','matrover','iss-auv','iss-arsiv','mimarlik','orman']:continue
  save(cv2.imread(str(p),-1),p.stem,group)
extract('docs/sticker-paketi/yeniden-tasarim/arac-duzeltme-ham.png',1,['matris','matrover'],'takimlar')
extract('docs/sticker-paketi/yeniden-tasarim/takim-kimlikleri-ham.png',3,['goksav','pusula','ashina-acik-govde','burkut','cagri','alhazen','ashina-inovasyon','andromeda','girisimcilik','matrobot','ashina-kanatlar','kara-hava-deniz'],'takimlar',{'goksav','pusula','ashina-acik-govde','alhazen','girisimcilik','kara-hava-deniz'})
extract('docs/sticker-paketi/yeniden-tasarim/yaratici-ham.png',2,['ben-robot-degilim','bende-calisiyordu','gece-vardiyasi','kagittan-gokyuzune','muhendis-yukleniyor','bir-vida-araniyor'],'yaratici')
# Secilen dairesel rozet mevcut kaynaktan, yeniden cizilmeden korunur.
im=cv2.imread(str(base/'05-yaratici.png'));crop=im[500:930,345:704];h,w=crop.shape[:2];rgba=cv2.cvtColor(crop,cv2.COLOR_BGR2BGRA);m=np.zeros((h,w),np.uint8);cv2.ellipse(m,(w//2,h//2),(w//2-3,h//2-4),0,0,360,255,-1);rgba[:,:,3]=m;save(rgba,'birlikte-uretiyoruz','yaratici')
(out/'manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
(out/'OKU.txt').write_text('Kullanicinin 7 baski paftasindaki secimler esas alindi. Tekrarlar tek dosyaya indirildi. PNG dosyalarinda dis arka plan alpha=0. Renkli cizimler rasterdir, tam vektor degildir. Matris ve Matrover yeniden uretildi. Dairesel birlikte uretiyoruz rozeti onceki kaynaktan korunmustur. Baski oncesi son gorsel kontrol gerekir. Kaynak ve betikler docs/sticker-paketi/yeniden-tasarim ile scripts altinda saklandi.\n')
html='<meta charset="utf-8"><title>MATRO Seçili Stickerlar</title><style>body{font:16px sans-serif;background:#ddd}img{width:220px;height:220px;object-fit:contain}article{display:inline-block;background:white;margin:8px;padding:8px}</style><h1>MATRO — Seçili stickerlar</h1>'
for g in ['takimlar','atolye','kampus','yaratici']:
 html+='<h2>'+g+'</h2>'
 for i in items:
  if i['group']==g:html+=f'<article><a href="{g}/{i["name"]}.png"><img src="{g}/{i["name"]}.png"><p>{i["name"]}</p></a></article>'
(out/'index.html').write_text(html)
with zipfile.ZipFile(out/'matro-secili-stickerlar.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in out.rglob('*'):
  if p.is_file() and p.suffix!='.zip':z.write(p,p.relative_to(out))
print(len(items),'sticker kaydedildi')
