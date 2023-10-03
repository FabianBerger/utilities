# Utilities Repository

This repository contains a collection of utility scripts for various purposes. Each script is designed to perform a specific task or solve a particular problem. Feel free to explore and use these utilities for your own projects.

## List of Utilities

- **Create Clusters for Many Body Expansion**: `get_many-body_clusters.py` - A script to create POSCAR files (VASP file format) for many body expansions.
- **Create VASP POTCAR files**: `get_POTCAR.py` - A script to create POTCAR files (VASP file format).
- **Add Adsorbates to Dopant Site of Single Atom Alloy Slabs (VASP POSCAR format)**: `add_adsorbate.py` - A script to add adsorbates (Hydrogen, Carbon Monoxide, water, OH or CH3) to dopant site of single atom alloy slabs in VASP POSCAR format.



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



## Generate VASP POTCAR Files

The `get_POTCAR.py` script is a versatile tool designed to facilitate the generation of VASP POTCAR (Projector Augmented Wave Pseudopotential) files for use in VASP calculations. It offers flexibility by allowing users to specify PAW (PAW potentials) settings and the location of PAW potentials. The script constructs the POTCAR file based on the chemical elements present in the input POSCAR or CONTCAR file.

### Features

- **PAW Settings**: You can select from various PAW settings to customize the POTCAR file according to your specific calculation needs.

- **User-Defined PAW Location**: Specify the directory containing PAW potentials to ensure compatibility with your local setup.

- **Automatic Element Mapping**: The script automatically reads the chemical elements from the 6th line of the input POSCAR or CONTCAR file and maps them to the corresponding PAW potentials based on your chosen PAW settings.

- **Appending to Existing POTCAR**: It can append selected PAW potentials to an existing POTCAR file, allowing you to maintain a comprehensive library of PAW potentials.

### Usage

To utilize the `get_POTCAR.py` script, follow these simple steps:

1. Ensure that you have a valid input POSCAR or CONTCAR file in the current directory.

2. Run the script from the command line with the desired options:

```bash
python get_POTCAR.py [--paw_setting PAW_SETTING] [--paw_location PAW_LOCATION]
```



## Add Adsorbates to VASP POSCAR

The `add_adsorbate.py` script allows you to add adsorbates (Hydrogen, Carbon Monoxide, water, OH or CH3) to the dopant atom of single atom ally slabs in VASP POSCAR format. It offers the flexibility to specify the type of adsorbate and the distance above the unique atom where the adsorbate will be added.

### Features

- Supports three types of adsorbates: Hydrogen (H), Carbon Monoxide (CO), Water (H2O), Hydroxyl (OH), or Methyl groups (CH3).
- Customizable distance above the unique atom for adsorbate placement.
- Renames the modified structure file appropriately.

### Usage

To add an adsorbate to a VASP POSCAR file, run the script with the following command:

```bash
python add_adsorbate.py --input_file [POSCAR_file] --adsorbate_type [adsorbate_type] --distance_above [distance_above]
```

