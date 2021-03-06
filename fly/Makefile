# Assemble chr4 of fruit fly (Drosophila melanogaster)
# See https://support.10xgenomics.com/de-novo-assembly/datasets/2.1.0/fly
# and https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/performance

# Number of threads.
t=8

# Reference genome.
ref=fly

# Sample dataset
sample=f1chr4

# Compress in parallel.
ifneq ($(shell command -v pigz),)
gzip=pigz -p$t
zcat=pigz -p$t -cd
else
gzip=gzip
zcat=gunzip -c
endif

abyss_k=112

.DELETE_ON_ERROR:
.SECONDARY:

all:

# Assemble the chunks with SPAdes.
assemble-chunks-spades: \
	results/assemblies/f1chr4.00.spades.gfa.png \
	results/assemblies/f1chr4.01.spades.gfa.png \
	results/assemblies/f1chr4.02.spades.gfa.png \
	results/assemblies/f1chr4.03.spades.gfa.png \
	results/assemblies/f1chr4.04.spades.gfa.png \
	results/assemblies/f1chr4.05.spades.gfa.png \
	results/assemblies/f1chr4.06.spades.gfa.png \
	results/assemblies/f1chr4.07.spades.gfa.png \
	results/assemblies/f1chr4.08.spades.gfa.png \
	results/assemblies/f1chr4.09.spades.gfa.png \
	results/assemblies/f1chr4.10.spades.gfa.png \
	results/assemblies/f1chr4.11.spades.gfa.png \
	results/assemblies/f1chr4.12.spades.gfa.png \
	results/assemblies/f1chr4.13.spades.gfa.png \
	results/assemblies/f1chr4.14.spades.gfa.png \
	results/assemblies/f1chr4.15.spades.gfa.png \
	results/assemblies/f1chr4.16.spades.gfa.png \
	results/assemblies/f1chr4.17.spades.gfa.png \
	results/assemblies/f1chr4.18.spades.gfa.png \
	results/assemblies/f1chr4.19.spades.gfa

# Assemble the chunks with Unicycler.
assemble-chunks-unicycler: \
	results/assemblies/f1chr4.00.unicycler.gfa.png \
	results/assemblies/f1chr4.01.unicycler.gfa.png \
	results/assemblies/f1chr4.02.unicycler.gfa.png \
	results/assemblies/f1chr4.03.unicycler.gfa.png \
	results/assemblies/f1chr4.04.unicycler.gfa.png \
	results/assemblies/f1chr4.05.unicycler.gfa.png \
	results/assemblies/f1chr4.06.unicycler.gfa.png \
	results/assemblies/f1chr4.07.unicycler.gfa.png \
	results/assemblies/f1chr4.08.unicycler.gfa.png \
	results/assemblies/f1chr4.09.unicycler.gfa.png \
	results/assemblies/f1chr4.10.unicycler.gfa.png \
	results/assemblies/f1chr4.11.unicycler.gfa.png \
	results/assemblies/f1chr4.12.unicycler.gfa.png \
	results/assemblies/f1chr4.13.unicycler.gfa.png \
	results/assemblies/f1chr4.14.unicycler.gfa.png \
	results/assemblies/f1chr4.15.unicycler.gfa.png \
	results/assemblies/f1chr4.16.unicycler.gfa.png \
	results/assemblies/f1chr4.17.unicycler.gfa.png \
	results/assemblies/f1chr4.18.unicycler.gfa.png \
	results/assemblies/f1chr4.19.unicycler.gfa.png

# Visualize the chunks assembled with Unicycler using Bandage.
bandage-chunks-unicycler:
	for i in results/assemblies/f1chr4.??.unicycler.gfa; do \
		Bandage load $$i --draw --colour blastrainbow --query flychr4.fa & \
	done

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
f1chr4.orig.fq.gz:
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
# ASSEMBLIES
unicycler: results/assemblies/$(sample).unicycler.fa results/assemblies/$(sample).unicycler.gfa
spades: results/assemblies/$(sample).spades.contigs.fa results/assemblies/$(sample).spades.fastg
abyss: results/assemblies/$(sample).abyss.contigs.fa results/assemblies/$(sample).abyss.contigs.gfa
unicycler-arcs: results/arcs-abyss-scaffold/$(sample).unicycler.fa
spades-arcs: results/arcs-abyss-scaffold/$(sample).spades.contigs.fa results/arcs-abyss-scaffold/$(sample).spades.scaffolds.fa
abyss-arcs: results/arcs-abyss-scaffold/$(sample).abyss.contigs.fa results/arcs-abyss-scaffold/$(sample).abyss.scaffolds.fa


################################################################################
# Unicycler

# Assembled paired-end reads using Unicycler.
results/assemblies/%.unicycler.fa: %.1.fq.gz %.2.fq.gz
	mkdir -p working
	unicycler -t $t --mode bold -o working/$*.unicycler -1 $*.1.fq.gz -2 $*.2.fq.gz 1> working/$*.unicycler.log 2>&1
	mkdir -p results/assemblies
	seqtk seq working/$*.unicycler/assembly.fasta > $@

# link the graph format
results/assemblies/%.unicycler.gfa: results/assemblies/%.unicycler.fa
	ln -sf ../../working/$*.unicycler/assembly.gfa $@

# Reassemble paired-end reads and chunked contigs using Unicycler.
%.unicycler.gfa: %.fa f1chr4.1.fq.gz f1chr4.2.fq.gz
	unicycler -t $t --mode bold -o $*.unicycler -1 f1chr4.1.fq.gz -2 f1chr4.2.fq.gz --long $<

################################################################################
# spades

# Assembled paired-end reads using spades.
results/assemblies/%.spades.contigs.fa: %.1.fq.gz %.2.fq.gz
	mkdir -p working
	spades.py -t $t -1 $*.1.fq.gz -2 $*.2.fq.gz -o working/$*.spades 1> working/$*.spades.log 2>&1
	mkdir -p results/assemblies
	seqtk seq working/$*.spades/contigs.fasta > $@
	seqtk seq working/$*.spades/scaffolds.fasta > results/assemblies/$*.spades.scaffolds.fa

results/assemblies/%.spades.fastg: results/assemblies/%.spades.contigs.fa
	ln -sf ../../working/$*.spades/assembly_graph.fastg $@

results/assemblies/%.spades.gfa: results/assemblies/%.spades.contigs.fa
	ln -sf ../../working/$*.spades/assembly_graph_with_scaffolds.gfa $@

################################################################################
# abyss

# Assembled paired-end reads using abyss.
results/assemblies/%.abyss.contigs.fa: %.1.fq.gz %.2.fq.gz
	mkdir -p working/$*.abyss
	abyss-pe np=$t name=assembly graph=gfa k=$(abyss_k) in='../../$*.1.fq.gz ../../$*.2.fq.gz' -C working/$*.abyss 1> working/$*.abyss.log 2>&1
	mkdir -p results/assemblies
	seqtk seq working/$*.abyss/assembly-contigs.fa > $@
	seqtk seq working/$*.abyss/assembly-scaffolds.fa > results/assemblies/$*.abyss.scaffolds.fa

results/assemblies/%.abyss.contigs.gfa: results/assemblies/%.abyss.contigs.fa
	ln -sf ../../working/$*.abyss/assembly-contigs.gfa $@
	ln -sf ../../working/$*.abyss/assembly-scaffolds.gfa results/assemblies/$*.abyss.scaffolds.gfa

################################################################################
# ARCS

# results/arcs-abyss-scaffold/%.digit.fa: results/assemblies/%.fa
# 	mkdir -p working/arcs-abyss-scaffold/
# 	seqtk rename $< > $@

results/arcs-abyss-scaffold/%.fa: results/assemblies/%.fa
	mkdir -p working/arcs-abyss-scaffold
	$(eval lr_l=50)
	$(eval arcs_c=2)
	$(eval arcs_d=0)
	$(eval arcs_e=30000)
	$(eval arcs_l=0)
	$(eval arcs_m=4-20000)
	$(eval arcs_r=0.05)
	$(eval arcs_s=98)
	$(eval arcs_z=500)
	$(eval lr_s=1000-100000)
	$(eval lr_n=5-20)
	abyss-map-ssq -j$t -l$(lr_l) f1chr4.fq.gz $< | abyss-fixmate-ssq --all --qname -l$(lr_l) | gzip > working/arcs-abyss-scaffold/$*.lr.sortn.sam.gz
	gunzip -c working/arcs-abyss-scaffold/$*.lr.sortn.sam.gz | arcs -c$(arcs_c) -d$(arcs_d) -e$(arcs_e) -l$(arcs_l) -m$(arcs_m) -r$(arcs_r) -s$(arcs_s) -z$(arcs_z) -g working/arcs-abyss-scaffold/$*.arcs.dist.gv --tsv=working/arcs-abyss-scaffold/$*.arcs.tsv --barcode-counts=working/arcs-abyss-scaffold/$*.arcs.barcode-counts.tsv /dev/stdin
	abyss-scaffold --SS -k$(abyss_k) -s$(lr_s) -n$(lr_n) -g working/arcs-abyss-scaffold/$*.arcs.path.dot working/arcs-abyss-scaffold/$*.arcs.dist.gv > working/arcs-abyss-scaffold/$*.arcs.path
	MergeContigs -k$(abyss_k) -o working/arcs-abyss-scaffold/$*.arcs.fa $< working/arcs-abyss-scaffold/$*.arcs.path
	mkdir -p results/arcs-abyss-scaffold
	ln -sf ../../working/arcs-abyss-scaffold/$*.arcs.fa $@

################################################################################
# QUAST

# Compute assembly metrics of one assembly using QUAST.
%.quast.tsv: flychr4.fa %.fa
	quast -se --fast --scaffold-gap-max-size 100000 -t $t -o $*.quast -r $^
	ln -s $*.quast/transposed_report.tsv $@

# Compute assembly metrics of multiple assemblies using QUAST.
results/quast/quast-%/report.txt: results/assemblies/%.abyss.contigs.fa results/assemblies/%.spades.contigs.fa results/assemblies/%.unicycler.fa results/arcs-abyss-scaffold/%.abyss.contigs.fa results/arcs-abyss-scaffold/%.spades.contigs.fa results/arcs-abyss-scaffold/%.unicycler.fa 
	mkdir -p results/quast/quast-$*
	quast.py --eukaryote -t $t -o results/quast/quast-$* -r flychr4.fa -l abyss-contig,spades-contigs,abyss,spades,unicycler,abyss-contig-arcs,spades-contigs-arcs,abyss-arcs,spades-arcs,unicycler-arcs results/assemblies/$*.abyss.contigs.fa results/assemblies/$*.spades.contigs.fa results/assemblies/$*.abyss.scaffolds.fa results/assemblies/$*.spades.scaffolds.fa results/assemblies/$*.unicycler.fa results/arcs-abyss-scaffold/$*.abyss.contigs.fa results/arcs-abyss-scaffold/$*.spades.contigs.fa results/arcs-abyss-scaffold/$*.abyss.scaffolds.fa results/arcs-abyss-scaffold/$*.spades.scaffolds.fa results/arcs-abyss-scaffold/$*.unicycler.fa 

# Aggregate QUAST reports.
f1chr4.quast.tsv: \
		f1chr4.talr.spades.miniasm.quast.tsv \
		f1chr4.talr.unicycler.miniasm.quast.tsv \
		f1chr4.unicycler.quast.tsv
	mlr --tsvlite cat $^ >$@
	mlr --tsvlite cut -f Assembly,NG50 $@ | column -t

################################################################################
# Bandage

# Render an assembly graph using Bandage to PNG.
%.gfa.png: %.gfa
	Bandage image $< $@

# Render an assembly graph using Bandage to SVG.
%.gfa.svg: %.gfa
	Bandage image $< $@

################################################################################
# minimap2

# Align a FASTA file to the reference genome and produce a PAF file.
%.$(ref).paf.gz: $(ref).fa %.fa
	$(time) minimap2 -t$t -xasm10 $^ | $(gzip) >$@

# Align a FASTA file to the reference genome and produce a SAM file.
%.$(ref).sam.gz: $(ref).fa %.fa
	$(time) minimap2 -t$t -xasm10 -a $^ | $(gzip) >$@

# Overlap sequences with Minimap2 and produce a PAF file.
%.minimap2.paf.gz: %.fa
	$(time) minimap2 -t$t -xava-ont $< $< | $(gzip) >$@

################################################################################
# Talr

# Recompress the gzip file using bgzip.
%.fq.gz: %.orig.fq.gz
	gunzip -c $< | bgzip -@$t >$@

# Index a bgzip file.
%.gz.gzi: %.gz
	bgzip -r $<

# Index a bgzipped FASTQ file.
%.fq.gz.bdx: %.fq.gz %.fq.gz.gzi
	../bin/index_barcodes.py $<

# Split a Physlr fleshed-out backbone path into equal-sized chunks.
%.fleshed.talr.path: %.fleshed.path
	../bin/chunk_fleshed_backbone.py $< 20 0.5 >$@

# Split a chunked path file into one line per chunk.
%.00.path: %.path
	gsplit -l1 -d --additional-suffix=.path $< $*.

# Extract the reads of each chunk.
%.00.fq.gz: %.backbone.fleshed.talr.00.path %.fq.gz.bdx
	awk '{ printf "-" } END { printf "\r" }' $*.backbone.fleshed.talr.??.path; \
	set -e; \
	for i in $$(awk '{printf "%02d\n", NR-1}' $*.backbone.fleshed.talr.??.path); do \
		../bin/get_barcode_reads.py $*.fq.gz <$*.backbone.fleshed.talr.$$i.path | $(gzip) >$*.$$i.fq.gz; \
		printf "="; \
	done
	echo

################################################################################
# Concatenate chunked assemblies

# Concatenate chunked SPAdes assemblies.
f1chr4.talr.spades.fa: \
		results/assemblies/f1chr4.00.spades.scaffolds.fa \
		results/assemblies/f1chr4.01.spades.scaffolds.fa \
		results/assemblies/f1chr4.02.spades.scaffolds.fa \
		results/assemblies/f1chr4.03.spades.scaffolds.fa \
		results/assemblies/f1chr4.04.spades.scaffolds.fa \
		results/assemblies/f1chr4.05.spades.scaffolds.fa \
		results/assemblies/f1chr4.06.spades.scaffolds.fa \
		results/assemblies/f1chr4.07.spades.scaffolds.fa \
		results/assemblies/f1chr4.08.spades.scaffolds.fa \
		results/assemblies/f1chr4.09.spades.scaffolds.fa \
		results/assemblies/f1chr4.10.spades.scaffolds.fa \
		results/assemblies/f1chr4.11.spades.scaffolds.fa \
		results/assemblies/f1chr4.12.spades.scaffolds.fa \
		results/assemblies/f1chr4.13.spades.scaffolds.fa \
		results/assemblies/f1chr4.14.spades.scaffolds.fa \
		results/assemblies/f1chr4.15.spades.scaffolds.fa \
		results/assemblies/f1chr4.16.spades.scaffolds.fa \
		results/assemblies/f1chr4.17.spades.scaffolds.fa \
		results/assemblies/f1chr4.18.spades.scaffolds.fa \
		results/assemblies/f1chr4.19.spades.scaffolds.fa
	cat $^ | seqtk rename >$@

# Concatenate chunked Unicycler assemblies.
f1chr4.talr.unicycler.fa: \
		results/assemblies/f1chr4.00.unicycler.fa \
		results/assemblies/f1chr4.01.unicycler.fa \
		results/assemblies/f1chr4.02.unicycler.fa \
		results/assemblies/f1chr4.03.unicycler.fa \
		results/assemblies/f1chr4.04.unicycler.fa \
		results/assemblies/f1chr4.05.unicycler.fa \
		results/assemblies/f1chr4.06.unicycler.fa \
		results/assemblies/f1chr4.07.unicycler.fa \
		results/assemblies/f1chr4.08.unicycler.fa \
		results/assemblies/f1chr4.09.unicycler.fa \
		results/assemblies/f1chr4.10.unicycler.fa \
		results/assemblies/f1chr4.11.unicycler.fa \
		results/assemblies/f1chr4.12.unicycler.fa \
		results/assemblies/f1chr4.13.unicycler.fa \
		results/assemblies/f1chr4.14.unicycler.fa \
		results/assemblies/f1chr4.15.unicycler.fa \
		results/assemblies/f1chr4.16.unicycler.fa \
		results/assemblies/f1chr4.17.unicycler.fa \
		results/assemblies/f1chr4.18.unicycler.fa \
		results/assemblies/f1chr4.19.unicycler.fa
	cat $^ | seqtk rename >$@

################################################################################
# miniasm

# Assemble long reads with Miniasm.
%.miniasm.gfa: %.fa %.minimap2.paf.gz
	miniasm -1 -2 -c1 -e1 -f $^ >$@

# Convert GFA to FASTA.
%.miniasm.fa: %.miniasm.gfa
	awk '/^S/ { print ">" $$2 " " $$4 "\n" $$3 }' $< >$@
