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
One could think of improving assemblies obtained from non-LR-aware assemblers by scaffolding them using linked reads. This can be done using [ARCS](https://github.com/bcgsc/arcs) which is designed specifically to scaffold draft assemblies using linked reads. These assemblies can be obtained by running the following commands:
```
make results/arcs-abyss-scaffold/f1chr4.unicycler.fa
make results/arcs-abyss-scaffold/f1chr4.spades.contigs.fa
make results/arcs-abyss-scaffold/f1chr4.spades.scaffolds.fa
make results/arcs-abyss-scaffold/f1chr4.abyss.contigs.fa
make results/arcs-abyss-scaffold/f1chr4.abyss.scaffolds.fa
```

### LR-aware assemblers

## Assessment of assemblies
We can use QUAST to compare TALR with other assemblies generated above. This can be easily done using the following command:

```
make results/quast/quast-f1chr4/report.txt
```

Here is a summary of the results for `chr4` of the Fruit Fly genome.

|                | NGA50  | Quast-misassemblies |
|----------------|--------|---------------------|
| ABySS          | 50548  | 4                   |
| SPAdes         | 77426  | 5                   |
| Unicycler      | 53909  | 5                   |
| ABySS+ARCS     | 88659  | 10                  |
| SPAdes+ARCS    | 172052 | 11                  |
| Unicycler+ARCS | 137285 | 9                   |

