#!/bin/bash
# MATRO Tanışma Kahvaltısı Reels/Hikâye: 3 Omni çekimi + yazı katmanları + Zeki'nin klon sesi (20 sn, 1080x1920, 30 fps)
cd /tmp/reels
ffmpeg -loglevel error -y \
 -ss 0 -t 4.8 -i c2.mp4 -ss 0 -t 8.0 -i c1.mp4 -ss 0.5 -t 7.9 -i c3.mp4 \
 -loop 1 -t 20 -i l0-sis.png -loop 1 -t 20 -i l0-logo.png -loop 1 -t 20 -i l1-baslik.png -loop 1 -t 20 -i l2-bilgi.png -loop 1 -t 20 -i l3-son.png \
 -i ses.mp3 -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[a];\
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[b];\
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[c];\
[a][b]xfade=transition=fade:duration=0.4:offset=4.4[ab];[ab][c]xfade=transition=slideleft:duration=0.4:offset=11.6[v0];\
[3:v]format=rgba,fade=t=in:st=0.1:d=0.5:alpha=1[s0];[4:v]format=rgba,fade=t=in:st=0.3:d=0.5:alpha=1[s1];\
[5:v]format=rgba,fade=t=in:st=4.7:d=0.4:alpha=1,fade=t=out:st=11.4:d=0.35:alpha=1[s2];\
[6:v]format=rgba,fade=t=in:st=7.8:d=0.4:alpha=1,fade=t=out:st=11.4:d=0.35:alpha=1[s3];\
[7:v]format=rgba,fade=t=in:st=12.1:d=0.6:alpha=1[s4];\
[v0][s0]overlay=0:0[v1];[v1][s1]overlay=0:0[v2];[v2][s2]overlay=0:0[v3];[v3][s3]overlay=0:0[v4];[v4][s4]overlay=0:0,format=yuv420p[v];\
[8:a]adelay=300|300,apad=whole_dur=20,afade=t=out:st=19.2:d=0.8,loudnorm=I=-14:TP=-1.5[au]" \
 -map "[v]" -map "[au]" -t 20 -c:v libx264 -crf 19 -preset veryfast -c:a aac -b:a 160k -movflags +faststart matro-tanisma-kahvaltisi-reels.mp4
echo bitti
