#!/usr/bin/env python3

import sys

file_fleshed_backbones = sys.argv[1]
chunks_count = int(sys.argv[2])
overlap_ratio = float(sys.argv[3])

with open(file_fleshed_backbones, mode="r") as fin:
    all = fin.read()

lines = all.splitlines()
fleshed_backbones = []
for line in lines:
    fleshed_backbones.append(
        line.replace(",", " ").replace(")", " ").replace("(", " ").split()
    )

total = sum(len(i) for i in fleshed_backbones)
chunk_size = round(total / ((chunks_count - 1) * (1 - overlap_ratio) + 1))
step_size = (1 - overlap_ratio) * chunk_size

chunkss = []
for backbone in fleshed_backbones:
    offsets = (int(i * step_size) for i in range(0, chunks_count))
    chunkss.append([backbone[i : i + chunk_size] for i in offsets])

for chunks in chunkss:
    for chunk in chunks:
        print(*(m.rsplit("_")[0] for m in chunk))
