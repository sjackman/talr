## Assembling linked reads
First, in order to have baseline assemblies to compare against TALR, we assemble 
linked-reads using both LR-aware and non-LR-aware assemblers.
For non-LR-aware assemblers we use ARCS to generate scaffolds using linked reads.

### non-LR-aware assemblers
We assemble linked reads using three different assemblers; Unicycler, SPAdes, and ABySS. 
The example below shows commands to do this for `chr4` of the Fruit Fly genome.

```
make results/assemblies/f1chr4.unicycler.fa
make results/assemblies/f1chr4.spades.contigs.fa
make results/assemblies/f1chr4.abyss.contigs.fa
```

We can also obtain these assemblies in graph fromats that can be visualized using Bandage as follows:
```
make results/assemblies/f1chr4.unicycler.gfa
make results/assemblies/f1chr4.spades.fastg
make results/assemblies/f1chr4.abyss.contigs.gfa
```

### Scaffolding assemblies using ARCS

### LR-aware assemblers

## Assessment of assemblies
We can use QUAST to compare TALR with other assemblies generated above. This can be easily done using the following command:

```
make results/quast/quast-f1chr4/report.txt
```

Here is a summary of the results for `chr4` of the Fruit Fly genome.

|           | NGA50 | Quast-misassemblies |
|-----------|-------|---------------------|
| ABySS     | 50548 | 4                   |
| SPAdes    | 77426 | 5                   |
| Unicycler | 53909 | 5                   |

