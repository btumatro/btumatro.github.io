#!/usr/bin/env python3
"""Birleştirilen sinematik klip örneğini şarkının takım adları bölümüne oturtur."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO = ROOT / 'videolar'
SONG = ROOT.parents[1] / 'ses' / '03-atolyeden-goklere.mp4'
OUT = ROOT / 'klip-ornek-01.mp4'
names = ['ashina-sinematik', 'lodos-sinematik', 'prusa-sinematik', 'zemheri-sinematik', 'matris-sinematik']
dur = 4.2
fade = 0.18
args = ['ffmpeg', '-y']
for name in names:
    args += ['-i', str(VIDEO / f'{name}-omni.mp4')]
args += ['-ss', '90.667', '-i', str(SONG)]
filters = []
for i in range(len(names)):
    filters.append(
        f'[{i}:v]trim=start=0.25:duration={dur},setpts=PTS-STARTPTS,'
        'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,'
        'fps=24,setsar=1,eq=contrast=1.035:saturation=0.97:brightness=0.003'
        f'[v{i}]'
    )
prev = 'v0'
offset = dur - fade
for i in range(1, len(names)):
    dest = f'x{i}'
    filters.append(f'[{prev}][v{i}]xfade=transition=fade:duration={fade}:offset={offset:.3f}[{dest}]')
    prev = dest
    offset += dur - fade
graph = ';'.join(filters)
args += ['-filter_complex', graph, '-map', f'[{prev}]', '-map', '5:a:0', '-t', '20.28',
         '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(OUT)]
subprocess.run(args, check=True)
print(f'Üretildi: {OUT}')
