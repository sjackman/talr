# TALR: Targeted Assembly of Linked Reads

Hackseq 2019 Project 6
<https://www.hackseq.com/hackseq19#descriptions>

# Description

Linked reads from 10x Genomics combine the benefits of large DNA molecules with the sequence fidelity and cost of short read sequencing. We will design a software tool to extract the reads from a set of linked read barcodes and assemble those reads. Multiple targeted assemblies will be combined to assemble an entire chromosome.

# Background

- Physlr Poster: Physlr: Construct a physical map from linked reads <https://f1000research.com/posters/8-1310>
- Physlr GitHub repo: <https://github.com/bcgsc/physlr>
- What are linked reads? <https://www.10xgenomics.com/linked-reads/>

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
- Which is the largest Supernova scaffold that maps to chr4? (hint: use minimap2)

# Assemble the fly linked reads using Unicycler

```sh
mkdir ~/work/talr/fly
cd ~/work/talr/fly
# Unicycler will take ~75 minutes.
nohup time make f1chr4.unicycler.gfa >f1chr4.unicycler.gfa.log
abyss-fac -t1000 -G1348131 f1chr4.unicycler/assembly.fasta
```

What is the NG50 of the Unicycler assembly of f1chr4?

# Visualize the assembly graph using Bandage

```sh
Bandage load f1chr4.unicycler.gfa
```

1. Draw graph
2. Build BLAST database
3. Load from FASTA file
4. Select `flychr4.fa`
5. Run BLAST search
6. Close

Do you see any major structural misassemblies?

# Run Physlr on chr4

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
