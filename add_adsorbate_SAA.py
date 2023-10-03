#!/usr/bin/env python3

import argparse
import os
import shutil
from datetime import datetime
from ase import io, Atoms, Atom

def find_unique_element(structure):
    """
    Find the unique chemical element in the given structure.

    Args:
        structure (ase.Atoms): The atomic structure to analyze.

    Returns:
        str: The symbol of the unique element if found, None otherwise.
    """
    element_counts = structure.get_chemical_symbols()
    unique_elements = [element for element in set(element_counts) if element_counts.count(element) == 1]

    if len(unique_elements) != 1:
        print("Error: There should be exactly one unique element in the structure.")
        return None

    return unique_elements[0]

def find_unique_atom(structure, unique_element):
    """
    Find the index of the unique atom of a given element in the structure.

    Args:
        structure (ase.Atoms): The atomic structure to search.
        unique_element (str): The chemical symbol of the unique element.

    Returns:
        int: The index of the unique atom if found, None otherwise.
    """
    for i, atom in enumerate(structure):
        if atom.symbol == unique_element:
            return i
    return None

def add_hydrogen(structure, unique_atom_position, distance_above):
    """
    Add a hydrogen atom to the given atomic structure.

    Args:
        structure (ase.Atoms): The atomic structure to which hydrogen will be added.
        unique_atom_position (list): The position of the unique atom.
        distance_above (float): The distance above the unique atom where hydrogen will be added.

    Returns:
        ase.Atoms: The modified atomic structure with the added hydrogen atom.
    """
    hydrogen_position = unique_atom_position + [0.0, 0.0, distance_above]
    hydrogen_atom = Atom('H', position=hydrogen_position)

    # Create a new Atoms object containing both the original structure and the hydrogen atom
    structure.extend(hydrogen_atom)

    return structure

def add_carbon_monoxide(structure, unique_atom_position, distance_above):
    """
    Add a carbon monoxide molecule to the given atomic structure.

    Args:
        structure (ase.Atoms): The atomic structure to which CO will be added.
        unique_atom_position (list): The position of the unique atom.
        distance_above (float): The distance above the unique atom where CO will be added.

    Returns:
        ase.Atoms: The modified atomic structure with the added CO molecule.
    """
    carbon_position = unique_atom_position + [0.0, 0.0, distance_above]
    oxygen_position = unique_atom_position + [0.0, 0.0, distance_above + 1.2]

    co_molecule = Atoms([Atom('C', position=carbon_position),
                         Atom('O', position=oxygen_position)])

    structure.extend(co_molecule)
    return structure

def add_methyl_group(structure, unique_atom_position, distance_above):
    """
    Add a methyl group to the given atomic structure.

    Args:
        structure (ase.Atoms): The atomic structure to which the methyl group will be added.
        unique_atom_position (list): The position of the unique atom.
        distance_above (float): The distance above the unique atom where the methyl group will be added.

    Returns:
        ase.Atoms: The modified atomic structure with the added methyl group.
    """
    carbon_position = unique_atom_position + [0.0, 0.0, distance_above]
    hydrogen_positions = [
        unique_atom_position + [1, 0.0, distance_above + 0.5],
        unique_atom_position + [-0.5, 0.866, distance_above + 0.5],
        unique_atom_position + [-0.5, -0.866, distance_above + 0.5]
    ]

    ch3_group = Atoms([Atom('C', position=carbon_position)] + [Atom('H', position=p) for p in hydrogen_positions])

    structure.extend(ch3_group)
    return structure

def is_direct_format(poscar_file):
    """
    Check if a VASP POSCAR file is in "direct" format.

    Args:
        poscar_file (str): Path to the VASP POSCAR file.

    Returns:
        bool: True if the file is in "direct" format, False otherwise.
    """
    with open(poscar_file, 'r') as file:
        lines = file.readlines()
    return lines[8].strip().lower() == 'direct'

def backup_existing_file(file_path):
    """
    Rename an existing file with a timestamp.

    Args:
        file_path (str): Path to the existing file.

    Returns:
        str: The new name of the file with a timestamp.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
    backup_file = f"{file_path}.{timestamp}"
    os.rename(file_path, backup_file)
    return backup_file

def main():
    """
    The main function of the script.

    Parses command-line arguments, processes the specified VASP POSCAR file,
    adds the selected adsorbate to the atomic structure, and saves the modified
    structure to a new VASP POSCAR file with an appropriate name.

    Command Line Arguments:
        --input_file (str): Path to the input VASP POSCAR file.
        --adsorbate_type (str): Type of adsorbate to add (H for Hydrogen,
                                CO for Carbon Monoxide, CH3 for Methyl group),
                                case-insensitive.
        --distance_above (float): Distance above the unique atom where the
                                  adsorbate will be added (default: 1.8 Angstroms).

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Add adsorbate to a VASP POSCAR file")
    parser.add_argument("--input_file", default="POSCAR", help="Path to the input VASP POSCAR file")
    parser.add_argument("--adsorbate_type", help="Type of adsorbate to add (H for Hydrogen, CO for Carbon Monoxide, CH3 for Methyl group), case-insensitive")
    parser.add_argument("--distance_above", type=float, default=1.8, help="Distance above the unique atom where the adsorbate will be added (default: 1.8 Angstroms)")

    args = parser.parse_args()

    # Convert the adsorbate type to lowercase for case-insensitive comparison
    adsorbate_type_lower = args.adsorbate_type.lower()
    adsorbate_type_upper = args.adsorbate_type.upper()

    if adsorbate_type_lower == 'me':
         adsorbate_type_lower = 'ch3'
    if adsorbate_type_upper == 'ME':
         adsorbate_type_upper = 'CH3'

    # Check if the target file already exists
    target_file = f'POSCAR_{adsorbate_type_upper}'

    if os.path.exists(target_file):
        # Rename the existing file with a timestamp
        backup_file = backup_existing_file(target_file)
        print(f"Renamed existing {target_file} to {backup_file}")

    # Load the existing POSCAR file
    input_file = args.input_file
    is_input_direct = is_direct_format(input_file)
    structure = io.read(input_file, format='vasp')

    # Find the unique element and atom position
    unique_element = find_unique_element(structure)
    unique_atom_index = find_unique_atom(structure, unique_element)
    unique_atom_position = structure[unique_atom_index].position

    if adsorbate_type_lower == 'ch3':
        structure = add_methyl_group(structure, unique_atom_position, args.distance_above)
    elif adsorbate_type_lower == 'h':
        structure = add_hydrogen(structure, unique_atom_position, args.distance_above)
    elif adsorbate_type_lower == 'co':
        structure = add_carbon_monoxide(structure, unique_atom_position, args.distance_above)
    else:
        print("Invalid adsorbate choice. No modification made.")
        return

    # Rename the modified structure file
    io.write(target_file, structure, format='vasp', direct=is_input_direct)

if __name__ == "__main__":
    main()
