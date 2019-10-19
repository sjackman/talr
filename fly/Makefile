# Assemble chr4 of fruit fly (Drosophila melanogaster)
# See https://support.10xgenomics.com/de-novo-assembly/datasets/2.1.0/fly
# and https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/performance

# Number of threads.
t=16

# Reference genome.
ref=fly

# Compress in parallel.
ifneq ($(shell command -v pigz),)
gzip=pigz -p$t
zcat=pigz -p$t -cd
else
gzip=gzip
zcat=gunzip -c
endif

.DELETE_ON_ERROR:
.SECONDARY:
all:

################################################################################
# Download data

# Download the fly genome from Ensembl.
fly.ensembl.fa:
	curl ftp://ftp.ensembl.org/pub/release-98/fasta/drosophila_melanogaster/dna/Drosophila_melanogaster.BDGP6.22.dna.toplevel.fa.gz | seqtk seq >$@

# Filter out the unplaced contigs from the fly genome.
fly.ensembl.chr.fa: fly.ensembl.fa
	paste - - <$< | sed 's/mitochondrion_genome/MT/' | egrep '^>(2L|2R|3L|3R|4|X|Y|MT) ' | tr '\t' '\n' >$@

# Symlink the reference genome.
fly.fa: fly.ensembl.chr.fa
	ln -sf $< $@

# Download the fly gene annotation from Ensembl.
fly.gff:
	curl ftp://ftp.ensembl.org/pub/release-98/gff3/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.22.98.chr.gff3.gz | $(zcat) >$@

# Download fly chr4 from Ensembl.
flychr4.fa:
	curl ftp://ftp.ensembl.org/pub/release-98/fasta/drosophila_melanogaster/dna/Drosophila_melanogaster.BDGP6.22.dna.chromosome.4.fa.gz | seqtk seq >$@

# Download the fly chr4 gene annotation from Ensembl.
flychr4.gff:
	curl ftp://ftp.ensembl.org/pub/release-98/gff3/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.22.98.chromosome.4.gff3.gz | $(zcat) >$@

# Download the Supernova assembly of the linked reads from 10x Genomics.
f1.supernova.fa:
	curl http://cf.10xgenomics.com/samples/assembly/2.1.0/fly/fly_pseudohap.fasta.gz | $(zcat) >$@

# Extract the chr4 scaffold from the Supernova assembly.
f1chr4.supernova.fa: f1.supernova.fa
	samtools faidx $< 49 | seqtk seq >$@

# Download the linked reads of chr4.
f1chr4.fq.gz:
	curl -O http://bcgsc.ca/downloads/btl/sjackman/f1chr4.fq.gz

################################################################################
# samtools

# Index a FASTA file.
%.fa.fai: %.fa
	samtools faidx $<

# Sort a SAM file by position.
%.sort.bam: %.sam.gz
	samtools sort -@$t -T$$(mktemp -u -t $(@F).XXXXXX) -o $@ $<

# Index a BAM file.
%.bam.bai: %.bam
	samtools index -@$t $<

################################################################################
# seqtk

# Select the first read of the read pair.
%.1.fq.gz: %.fq.gz
	seqtk dropse $< | seqtk seq -1 | $(gzip) >$@

# Select the second read of the read pair.
%.2.fq.gz: %.fq.gz
	seqtk dropse $< | seqtk seq -2 | $(gzip) >$@

# Cut scaffolds at Ns to create scaftigs.
%.scaftigs.fa: %.fa
	seqtk cutN -n1 $< | tr :- _ | seqtk seq >$@

################################################################################
# Unicycler

# Assembled paired-end reads using Unicycler.
results/assemblies/%.unicycler.gfa: %.1.fq.gz %.2.fq.gz
	mkdir -p working
	unicycler -t $t --mode bold -o working/$*.unicycler -1 $*.1.fq.gz -2 $*.2.fq.gz 1> working/$*.unicycler.log 2>&1
	mkdir -p results/assemblies
	ln -sf ../../working/$*.unicycler/assembly.gfa $@

# Copy the FASTA file.
results/assemblies/%.unicycler.fa: results/assemblies/%.unicycler.gfa
	seqtk seq working/$*.unicycler/assembly.fasta >$@

################################################################################
# spades

# Assembled paired-end reads using spades.
results/assemblies/%.spades.fastg: %.1.fq.gz %.2.fq.gz
	mkdir -p working
	spades.py -t $t -1 $*.1.fq.gz -2 $*.2.fq.gz -o working/$*.spades 1> working/$*.spades.log 2>&1
	mkdir -p results/assemblies
	ln -sf ../../working/$*.spades/assembly_graph.fastg $@

results/assemblies/%.spades.contigs.fa: results/assemblies/%.spades.fastg
	seqtk seq working/$*.spades/contigs.fasta > $@
	seqtk seq working/$*.spades/scaffolds.fasta > results/assemblies/$*.spades.scaffolds.fa

################################################################################
# abyss

# Assembled paired-end reads using abyss.
results/assemblies/%.abyss.contigs.fa: %.1.fq.gz %.2.fq.gz
	mkdir -p working/$*.abyss
	abyss-pe np=$t name=assembly graph=gfa k=112 in='../../$*.1.fq.gz ../../$*.2.fq.gz' -C working/$*.abyss 1> working/$*.abyss.log 2>&1
	mkdir -p results/assemblies
	seqtk seq working/$*.abyss/assembly-contigs.fa > $@
	seqtk seq working/$*.abyss/assembly-scaffolds.fa > results/assemblies/$*.abyss.scaffolds.fa

results/assemblies/%.abyss.contigs.gfa: results/assemblies/%.abyss.contigs.fa
	ln -sf ../../working/$*.abyss/assembly-contigs.gfa $@
	ln -sf ../../working/$*.abyss/assembly-scaffolds.gfa results/assemblies/$*.abyss.scaffolds.gfa

################################################################################
# quast
results/quast/quast-%/report.txt: results/assemblies/%.abyss.contigs.fa results/assemblies/%.spades.contigs.fa results/assemblies/%.unicycler.fa
	mkdir -p results/quast/quast-$*
	quast.py --eukaryote -t $t -o results/quast/quast-$* -r flychr4.fa -l abyss-contig,spades-contigs,abyss,spades,unicycler results/assemblies/$*.abyss.contigs.fa results/assemblies/$*.spades.contigs.fa results/assemblies/$*.abyss.scaffolds.fa results/assemblies/$*.spades.scaffolds.fa results/assemblies/$*.unicycler.fa

################################################################################
# minimap2

# Align a FASTA file to the reference genome and produce a PAF file.
%.$(ref).paf.gz: $(ref).fa %.fa
	$(time) minimap2 -t$t -xasm10 $^ | $(gzip) >$@

# Align a FASTA file to the reference genome and produce a SAM file.
%.$(ref).sam.gz: $(ref).fa %.fa
	$(time) minimap2 -t$t -xasm10 -a $^ | $(gzip) >$@
