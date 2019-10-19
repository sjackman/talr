import sys
# file=open("../f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.path", mode='r')
#file_fleshed_backbones = "../f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.path"#sys.argv[1]
file_fleshed_backbones = sys.argv[1]
chunks_count = int(sys.argv[2])
overlap_ratio = float(sys.argv[3])

file = open(file_fleshed_backbones, mode='r')
all = file.read()
file.close()
lines = all.splitlines()
fleshed_backbones=[]
for line in lines:
    fleshed_backbones.append(line.replace(',', ' ').replace(')', ' ').replace('(', ' ').split())

total=sum(len(i) for i in fleshed_backbones)
b_per_c = int(total / (overlap_ratio * (chunks_count - 1)))
overlap = int(overlap_ratio*b_per_c)
chunkss =[]
for backbone in fleshed_backbones:
    chunkss.append([backbone[i:i+b_per_c] for i in range(0, len(backbone), b_per_c-overlap)])
for chunks in chunkss:
    for chunk in chunks:
        for mol in chunk:
            print(mol.split("_")[0], end = ' ', file=sys.stdout)
        print(file=sys.stdout)
