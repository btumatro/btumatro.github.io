import os,sys
from PIL import Image,ImageDraw,ImageFont
D,out=sys.argv[1],sys.argv[2]
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',22)
K=['adem-baglan','irmak-karaagac','muhammed-ataman']
ST=['a reels sahne','b reels pafta','c 3B animasyon','d vektör','e suluboya','f çizgi roman']
S=320;im=Image.new('RGB',(S*7,44+S*3),(24,24,24));d=ImageDraw.Draw(im)
d.text((8,10),'fotoğraf',fill=(255,255,255),font=f)
for j,t in enumerate(ST): d.text((S*(j+1)+8,10),t,fill=(255,140,0),font=f)
for i,k in enumerate(K):
  y=44+i*S;im.paste(Image.open(f'docs/ekip/yz/codex/gri-fon/{k}.jpg').convert('RGB').resize((S-6,S-6)),(0,y))
  for j,t in enumerate(ST):
    p=f'{D}/{t[0]}-{k}.jpg'
    if os.path.exists(p): im.paste(Image.open(p).convert('RGB').resize((S-6,S-6)),(S*(j+1),y))
im.save(out,quality=86)
