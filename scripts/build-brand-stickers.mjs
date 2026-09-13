// Orijinal logolar yeniden çizilmez; kaynak PNG baytları SVG içine gömülür.
// Metin ve çevre geometrileri düzenlenebilir. node scripts/build-brand-stickers.mjs
import fs from 'node:fs/promises';
import sharp from 'sharp';
const out = 'public/media/stickers/kurumsal';
await fs.mkdir(out, { recursive: true });
const paths = {
 blue:'public/logo-matro-mavi.png', white:'public/logo-matro-beyaz.png',
 black:'public/logo-matro-siyah.png', btu:'public/logo-btu.png',
 tf:'docs/sticker-paketi/referanslar/TR_TEKNOFEST/t3-logo-TR-01.png'
};
const logos = Object.fromEntries(await Promise.all(Object.entries(paths).map(async ([k,p])=>[k,'data:image/png;base64,'+(await fs.readFile(p)).toString('base64')])));
const image=(key,x,y,w,h)=>`<image href="${logos[key]}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"/>`;
const text=(s,x,y,size=30,color='#123c70',extra='')=>`<text x="${x}" y="${y}" fill="${color}" font-family="Arial, sans-serif" font-size="${size}" font-weight="800" text-anchor="middle" ${extra}>${s}</text>`;
const rect=(x,y,w,h,r,fill,stroke='none',sw=0)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const shell=(s)=>`<svg xmlns="http://www.w3.org/2000/svg" width="600" height="760" viewBox="0 0 600 760">${s}</svg>`;
const navy='#123c70',cyan='#00abc1',ink='#11171c';
const designs=[
 ['01-matro-mavi', 'MATRO / Mavi kimlik',shell(
 rect(18,18,564,724,100,'white',navy,4)+
 '<path d="M85 600H515" stroke="#00abc1" stroke-width="5"/>'+
 image('blue',100,58,400,400)+text('MATRO',300,566,82)+
 text('BİRLİKTE ÜRETİYORUZ',300,654,24)+text('BURSA',300,697,17,navy,'letter-spacing="8"'))],
 ['02-matro-gece', 'MATRO / Gece vardiyası',shell(
 rect(18,18,564,724,70,'white')+rect(28,28,544,704,62,navy)+
 image('white',100,58,400,400)+text('MATRO',300,550,82,'white')+
 rect(90,590,420,62,12,cyan)+text('GECE VARDİYASI',300,632,28,navy)+
 text('ATÖLYE AÇIK. FİKİRLER AÇIK.',300,699,19,'white'))],
 ['03-matro-siyah', 'MATRO / Üretim etiketi',shell(
 '<path d="M60 20H490L580 110V690L530 740H20V60Z" fill="white" stroke="#11171c" stroke-width="4"/>'+
 image('black',105,60,390,390)+
 rect(55,487,490,113,0,ink)+text('MATRO',300,573,88,'white')+
 text('ÇİZ / ÜRET / TEST ET',300,655,28,ink)+
 text('FİKİRDEN PROTOTİPE',300,705,19,ink,'letter-spacing="3"'))],
 ['04-btu-matro', 'MATRO / BTÜ kimliği',shell(
 rect(18,18,564,724,32,'white',navy,4)+
 image('btu',145,50,310,204)+
 '<path d="M90 292H510" stroke="#d7e6ed" stroke-width="2"/>'+
 image('blue',185,330,230,230)+
 text('MATRO',300,653,76)+text('AYNI KAMPÜS. ORTAK MERAK.',300,706,20))],
 ['05-teknofest-matro', 'MATRO / TEKNOFEST saha etiketi',shell(
 '<path d="M100 18H500L580 100V706Q580 742 544 742H56Q20 742 20 706V100Z" fill="white" stroke="#123c70" stroke-width="4"/>'+
 '<circle cx="300" cy="70" r="15" fill="none" stroke="#123c70" stroke-width="5"/>'+
 image('tf',42,116,516,430)+
 rect(48,559,504,109,14,navy)+text('MATRO',300,642,79,'white')+
 text('ATÖLYEDEN SAHAYA',300,707,24,navy))],
 ['06-matro-devrede', 'MATRO / Devrede',shell(
 rect(18,18,564,724,70,'white',navy,4)+
 '<g stroke="#00abc1" stroke-width="5" fill="white"><path d="M60 90V290H100M540 90V290H500M60 670V550H98M540 670V550H502"/><circle cx="60" cy="90" r="9"/><circle cx="540" cy="90" r="9"/><circle cx="60" cy="670" r="9"/><circle cx="540" cy="670" r="9"/></g>'+
 image('blue',130,65,340,340)+
 text('MATRO',300,510,79)+rect(110,551,380,72,36,cyan)+
 text('DEVREDE',300,600,34,navy)+text('KOD + DEVRE + MEKANİK',300,684,22))],
];
for(const [id,,svg] of designs){
 await fs.writeFile(out+'/'+id+'.svg',svg);
 await sharp(Buffer.from(svg)).resize(1200,1520).png().toFile(out+'/'+id+'.png');
}
const composites=await Promise.all(designs.map(async ([id],i)=>({
 input:await sharp(out+'/'+id+'.png').resize(480,608).toBuffer(),left:30+(i%3)*510,top:30+Math.floor(i/3)*638
})));
await sharp({create:{width:1560,height:1306,channels:3,background:'#e8edf1'}}).composite(composites).png().toFile('public/media/stickers/06-kurumsal-seri.png');
await fs.writeFile(out+'/manifest.json',JSON.stringify({sources:paths,logoPolicy:'Kaynak PNG baytları değiştirilmeden SVG içine gömüldü. Logo yazıları yeniden yazılmadı.',items:designs.map(([id,title])=>({id,title,svg:id+'.svg',png:id+'.png'}))},null,2));
console.log('6 SVG, 6 PNG ve seri önizlemesi hazır.');
