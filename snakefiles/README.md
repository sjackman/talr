# Snakefile
This repository contains snakefiles running specific portions of pipelines that
may need to be repeated frequently with different parameters. The usage pattern
is:
1. Copy snakefile to empty working directory as `Snakefile`
2. Set up `config.json` with parameters specific to snakefile
3. Run pipeline

# backbone_path.snake
This snakefile is for generating the `.backbone.fleshed.path` file.

## Required parameters
Key | Description
--- | ---
`physlr_root` | path to your physlr repo
`reads` | path to the reads that you wish to run through physlr

# read_extract.snake
This snakefile is for extracting reads given a `.backbone.fleshed.path` file.

## Required parameters
Key | Description
--- | ---
`physlr_root` | path to your physlr repo
`talr_root` | path to your talr repo
`fleshed_path` | path to the `.backbone.fleshed.path` file that you want to use


