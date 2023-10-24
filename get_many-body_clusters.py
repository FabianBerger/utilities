#!/usr/bin/env python3
import sys
import os
from collections import OrderedDict
import argparse

"""
This script processes monomers and creates CONTCAR files for various body order terms.
It reads the contents of a CONTCAR file and a monomers file, checks the validity of atom indices,
and generates new CONTCAR files for different combinations of monomers based on the specified body order.

Usage:
    python script_name.py [body_order] [CONTCAR_filename] [monomers_filename]

Arguments:
    body_order (int, optional): The body order term to generate (default is 0 for full body).
    CONTCAR_filename (str, optional): The name of the CONTCAR file (default is "CONTCAR").
    monomers_filename (str, optional): The name of the monomers file (default is "monomers").

Functions:
    read_file(filename):
        Read the contents of a file.
    
    check_atom_indices(atom_indices, total_atoms):
        Check if atom indices are valid.
    
    clean_monomers_content(monomers_content):
        Process the monomers content to create a cleaned version.
    
    process_monomers(contcar_content, monomers_content):
        Process monomers data, check atom indices validity, and identify missing atoms.
    
    get_atomic_symbols(contcar_content, atom_indices):
        Get atomic symbols from atom indices.
    
    create_monomer_contcar_file(file_name, contcar_content, monomer):
        Create a new CONTCAR file for a monomer.
    
    main():
        Main function to process monomers and create CONTCAR files.

The script takes command-line arguments for specifying the body order term, CONTCAR filename, and monomers filename.
If no arguments are provided, it uses default values. The script generates CONTCAR files for different combinations
of monomers based on the specified body order and writes them as "POSCAR_i" files, where 'i' represents the monomer combination.

Author:
    Dr Fabian Berger

"""
# Define command-line arguments using argparse
def parse_args():
    parser = argparse.ArgumentParser(description="Process monomers and create CONTCAR files for various body order terms.")
    parser.add_argument("--body-order", type=int, default=0, help="The body order term to generate (default is 0 for full body).")
    parser.add_argument("--contcar", default="CONTCAR", help="The name of the CONTCAR file (default is 'CONTCAR').")
    parser.add_argument("--monomers", default="monomers", help="The name of the monomers file (default is 'monomers').")
    return parser.parse_args()

# Function to read the contents of a file
def read_file(filename):
    """
    Read the contents of a file.
    Args:
        filename (str): The name of the file to read.
    Returns:
        str: The contents of the file.
    If the file is not found, it prints an error message and returns None.
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

# Function to check if atom indices are valid
def check_atom_indices(atom_indices, total_atoms):
    """
    Check if atom indices are valid.
    Args:
        atom_indices (list of int): List of atom indices.
        total_atoms (int): Total number of atoms.
    Returns:
        bool: True if atom indices are valid, False otherwise.
    This function checks if atom indices are within the valid range and not duplicated.
    """
    # Create a set to keep track of seen atom indices
    seen_indices = set()
    # List to store repeated atom indices
    repeated_indices = []

    for atom_index in atom_indices:
        if atom_index in seen_indices:
            repeated_indices.append(atom_index)
        else:
            seen_indices.add(atom_index)

    # Check for duplicate atom indices
    if repeated_indices:
        print(f"Error: Atom indices {', '.join(map(str, repeated_indices))} are repeated in the monomers file.")
        return False

    # Check if any atom index exceeds the total number of atoms
    invalid_indices = [atom_index for atom_index in atom_indices if atom_index > total_atoms]
    if invalid_indices:
        print(f"Error: Atom indices {', '.join(map(str, invalid_indices))} exceed the number of atoms defined in the CONTCAR file. Use commas to separate atom indices not spaces.")
        return False

    return True

def clean_monomers_content(monomers_content):
    """
    Process the monomers content to create a cleaned version.
    Args:
        monomers_content (str): The original monomers content.
    Returns:
        str: The cleaned monomers content.
    This function cleans the monomers content by:
    1. Removing whitespace from each line.
    2. Removing everything after and including '#' to handle comments.
    3. Skipping lines without values.
    4. Checking that only integers and commas remain in the cleaned content.
    """
    # Initialize an empty string to store the cleaned monomers content
    monomers_content_clean = ""

    # Process each line in the input
    for line_number, line in enumerate(monomers_content.split('\n'), start=1):
        # Remove leading/trailing whitespace and everything after and including "#"
        line = line.split('#')[0].replace(' ', '')

        # Skip lines without values
        if not line:
            continue

        # Check that only integers and commas remain in the line
        for char in line:
            if not (char.isdigit() or char == ','):
                # If an invalid character is found, print an error message
                # indicating the line number and the invalid character
                print(f"Error in line {line_number} of the monomers file: Invalid character '{char}' detected.")
                # Exit the python scripy
                sys.exit(1)

        # If the line is valid, add the cleaned line to the monomers_content_clean string
        monomers_content_clean += line + '\n'

    # Return the cleaned monomers content if all lines are valid
    return monomers_content_clean

# Function to process monomers data
def process_monomers(contcar_content, monomers_content):
    """
    Process monomers data.
    Args:
        contcar_content (str): The contents of the CONTCAR file.
        monomers_content (str): The cleaned monomers content.
    Returns:
        list of list of int: List of monomers, each represented as a list of atom indices.
    This function processes monomers data, checks atom indices validity, and identifies missing atoms.
    """
    # Split monomers content into lines and parse atom indices
    monomer_lines = monomers_content.strip().split('\n')
    monomers = [sorted(map(int, line.split(','))) for line in monomer_lines]

    # Get total number of atoms from CONTCAR file
    total_atoms = sum(map(int, contcar_content.split('\n')[6].split()))
    all_atom_indices = list(range(1, total_atoms + 1))

    # Check validity of atom indices
    if not check_atom_indices([atom for monomer in monomers for atom in monomer], total_atoms):
        return None

    # Identify missing atoms in the monomers
    all_monomer_indices = [atom for monomer in monomers for atom in monomer]
    missing_atoms = list(set(all_atom_indices) - set(all_monomer_indices))
    monomers.append(missing_atoms)

    return monomers

# Function to get atomic symbols from atom indices
def get_atomic_symbols(contcar_content, atom_indices):
    """
    Get atomic symbols from atom indices.
    Args:
        contcar_content (str): The contents of the CONTCAR file.
        atom_indices (list of int): List of atom indices.
    Returns:
        list of str: List of atomic symbols corresponding to the given atom indices.
    This function maps atom indices to atomic symbols based on the CONTCAR file.
    """
    atom_symbols = contcar_content.split('\n')[5].split()
    atomic_symbols = []

    # Map atom indices to atomic symbols
    for atom_index in atom_indices:
        sum_integers = 0
        for i, num in enumerate(map(int, contcar_content.split('\n')[6].split())):
            if atom_index <= sum_integers + num:
                atomic_symbols.append(atom_symbols[i])
                break
            sum_integers += num

    return atomic_symbols

# Function to create CONTCAR file
def create_monomer_contcar_file(file_name, contcar_content, monomer):
    """
    Create a new CONTCAR file for a monomer.
    Args:
        file_name (str): The name of the output file.
        contcar_content (str): The contents of the CONTCAR file.
        monomer (list of int): List of atom indices representing the monomer.
    This function creates a new CONTCAR file for a given monomer, including atomic symbols and coordinates.
    """
    with open(file_name, "w") as file:
        atomic_symbols = get_atomic_symbols(contcar_content, monomer)
        unique_atomic_symbols = list(OrderedDict.fromkeys(atomic_symbols))

        # Write atomic symbols and other metadata to the new file
        file.write('   ' + '   '.join(unique_atomic_symbols) + '\n')
        file.write(contcar_content.split('\n')[1] + '\n')
        file.write('\n'.join(contcar_content.split('\n')[2:5]) + '\n')
        file.write('   ' + '    '.join(unique_atomic_symbols) + '\n')
        file.write('   ' + '   '.join(map(str, [atomic_symbols.count(symbol) for symbol in unique_atomic_symbols])) + '\n')
        file.write('\n'.join(contcar_content.split('\n')[8:9]) + '\n')

        # Write atom coordinates for the monomer
        for atom_index in monomer:
            atom_line = contcar_content.split('\n')[8 + atom_index]
            file.write(atom_line + '\n')

# Main function
def main():
    """
    Main function to process monomers and create CONTCAR files.
    This function parses command line arguments, reads CONTCAR and monomers content,
    processes the monomers, and creates CONTCAR files for the specified body order.
    """
    args = parse_args()

    body_order = args.body_order
    contcar_filename = args.contcar
    monomers_filename = args.monomers
    if body_order == 0:
        print(f"Used files: {contcar_filename} and {monomers_filename}, body order: full")
    else:
        print(f"Used files: {contcar_filename} and {monomers_filename}, body order: {body_order}")

    # Read CONTCAR and monomers content
    contcar_content = read_file(contcar_filename)
    monomers_content = read_file(monomers_filename)
    monomers_content = clean_monomers_content(monomers_content)

    # Process monomers and create files
    if contcar_content is not None and monomers_content is not None:
        monomers = process_monomers(contcar_content, monomers_content)
        if monomers is not None:
            if len(monomers) > 4:
                print(f"More than four monomers are not yet implemented.")
                return
            else:
                # 1. order body terms
                for i, monomer1 in enumerate(monomers, start=1):
                    create_monomer_contcar_file(f"POSCAR_{i}", contcar_content, monomer1)
                    if body_order == 1:
                            continue

                    # 2. order body terms
                    for j, monomer2 in enumerate(monomers[i:], start=i+1):
                        combined_monomer = sorted(monomer1 + monomer2)
                        create_monomer_contcar_file(f"POSCAR_{i}_{j}", contcar_content, combined_monomer)
                        if body_order == 2 or len(monomers) == 2:
                            continue

                        # 3. order body terms
                        for k, monomer3 in enumerate(monomers[j:], start=j+1):
                            combined_monomer = sorted(monomer1 + monomer2 + monomer3)
                            create_monomer_contcar_file(f"POSCAR_{i}_{j}_{k}", contcar_content, combined_monomer)

                            if body_order == 3 or len(monomers) == 3:
                                continue

                            # 4. order body terms
                            for l, monomer4 in enumerate(monomers[k:], start=k+1):
                                combined_monomer = sorted(monomer1 + monomer2 + monomer3 + monomer4)
                                create_monomer_contcar_file(f"POSCAR_{i}_{j}_{k}_{l}", contcar_content, combined_monomer)
                                
                                if body_order == 4 or len(monomers) == 4:
                                    continue

                                # 5. order body terms
                                for m, monomer5 in enumerate(monomers[l:], start=l+1):
                                    combined_monomer = sorted(monomer1 + monomer2 + monomer3 + monomer4 + monomer5)
                                    create_monomer_contcar_file(f"POSCAR_{i}_{j}_{k}_{l}_{m}", contcar_content, combined_monomer)

                                    if body_order == 5 or len(monomers) == 5:
                                        continue

                                    # 6. order body terms
                                    for n, monomer6 in enumerate(monomers[m:], start=m+1):
                                        combined_monomer = sorted(monomer1 + monomer2 + monomer3 + monomer4 + monomer5 + monomer6)
                                        create_monomer_contcar_file(f"POSCAR_{i}_{j}_{k}_{l}_{m}_{n}", contcar_content, combined_monomer)

                                        if body_order == 6 or len(monomers) == 6:
                                            continue

                                        # 7. order body terms
                                        for o, monomer7 in enumerate(monomers[n:], start=n+1):
                                            combined_monomer = sorted(monomer1 + monomer2 + monomer3 + monomer4 + monomer5 + monomer6 + monomer7)
                                            create_monomer_contcar_file(f"POSCAR_{i}_{j}_{k}_{l}_{m}_{n}_{o}", contcar_content, combined_monomer)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
