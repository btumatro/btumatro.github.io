from pathlib import Path
import cv2, numpy as np, json, shutil
root=Path('public/media/stickers/v2')
groups={'takimlar':(2,['matris','matrover','iss-auv','iss-arsiv','zemheri','luna','lodos','prusa']), 'atolye':(3,['matro-btu','atolye-modu','ciz-uret-test-et','birlikte-uret','bir-test-daha','koddan-harekete','matro-bursa','takim-isi','sahaya-hazir']), 'kampus':(3,['btu','teknofest','makine','bilgisayar','elektrik-elektronik','mekatronik','endustri','mimarlik','kimya','orman','malzeme','matroda-yerin-var'])}
report=[]
for group,(cols,names) in groups.items():
 im=cv2.imread(str(root/f'{group}.png'),cv2.IMREAD_UNCHANGED)
 mask=cv2.morphologyEx(im[:,:,3],cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
 contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 big=[c for c in contours if cv2.contourArea(c)>20000]
 if group=='takimlar':
  big=[c for c in big if cv2.boundingRect(c)[1]>440]
  outlines=[[(15,195),(100,175),(93,110),(266,4),(310,4),(320,65),(425,65),(453,54),(659,123),(659,166),(585,186),(585,267),(596,350),(570,405),(483,413),(458,438),(416,445),(256,445),(242,425),(172,424),(125,390),(98,281),(15,255)],[(595,326),(622,268),(652,215),(674,145),(729,125),(733,41),(780,0),(888,0),(906,70),(951,89),(964,139),(1009,148),(1020,326),(1008,372),(988,415),(914,433),(707,442),(686,421),(594,405)]]
  big.extend(np.array(p,np.int32).reshape(-1,1,2) for p in outlines)
 assert len(big)==len(names),(group,len(big))
 big.sort(key=lambda c:cv2.boundingRect(c)[1]+cv2.boundingRect(c)[3]/2)
 ordered=[]
 for r in range(0,len(big),cols):ordered.extend(sorted(big[r:r+cols],key=lambda c:cv2.boundingRect(c)[0]))
 dest=root/'tekil'/group;dest.mkdir(parents=True,exist_ok=True)
 whole=np.zeros_like(im)
 for name,c in zip(names,ordered):
  m=np.zeros(mask.shape,np.uint8);cv2.drawContours(m,[c],-1,255,cv2.FILLED)
  # Konturun icindeki beyaz sticker payini opak tut, disini alpha=0 yap.
  pixels=im.copy();pixels[:,:,3]=m
  pixels[(m>0)&(im[:,:,3]==0),:3]=255
  x,y,w,h=cv2.boundingRect(c)
  piece=cv2.copyMakeBorder(pixels[y:y+h,x:x+w],12,12,12,12,cv2.BORDER_CONSTANT,value=(0,0,0,0))
  cv2.imwrite(str(dest/f'{name}.png'),piece)
  whole[m>0]=pixels[m>0]
  report.append({'group':group,'name':name,'file':str(dest/f'{name}.png'),'width':piece.shape[1],'height':piece.shape[0],'alphaMin':int(piece[:,:,3].min()),'alphaMax':int(piece[:,:,3].max())})
 cv2.imwrite(str(root/f'{group}.png'),whole)
 white=whole[:,:,:3].copy();white[whole[:,:,3]==0]=255
 cv2.imwrite(str(root/f'{group}-beyaz.png'),white)
# ASHINA araci tek sticker olarak uretilmistir; mevcut alpha kanali korunur.
a=cv2.imread(str(root/'ashina.png'),cv2.IMREAD_UNCHANGED)
assert a.shape[2]==4 and a[:,:,3].min()==0
(root/'tekil/takimlar').mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'ashina.png',root/'tekil/takimlar/ashina.png')
report.append({'group':'takimlar','name':'ashina','file':str(root/'tekil/takimlar/ashina.png'),'width':a.shape[1],'height':a.shape[0],'alphaMin':int(a[:,:,3].min()),'alphaMax':int(a[:,:,3].max())})
(root/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Dogrulanan tekil PNG:',len(report))
for item in report:
 p=Path(item['file']);im=cv2.imread(str(p),cv2.IMREAD_UNCHANGED)
 contours,_=cv2.findContours((im[:,:,3]>127).astype(np.uint8)*255,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 paths=[]
 for c in contours:
  if cv2.contourArea(c)<100:continue
  pts=cv2.approxPolyDP(c,0.8,True).reshape(-1,2)
  paths.append('M '+' L '.join(f'{x},{y}' for x,y in pts)+' Z')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {im.shape[1]} {im.shape[0]}"><g id="Kesim-Konturu" fill="none" stroke="#ff00ff" stroke-width="1">'+''.join(f'<path d="{d}"/>' for d in paths)+'</g></svg>'
 p.with_suffix('.kesim.svg').write_text(svg)
