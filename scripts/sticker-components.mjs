import sharp from 'sharp';
for(const f of ['09-araclar-referans','10-atolye-guncel','11-kampus-guncel']){
 const {data,info:{width:w,height:h}}=await sharp('public/media/stickers/'+f+'.png').removeAlpha().raw().toBuffer({resolveWithObject:true});let m=Buffer.alloc(w*h);for(let i=0;i<m.length;i++)m[i]=Math.min(...data.subarray(i*3,i*3+3))<250?255:0;
 m=await sharp(m,{raw:{width:w,height:h,channels:1}}).dilate(2).greyscale().raw().toBuffer();let seen=new Uint8Array(w*h),cs=[];
 for(let i=0;i<seen.length;i++){if(seen[i]||!m[i])continue;let q=[i],x0=w,y0=h,x1=0,y1=0;seen[i]=1;for(let k=0;k<q.length;k++){let p=q[k],x=p%w,y=Math.floor(p/w);x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);for(const n of [x>0?p-1:-1,x<w-1?p+1:-1,y>0?p-w:-1,y<h-1?p+w:-1])if(n>=0&&!seen[n]&&m[n]){seen[n]=1;q.push(n);}}if(q.length>1000)cs.push([q.length,x0,y0,x1,y1]);}console.log(f,cs);
}
