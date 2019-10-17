# TALR: Targeted Assembly of Linked Reads

.DELETE_ON_ERROR:
.SECONDARY:

all: physlr/src/physlr-indexlr
	make -C fly fly.fa.fai flychr4.fa.fai f1.supernova.fa.fai f1chr4.fq.gz

install-deps: physlr/README.md
	brew bundle
	cd physlr && brew bundle
	pip_pypy3 install networkx pygraphviz tqdm
	Rscript -e 'install.packages(c("tidyverse", "Polychrome"))'

physlr/README.md:
	git clone https://github.com/bcgsc/physlr

physlr/src/physlr-indexlr: physlr/README.md
	make -C ~/work/talr/physlr/src CC=gcc-9 CXX=g++-9
