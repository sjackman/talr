# TALR: Targeted Assembly of Linked Reads

Hackseq 2019 Project 6
<https://www.hackseq.com/hackseq19#descriptions>

- @sjackman Shaun Jackman (team lead)
- @afshinfard Amirhossein Afshinfard
- @aliceZhu Alice Zhu
- @bernieyiweizhao Bernie Zhao
- @emreerhan Emre Erhan
- @gapalm Liubov Gapa
- @haghshenas Ehsan Haghshenas
- @schutzekatze Vladimir Nikolić
- @thezange Aleksis Korhonen
- @trgibbons Ted Gibbons

# Description

Linked reads from 10x Genomics combine the benefits of large DNA molecules with the sequence fidelity and cost of short read sequencing. We will design a software tool to extract the reads from a set of linked read barcodes and assemble those reads. Multiple targeted assemblies will be combined to assemble an entire chromosome.

# Background

Linked read sequencing is a library preparation technique used prior to short read DNA sequencing. Large DNA molecules are isolated using microfluidics, so that reads that are derived from the same large DNA molecule are associated with the same barcode. A barcode is a 16 nucleotide sequence for 10x Genomics Chromium linked read sequencing.

- Physlr Poster: Physlr: Construct a physical map from linked reads <https://f1000research.com/posters/8-1310>
- Physlr GitHub repo: <https://github.com/bcgsc/physlr>
- What are linked reads? <https://www.10xgenomics.com/linked-reads/>

# Pipeline

1. Use Physlr to construct a physical map of the linked reads, which is an ordered list of barcodes.
2. Identify a set of barcodes that covers a region of 100 to 200 kbp.
3. Collect the reads from that set barcodes.
4. Assemble those reads using a standard short read assembler.
5. Repeat steps two through five for a tiling path of adjacent, overlapping regions.
6. Combine these targeted subassemblies using a standard long read assembler.

# Tasks

For a list of tasks, see <https://github.com/sjackman/talr/issues/1>

# Install Software

Install Homebrew on macOS (<https://brew.sh>) and Linux (<https://docs.brew.sh/linux>).

```sh
mkdir -p ~/work
cd ~/work
git clone https://github.com/sjackman/talr
cd ~/work/talr
brew bundle
git clone https://github.com/bcgsc/physlr
cd ~/work/talr/physlr
brew bundle
```

# Download Data

Our toy data set is the linked reads from chromosome 4 (chr4) of fruit fly (*Drosophila melanogaster*). These chr4 reads are extracted from a shotgun sequencing data set provided by 10x Genomics by aligning the full data set to the reference genome and keeping only those reads that align to chr4.

See <https://support.10xgenomics.com/de-novo-assembly/datasets/2.1.0/fly>
and <https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/performance>

```sh
cd ~/work/talr/fly
# Download the fly genome from NCBI.
make fly.fa.fai flychr4.fa.fai
# Download the Supernova assembly of the linked reads from 10x Genomics.
make f1.supernova.fa.fai
# Download the fly linked reads of chromosome 4.
make f1chr4.fq.gz
```

- How big is chr4?
- What's the depth of coverage of chr4?
- Which is the largest Supernova scaffold that maps to chr4? (hint: use [minimap2](https://github.com/lh3/minimap2))

# Assemble the fly linked reads using Unicycler

Unicycler is a genome sequence assembly tool. Its intended to be used to assemble a genome using both short reads and long reads. It can also be used to assemble only short reads (using [SPAdes](https://github.com/ablab/spades)) or assembly only long reads (using [miniasm](https://github.com/lh3/miniasm)). We have only short reads for this fly data set.

```sh
mkdir ~/work/talr/fly
cd ~/work/talr/fly
# Unicycler will take ~75 minutes.
nohup time make f1chr4.unicycler.gfa >f1chr4.unicycler.gfa.log
abyss-fac -t1000 -G1348131 f1chr4.unicycler/assembly.fasta
```

What is the NG50 of the [Unicycler](https://github.com/rrwick/Unicycler) assembly of f1chr4? [NG50](https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics) is a metric of genome sequence assembly contiguity.

# Visualize the assembly graph using Bandage

[Bandage](https://github.com/rrwick/Bandage) visualizes a genome sequence assembly graph in [GFA1](https://github.com/GFA-spec/GFA-spec/blob/master/GFA1.md) format. We can assess the quality (contiguity and correctness) of the genome assembly by visually inspecting an alignment of the reference genome to the genome assembly graph.

```sh
Bandage load f1chr4.unicycler.gfa
```

1. Draw graph
2. Build BLAST database
3. Load from FASTA file
4. Select `flychr4.fa`
5. Run BLAST search
6. Close

Do you see any major structural misassemblies? Look for discontiguities in the colour spectrum of a contig.

# Run Physlr on chr4

[Physlr](https://github.com/bcgsc/physlr) constructs a physical map (an ordered sequence of barcodes) using linked read sequencing.

```sh
# Compile Physlr.
make -C ~/work/talr/physlr/src CC=gcc-9 CXX=g++-9
pip_pypy3 install networkx pygraphviz tqdm
Rscript -e 'install.packages(c("tidyverse", "Polychrome"))'
# Run Physlr.
cd ~/work/talr/physlr/data
mkdir -p fly
ln -s ../../../fly/f1chr4.fq.gz fly/fly.f1.chr4.sortbxn.dropse.fq.gz
# Use the Ensembl reference genome rather than default NCBI reference genome.
make fly/fly.ensembl.chr.fa
ln -sf fly.ensembl.chr.fa fly/fly.fa
# Physlr will take ~10 minutes.
nohup time make t=4 ref=fly lr=f1chr4 draft=f1.supernova.scaftigs n=50 f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.path >f1chr4.k32-w32.n100-1000.c2-x.physlr.overlap.n50.mol.backbone.fleshed.path.log
```
