#!/bin/bash
# Yazısız, seslendirmesiz kurgu: aynı 3 çekim, aynı kesim; sessiz ses izi
cd "$(dirname "$0")"
ffmpeg -loglevel error -y -ss 0 -t 4.8 -i omni-c2-cay-dokme.mp4 -ss 0 -t 8.0 -i omni-c1-sofra-kusbakisi.mp4 -ss 0.5 -t 7.9 -i omni-c3-ogrenciler-masada.mp4 \
 -f lavfi -t 20 -i anullsrc=r=48000:cl=stereo -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[a];\
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[b];\
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[c];\
[a][b]xfade=transition=fade:duration=0.4:offset=4.4[ab];[ab][c]xfade=transition=slideleft:duration=0.4:offset=11.6,format=yuv420p[v]" \
 -map "[v]" -map 3:a -t 20 -c:v h264_videotoolbox -b:v 12M -c:a aac -b:a 128k -movflags +faststart ../reels-ham-sessiz-yazisiz.mp4
