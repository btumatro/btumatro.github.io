#!/bin/bash
# Yazısız, seslendirmesiz kurgu; Omni'nin kendi ortam sesleri geçişlerde çapraz kararmayla
cd "$(dirname "$0")"
ffmpeg -loglevel error -y -ss 0 -t 4.8 -i omni-c2-cay-dokme.mp4 -ss 0 -t 8.0 -i omni-c1-sofra-kusbakisi.mp4 -ss 0.5 -t 7.9 -i omni-c3-ogrenciler-masada.mp4 -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[a];\
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[b];\
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[c];\
[a][b]xfade=transition=fade:duration=0.4:offset=4.4[ab];[ab][c]xfade=transition=slideleft:duration=0.4:offset=11.6,format=yuv420p[v];\
[0:a]aresample=48000[x];[1:a]aresample=48000[y];[2:a]aresample=48000[z];[x][y]acrossfade=d=0.4[xy];[xy][z]acrossfade=d=0.4,afade=t=out:st=19.2:d=0.8,loudnorm=I=-16:TP=-1.5[au]" \
 -map "[v]" -map "[au]" -t 20 -c:v h264_videotoolbox -b:v 12M -c:a aac -b:a 160k -movflags +faststart ../reels-ham-omni-sesli.mp4
