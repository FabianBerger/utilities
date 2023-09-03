#!/usr/bin/env python3
import os
import argparse
import shutil
import datetime

"""
get_POTCAR.py

This script generates a VASP POTCAR (Projector Augmented Wave Pseudopotential) file for use in VASP calculations. It allows users to specify PAW (PAW potentials) settings and the location of PAW potentials, and then it constructs the POTCAR file based on the chemical elements present in the input POSCAR or CONTCAR file.

Usage:
    python generate_POTCAR.py [--paw_setting PAW_SETTING] [--paw_location PAW_LOCATION]

Arguments:
    --paw_setting {1, 2, 3, 4, 5, 6}
        Select the PAW settings:
        1 : VASP recommendation for PAW potentials.
        2 : Hard PAW potentials or VASP recommendation if not available.
        3 : VASP recommendation for GW/RPA PAW potentials.
        4 : Hard GW/RPA PAW potentials or VASP recommendation if not available.
        5 : Materials Project Recommendation.
        6 : Minimum electron PAW potentials.
        (Default: 1)

    --paw_location PAW_LOCATION
        Path to the directory containing PAW potentials.
        (Default: '/home/fb593/michaelides-backup/fb593/apps/vasp/vasp_PP_LIBRARY/potpaw_PBE.54/')

Description:
    - The script reads the chemical elements from the 6th line of the input POSCAR or CONTCAR file.
    - It maps each element to the corresponding PAW potential based on the selected PAW setting.
    - The script appends the selected PAW potentials to the POTCAR file.

Functions:
    - parse_arguments():
        Parse command-line arguments.
    
    - is_valid_line(line):
        Check if a line contains only alphabetic characters and spaces.

    - read_6th_line(filename):
        Read the 6th line of a file.
    
    - create_element_dict():
        Create a dictionary that maps chemical elements to PAW potentials for different settings.

    - write_POTCAR(paw_pot, source_path):
        Append a specified POTCAR file to the existing POTCAR file.

Example:
    To generate a POTCAR file with VASP recommended PAW potentials, run:
    python generate_POTCAR.py --paw_setting 1 --paw_location /path/to/potpaw_directory

Notes:
    - Ensure that the input POSCAR or CONTCAR file exists in the current directory.

For more information on available PAW potentials, refer to the VASP documentation (https://www.vasp.at/wiki/index.php/Available_PAW_potentials/) or the Materials Project documentation (https://docs.materialsproject.org/methodology/materials-methodology/calculation-details/r2scan-calculations/pseudopotentials/).

Author:
    Dr Fabian Berger

"""

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process files and arguments.')
    parser.add_argument(
        "--paw_setting",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        default=1,
        help=(
            "Select the PAW settings:\n"
            "1 : VASP recommendation for PAW potentials.\n"
            "2 : Hard PAW potentials or VASP recommendation if not available.\n"
            "3 : VASP recommendation for GW/RPA PAW potentials.\n"
            "4 : Hard GW/RPA PAW potentials or VASP recommendation if not available.\n"
            "5 : Materials Project Recommendation.\n"
            "6 : Minimum electron PAW potentials."
        )
    )
    parser.add_argument('--paw_location', type=str, default='/home/fb593/michaelides-backup/fb593/apps/vasp/vasp_PP_LIBRARY/potpaw_PBE.54/', help='Path to paw_location')
    return parser.parse_args()


def is_valid_line(line):
    """
    Check if a line contains only alphabetic characters and spaces.

    Args:
        line (str): The line to check.

    Returns:
        bool: True if the line contains only alphabetic characters and spaces, False otherwise.
    """
    for char in line.strip():
        if not char.isalpha() and char != ' ':
            return False
    return True


def read_6th_line(filename):
    """
    Read the 6th line of a file.

    Args:
        filename (str): The name of the file to read.

    Returns:
        list: A list of strings obtained by splitting the 6th line, or an empty list if reading fails.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 6:
                line = lines[5].strip()
                if is_valid_line(line):
                    return line.split()
                else:
                    print(f"6th line of {filename} contains non-letter characters.")
            else:
                print(f"{filename} does not have 6 lines.")
    except FileNotFoundError:
        print(f"{filename} not found.")
    return []


def create_element_dict():
    """
    Create a dictionary that maps chemical elements to PAW potentials for different settings.

    Returns:
        dict: A dictionary mapping chemical elements to lists of PAW potentials.
    """
    element_dict = {
        #recommended DFT VASP (01.09.2023), DFT hard (if not avail, VASP rec), recommended GW/RPA VASP, GW/RPA hard (if not avail, VASP rec), redommended Materials Project, minimal
            # check if Gd, Lu in materials project is a typo (https://docs.materialsproject.org/methodology/materials-methodology/calculation-details/r2scan-calculations/pseudopotentials)
        "H": ["H", "H_h", "H_GW", "H_h_GW", "H", "H"],
        "He": ["He", "He", "He_GW", "He_GW", "He", "He"],
        "Li": ["Li_sv", "Li_sv", "Li_sv_GW", "Li_sv_GW", "Li_sv", "Li"],
        "Be": ["Be", "Be", "Be_sv_GW", "Be_sv_GW", "Be_sv", "Be"],
        "B": ["B", "B_h", "B_GW", "B_GW", "B", "B"],
        "C": ["C", "C_h", "C_GW", "C_h_GW", "C", "C"],
        "N": ["N", "N_h", "N_GW", "N_h_GW", "N", "N"],
        "O": ["O", "O_h", "O_GW", "O_h_GW", "O", "O"],
        "F": ["F", "F_h", "F_GW", "F_h_GW", "F", "F"],
        "Ne": ["Ne", "Ne", "Ne_GW", "Ne_GW", "Ne", "Ne"],
        "Na": ["Na_pv", "Na_pv", "Na_sv_GW", "Na_sv_GW", "Na_pv", "Na"],
        "Mg": ["Mg", "Mg", "Mg_sv_GW", "Mg_sv_GW", "Mg_pv", "Mg"],
        "Al": ["Al", "Al", "Al_GW", "Al_GW", "Al", "Al"],
        "Si": ["Si", "Si", "Si_GW", "Si_GW", "Si", "Si"],
        "P": ["P", "P_h", "P_GW", "P_GW", "P", "P"],
        "S": ["S", "S_h", "S_GW", "S_GW", "S", "S"],
        "Cl": ["Cl", "Cl_h", "Cl_GW", "Cl_GW", "Cl", "Cl"],
        "Ar": ["Ar", "Ar", "Ar_GW", "Ar_GW", "Ar", "Ar"],
        "K": ["K_sv", "K_sv", "K_sv_GW", "K_sv_GW", "K_sv", "K_pv"],
        "Ca": ["Ca_sv", "Ca_sv", "Ca_sv_GW", "Ca_sv_GW", "Ca_sv", "Ca_pv"],
        "Sc": ["Sc_sv", "Sc_sv", "Sr_sv_GW", "Sr_sv_GW", "Sc_sv", "Sc"],
        "Ti": ["Ti_sv", "Ti_sv", "Ti_sv_GW", "Ti_sv_GW", "Ti_pv", "Ti"],
        "V": ["V_sv", "V_sv", "V_sv_GW", "V_sv_GW", "", "V"],
        "Cr": ["Cr_pv", "Cr_pv", "Cr_sv_GW", "Cr_sv_GW", "Cr_pv", "Cr"],
        "Mn": ["Mn_pv", "Mn_pv", "Mn_sv_GW", "Mn_sv_GW", "Mn_pv", "Mn"],
        "Fe": ["Fe", "Fe", "Fe_sv_GW", "Fe_sv_GW", "Fe_pv", "Fe"],
        "Co": ["Co", "Co", "Co_sv_GW", "Co_sv_GW", "Co", "Co"],
        "Ni": ["Ni", "Ni", "Ni_sv_GW", "Ni_sv_GW", "Ni_pv", "Ni"],
        "Cu": ["Cu", "Cu", "Cu_sv_GW", "Cu_sv_GW", "Cu_pv", "Cu"],
        "Zn": ["Zn", "Zn", "Zn_sv_GW", "Zn_sv_GW", "Zn", "Zn"],
        "Ga": ["Ga_d", "Ga_h", "Ga_d_GW", "Ga_d_GW", "Ga_d", "Ga"],
        "Ge": ["Ge_d", "Ge_h", "Ge_d_GW", "Ge_d_GW", "Ge_d", "Ge"],
        "As": ["As", "As", "As_GW", "As_GW", "As", "As"],
        "Se": ["Se", "Se", "Se_GW", "Se_GW", "Se", "Se"],
        "Br": ["Br", "Br", "Br_GW", "Br_GW", "Br", "Br"],
        "Kr": ["Kr", "Kr", "Kr_GW", "Kr_GW", "Kr", "Kr"],
        "Rb": ["Rb_sv", "Rb_sv", "Rb_sv_GW", "Rb_sv_GW", "Rb_sv", "Rb_pv"],
        "Sr": ["Sr_sv", "Sr_sv", "Sr_sv_GW", "Sr_sv_GW", "Sr_sv", "Sr_sv"],
        "Y": ["Y_sv", "Y_sv", "Y_sv_GW", "Y_sv_GW", "Y_sv", "Y_sv"],
        "Zr": ["Zr_sv", "Zr_sv", "Zr_sv_GW", "Zr_sv_GW", "Zr_sv", "Zr_sv"],
        "Nb": ["Nb_sv", "Nb_sv", "Nb_sv_GW", "Nb_sv_GW", "Nb_pv", "Nb_pv"],
        "Mo": ["Mo_sv", "Mo_sv", "Mo_sv_GW", "Mo_sv_GW", "Mo_pv", "Mo"],
        "Tc": ["Tc_pv", "Tc_pv", "Tc_sv_GW", "Tc_sv_GW", "Tc_pv", "Tc"],
        "Ru": ["Ru_pv", "Ru_pv", "Ru_sv_GW", "Ru_sv_GW", "Ru_pv", "Ru"],
        "Rh": ["Rh_pv", "Rh_pv", "Rh_sv_GW", "Rh_sv_GW", "Rh_pv", "Rh"],
        "Pd": ["Pd", "Pd", "Pd_sv_GW", "Pd_sv_GW", "Pd", "Pd"],
        "Ag": ["Ag", "Ag", "Ag_sv_GW", "Ag_sv_GW", "Ag", "Ag"],
        "Cd": ["Cd", "Cd", "Cd_sv_GW", "Cd_sv_GW", "Cd", "Cd"],
        "In": ["In_d", "In_d", "In_d_GW", "In_d_GW", "In_d", "In"],
        "Sn": ["Sn_d", "Sn_d", "Sn_d_GW", "Sn_d_GW", "Sn_d", "Sn"],
        "Sb": ["Sb", "Sb", "Sb_d_GW", "Sb_d_GW", "Sb", "Sb"],
        "Te": ["Te", "Te", "Te_GW", "Te_GW", "Te", "Te"],
        "I": ["I", "I", "I_GW", "I_GW", "I", "I"],
        "Xe": ["Xe", "Xe", "Xe_GW", "Xe_GW", "Xe", "Xe"],
        "Cs": ["Cs_sv", "Cs_sv", "Cs_sv_GW", "Cs_sv_GW", "Cs_sv", "Cs_sv"],
        "Ba": ["Ba_sv", "Ba_sv", "Ba_sv_GW", "Ba_sv_GW", "Ba_sv", "Ba_sv"],
        "La": ["La", "La", "La_GW", "La_GW", "La", "La_s"],
        "Ce": ["Ce", "Ce_h", "Ce_GW", "Ce_GW", "Ce", "Ce_3"],
        "Pr": ["Pr_3", "Pr_3", "", "", "Pr_3", "Pr_3"],
        "Nd": ["Nd_3", "Nd_3", "", "", "Nd_3", "Nd_3"],
        "Pm": ["Pm_3", "Pm_3", "", "", "Pm_3", "Pm_3"],
        "Sm": ["Sm_3", "Sm_3", "", "", "Sm_3", "Sm_3"],
        "Eu": ["Eu_2", "Eu_2", "", "", "Eu", "Eu_2"],
        "Gd": ["Gd_3", "Gd_3", "", "", "Gd", "Gd_3"],
        "Tb": ["Tb_3", "Tb_3", "", "", "Tb_3", "Tb_3"],
        "Dy": ["Dy_3", "Dy_3", "", "", "Dy_3", "Dy_3"],
        "Ho": ["Ho_3", "Ho_3", "", "", "Ho_3", "Ho_3"],
        "Er": ["Er_3", "Er_3", "", "", "Er_3", "Er_2"],
        "Tm": ["Tm_3", "Tm_3", "", "", "Tm_3", "Tm_3"],
        "Yb": ["Yb_2", "Yb_2", "", "", "Yb_2", "Yb_2"],
        "Lu": ["Lu_3", "Lu_3", "", "", "Lu", "Lu_3"],
        "Hf": ["Hf_pv", "Hf_pv", "Hf_sv_GW", "Hf_sv_GW", "Hf_pv", "Hf"],
        "Ta": ["Ta_pv", "Ta_pv", "Ta_sv_GW", "Ta_sv_GW", "Ta_pv", "Ta"],
        "W": ["W_sv", "W_sv", "W_sv_GW", "W_sv_GW", "W_sv", "W"],
        "Re": ["Re", "Re", "Re_sv_GW", "Re_sv_GW", "Re_pv", "Re"],
        "Os": ["Os", "Os", "Os_sv_GW", "Os_sv_GW", "Os_pv", "Os"],
        "Ir": ["Ir", "Ir", "Ir_sv_GW", "Ir_sv_GW", "Ir", "Ir"],
        "Pt": ["Pt", "Pt", "Pt_sv_GW", "Pt_sv_GW", "Pt", "Pt"],
        "Au": ["Au", "Au", "Au_sv_GW", "Au_sv_GW", "Au", "Au"],
        "Hg": ["Hg", "Hg", "Hg_sv_GW", "Hg_sv_GW", "Hg", "Hg"],
        "Tl": ["Tl_d", "Tl_d", "Tl_d_GW", "Tl_d_GW", "Tl_d", "Tl"],
        "Pb": ["Pb_d", "Pb_d", "Pb_d_GW", "Pb_d_GW", "Pb_d", "Pb"],
        "Bi": ["Bi_d", "Bi_d", "Bi_d_GW", "Bi_d_GW", "Bi", "Bi"],
        "Po": ["Po_d", "Po_d", "Po_d_GW", "Po_d_GW", "", "Po"],
        "At": ["At", "At", "At_d_GW", "At_d_GW", "", "At"],
        "Rn": ["Rn", "Rn", "Rn_d_GW", "Rn_d_GW", "", "Rn"]
    }
    return element_dict


def write_POTCAR(paw_pot, source_path):
    """
    Append a specified POTCAR file to the existing POTCAR file.

    Args:
        paw_pot (str): The name of the PAW potential.
        source_path (str): The path to the source POTCAR file to be appended.

    Returns:
        None
    """
    # Check if the source file exists before copying
    if os.path.isfile(source_path):
        with open(source_path, "rb") as source_file:
            # Append the content of the source POTCAR file to the existing POTCAR file
            with open("POTCAR", "ab") as potcar_file_append:
                shutil.copyfileobj(source_file, potcar_file_append)
        print(f"Appended POTCAR {paw_pot} to the existing POTCAR file.")
    else:
        print(f"POTCAR {paw_pot} not found in the specified path.")


def main():
    args = parse_arguments()
    paw_location = args.paw_location
    # Print messages based on the arguments
    print(f"Paw Location: {paw_location}")
    if args.paw_setting == 1:
        print("1 : VASP recommendation for PAW potentials, (https://www.vasp.at/wiki/index.php/Available_PAW_potentials/, 01.09.2023)")
    elif args.paw_setting == 2:
        print("2 : Hard PAW potentials or VASP recommendation if not available, (https://www.vasp.at/wiki/index.php/Available_PAW_potentials/, 01.09.2023)")
    elif args.paw_setting == 3:
        print("3 : VASP recommendation for GW/RPA PAW potentials, (https://www.vasp.at/wiki/index.php/Available_PAW_potentials/, 01.09.2023)")
    elif args.paw_setting == 4:
        print("4 : Hard GW/RPA PAW potentials or VASP recommendation if not available, (https://www.vasp.at/wiki/index.php/Available_PAW_potentials/, 01.09.2023)")
    elif args.paw_setting == 5:
        print("5 : Materials Project Recommendation (https://docs.materialsproject.org/methodology/materials-methodology/calculation-details/r2scan-calculations/pseudopotentials, 01.09.2023)")
    elif args.paw_setting == 6:
        print("6 : Minimum electron PAW potentials, (https://www.vasp.at/wiki/index.php/Available_PAW_potentials/, 01.09.2023)")

    element_dict = create_element_dict()

    # Get a list of files in the current directory
    files_in_directory = os.listdir()

    # Check if POSCAR and CONTCAR files exist and add them to the filenames list
    if "POSCAR" in files_in_directory:
        filename = "POSCAR"
    elif "CONTCAR" in files_in_directory:
        filename = "CONTCAR"

    # Check and process the selected files
    elements = []
    elements = read_6th_line(filename)

    # Create a new POTCAR file for appending
    if os.path.isfile("POTCAR"):
        # Get the current timestamp to create a unique suffix
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        # Rename the existing "POTCAR" file to "POTCAR_old_timestamp"
        os.rename("POTCAR", f"POTCAR_old_{timestamp}")

    with open("POTCAR", "ab") as potcar_file:
        # Process each string from the 6th line
        for element in elements:
            # Check if the selected_string corresponds to a key in the element_dict
            if element in element_dict:
                # Construct the source path using paw_location and the corresponding value in the dict
                source_path = os.path.join(paw_location, element_dict[element][args.paw_setting - 1], "POTCAR")
                print(f"source_path {source_path}")
                write_POTCAR(element_dict[element][args.paw_setting - 1], source_path)
            else:
                print(f"Element {element} is not in the dictionary.")


if __name__ == "__main__":
    main()
