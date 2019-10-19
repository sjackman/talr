# Chunk fleshed_backbone
`chunk_fleshed_backbones.py` gives as input a) a fleshed backbone b) number of chunks, c) chunks overlap rations [0,1). It then subset the fleshed backone into chunks and output all barcodes of a chunk in a single line of a new file `*.chunked.path`

example: 
```angular2
pypy3 chunk_fleshed_backbone.py ../physlr/data/f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.path 20 0.5 > ../physlr/data/f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.chunked20.5.path
```

# Group reads based on fleshed_backbone
`chunk_reads_fleshed_backbones.py` gives as input a) the chunked fleshed_backbone made with the other script, b) an unzipped `.fq` reads format (with the bx attached to the read header); It extract and group the reads based on `*.chunked_fleshed_backbone.path` and output them into separate files in a directory with the same name as for the chunked_fleshed_backbone `+ "_reads/"`

example:

```angular2
pypy3 chunk_reads_fleshed_backbone.py ../f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.chunked20.5.path /projects/btl_scratch/aafshinfard/hackseq19/talr/fly/f1chr4_2.fq
``` 