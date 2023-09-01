# Utilities Repository

This repository contains a collection of utility scripts for various purposes. Each script is designed to perform a specific task or solve a particular problem. Feel free to explore and use these utilities for your own projects.

## List of Utilities

- **Create Clusters for Many Body Expansion**: `get_many-body_clusters.py` - A script to create POSCAR files (VASP file format) for many body expansions.



## Create Clusters for Many Body Expansion

This script is designed to process monomers and create modified POSCAR files for for many body expansions. It simplifies the process of generating structes of monomers.

### Features

- Cleans and validates input monomers data.
- Generates POSCAR files for various body order terms.
- Handles comments and ensures only valid characters are used.

### Usage

To use the Monomer Processor script, run it from the command line with the following arguments:

```bash
python get_many-body_clusters.py [body_order] [CONTCAR_filename] [monomers_filename]
```
