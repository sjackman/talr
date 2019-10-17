# Assemble chr4 of fruit fly (Drosophila melanogaster)
# See https://support.10xgenomics.com/de-novo-assembly/datasets/2.1.0/fly
# and https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/performance

# Number of threads.
t=8

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
	ln -s $< $@

# Extract chr4 from the fly reference genome.
flychr4.fa: fly.ensembl.chr.fa
	samtools faidx $< 4 | seqtk seq >$@

# Download the fly gene annotation from Ensembl.
fly.gff:
	curl ftp://ftp.ensembl.org/pub/release-98/gff3/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.22.98.chr.gff3.gz | $(zcat) >$@

# Download the fly chr4 gene annotation from Ensembl.
flychr4.gff:
	curl ftp://ftp.ensembl.org/pub/release-98/gff3/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.22.98.chromosome.4.gff3.gz | $(zcat) >$@

# Download the Supernova assembly of the linked reads from 10x Genomics.
f1.supernova.fa:
	curl http://cf.10xgenomics.com/samples/assembly/2.1.0/fly/fly_pseudohap.fasta.gz | $(zcat) >$@

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

################################################################################
# Unicycler

# Assembled paired-end reads using Unicycler.
%.unicycler.gfa: %.1.fq.gz %.2.fq.gz
	unicycler -t$t --mode bold -o $*.unicycler -1 $*.1.fq.gz -2 $*.2.fq.gz
	ln -s $*.unicycler/assembly.gfa $@

# Copy the FASTA file.
%.unicycler.fa: %.unicycler.gfa
	seqtk seq $*.unicycler/assembly.fasta >$@

################################################################################
# minimap2

# Align a FASTA file to the reference genome and produce a PAF file.
%.$(ref).paf.gz: $(ref).fa %.fa
	$(time) minimap2 -t$t -xasm10 $^ | $(gzip) >$@

# Align a FASTA file to the reference genome and produce a SAM file.
%.$(ref).sam.gz: $(ref).fa %.fa
	$(time) minimap2 -t$t -xasm10 -a $^ | $(gzip) >$@
