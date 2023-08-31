#!/usr/bin/env python3
import sys
import os
from collections import OrderedDict

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

def check_atom_indices(atom_indices, total_atoms):
    if len(atom_indices) != len(set(atom_indices)):
        print("Error: Atom index is repeated in the monomers file.")
        return False
    if any(atom_index > total_atoms for atom_index in atom_indices):
        print("Error: Atom index exceeds the number of atoms defined in the CONTCAR file.")
        return False
    return True

def process_monomers(contcar_content, monomers_content):
    monomer_lines = monomers_content.strip().split('\n')
    #monomers = [list(map(int, line.split(','))) for line in monomer_lines]
    monomers = [sorted(map(int, line.split(','))) for line in monomer_lines]

    total_atoms = sum(map(int, contcar_content.split('\n')[6].split()))
    all_atom_indices = list(range(1, total_atoms + 1))

    if not check_atom_indices([atom for monomer in monomers for atom in monomer], total_atoms):
        return None

    all_monomer_indices = [atom for monomer in monomers for atom in monomer]
    missing_atoms = list(set(all_atom_indices) - set(all_monomer_indices))
    monomers.append(missing_atoms)

    return monomers

def get_atomic_symbols(contcar_content, atom_indices):
    atom_symbols = contcar_content.split('\n')[5].split()
    atomic_symbols = []

    for atom_index in atom_indices:
        sum_integers = 0
        for i, num in enumerate(map(int, contcar_content.split('\n')[6].split())):
            if atom_index <= sum_integers + num:
                atomic_symbols.append(atom_symbols[i])
                break
            sum_integers += num

    return atomic_symbols

def create_monomer_contcar_file(file_name, contcar_content, monomer):
    with open(file_name, "w") as file:
        atomic_symbols = get_atomic_symbols(contcar_content, monomer)
        unique_atomic_symbols = list(OrderedDict.fromkeys(atomic_symbols))

        file.write('   ' + '   '.join(unique_atomic_symbols) + '\n')
        file.write(contcar_content.split('\n')[1] + '\n')
        file.write('\n'.join(contcar_content.split('\n')[2:5]) + '\n')
        file.write('   ' + '    '.join(unique_atomic_symbols) + '\n')
        file.write('   ' + '   '.join(map(str, [atomic_symbols.count(symbol) for symbol in unique_atomic_symbols])) + '\n')
        file.write('\n'.join(contcar_content.split('\n')[8:9]) + '\n')

        for atom_index in monomer:
            atom_line = contcar_content.split('\n')[8 + atom_index]
            file.write(atom_line + '\n')

def create_pair_combination_contcar_file(file_name, contcar_content, monomer1, monomer2):
    with open(file_name, "w") as file:
        atomic_symbols = get_atomic_symbols(contcar_content, monomer1 + monomer2)
        unique_atomic_symbols = list(OrderedDict.fromkeys(atomic_symbols))

        file.write('   ' + '   '.join(unique_atomic_symbols) + '\n')
        file.write(contcar_content.split('\n')[1] + '\n')
        file.write('\n'.join(contcar_content.split('\n')[2:5]) + '\n')
        file.write('   ' + '    '.join(unique_atomic_symbols) + '\n')
        file.write('   ' + '   '.join(map(str, [atomic_symbols.count(symbol) for symbol in unique_atomic_symbols])) + '\n')
        file.write('\n'.join(contcar_content.split('\n')[8:9]) + '\n')

        for atom_index in monomer1 + monomer2:
            atom_line = contcar_content.split('\n')[8 + atom_index]
            file.write(atom_line + '\n')

def main():
    if len(sys.argv) == 1:
        contcar_filename = "CONTCAR"
        monomers_filename = "monomers"
    elif len(sys.argv) == 3:
        contcar_filename = sys.argv[1]
        monomers_filename = sys.argv[2]
    else:
        script_name = os.path.basename(sys.argv[0])
        print(f"Usage: {script_name} [CONTCAR_filename monomers_filename]")
        return

    contcar_content = read_file(contcar_filename)
    monomers_content = read_file(monomers_filename)

    if contcar_content is not None and monomers_content is not None:
        monomers = process_monomers(contcar_content, monomers_content)

        if monomers is not None:
            for i, monomer1 in enumerate(monomers, start=1):
                create_monomer_contcar_file(f"POSCAR_{i}", contcar_content, monomer1)
                for j, monomer2 in enumerate(monomers[i:], start=i+1):
                    combined_monomer = sorted(monomer1 + monomer2)
                    create_monomer_contcar_file(f"POSCAR_{i}_{j}", contcar_content, combined_monomer)

if __name__ == "__main__":
    main()
