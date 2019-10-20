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
step_size = int((1 - overlap_ratio) * chunk_size)

chunkss = []
for backbone in fleshed_backbones:
    chunkss.append(
        [
            backbone[i : i + chunk_size]
            for i in range(0, len(backbone), step_size)
            if i + chunk_size < total
        ]
    )

for chunks in chunkss:
    for chunk in chunks:
        out_list = [m.split("_")[0] for m in chunk]
        out_line = " ".join(out_list)
        sys.stdout.write(out_line + "\n")
