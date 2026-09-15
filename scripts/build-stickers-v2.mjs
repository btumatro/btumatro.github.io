import sharp from 'sharp';
import fs from 'node:fs/promises';
const dir='public/media/stickers/v2';
await fs.mkdir(dir,{recursive:true});
const report=[];
for(const name of ['takimlar','atolye','kampus']) {
 const {data,info}=await sharp(`docs/sticker-paketi/yeniden-tasarim/${name}-ham.png`).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const {width:w,height:h}=info, n=w*h, mask=new Uint8Array(n), queue=new Int32Array(n);let head=0,tail=0;
 const gray=(i)=>{const r=data[i*3],g=data[i*3+1],b=data[i*3+2];return Math.max(r,g,b)-Math.min(r,g,b)<30&&Math.min(r,g,b)>85;};
 const add=(i)=>{if(!mask[i]&&gray(i)){mask[i]=1;queue[tail++]=i;}};
 for(let x=0;x<w;x++){add(x);add((h-1)*w+x);}for(let y=0;y<h;y++){add(y*w);add(y*w+w-1);}
 while(head<tail){const i=queue[head++],x=i%w,y=Math.floor(i/w);if(x)add(i-1);if(x<w-1)add(i+1);if(y)add(i-w);if(y<h-1)add(i+w);}
 const out=Buffer.alloc(n*4);for(let i=0;i<n;i++){out[i*4]=data[i*3];out[i*4+1]=data[i*3+1];out[i*4+2]=data[i*3+2];out[i*4+3]=mask[i]?0:255;}
 await sharp(out,{raw:{width:w,height:h,channels:4}}).png().toFile(`${dir}/${name}.png`);
 await sharp(out,{raw:{width:w,height:h,channels:4}}).flatten({background:'#ffffff'}).png().toFile(`${dir}/${name}-beyaz.png`);
 report.push({name,width:w,height:h,transparentPixels:tail,totalPixels:n,alphaZeroPercent:Math.round(tail/n*100)});
}
await fs.writeFile(`${dir}/kontrol.json`,JSON.stringify(report,null,2));console.log(report);
