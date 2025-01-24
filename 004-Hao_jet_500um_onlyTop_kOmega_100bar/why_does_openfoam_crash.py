import subprocess
import os
import csv
import argparse
import time
from pathlib import Path

def modify_foam_file(filepath, new_values, output_filepath=None):
    """
    Modify a foam file with new values from a dictionary.
    
    Args:
        filepath (str): Path to the original file
        new_values (dict): Dictionary containing the new values
        output_filepath (str, optional): Path for the modified file. If None, overwrites original file
    """
    if output_filepath is None:
        output_filepath = filepath
    
    # Read the entire file
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Process the lines
    modified_lines = []
    start_parsing = False
    
    for line in lines:
        # Keep original line by default
        modified_line = line
        
        # Strip whitespace for checking
        stripped_line = line.strip()
        
        # Start parsing after application line
        if stripped_line.startswith('application'):
            start_parsing = True
            
        if start_parsing:
            # Skip special lines
            if (not stripped_line.startswith(('/', '{', '}', '\\')) and 
                ' ' in stripped_line and 
                not stripped_line.startswith('// *')):
                
                # Get the key (first word)
                key = stripped_line.split()[0]
                
                # If this key exists in our new_values, replace the line
                if key in new_values:
                    modified_line = f"{key:<15} {new_values[key]};\n"
        
        modified_lines.append(modified_line)
    
    # Write the modified content to the output file
    with open(output_filepath, 'w') as file:
        file.writelines(modified_lines)

def get_latest_time(case_dir):
    """Get the latest time directory from OpenFOAM case."""
    time_dirs = []
    for item in os.listdir(case_dir):
        try:
            # Check if the directory name can be converted to float
            time = float(item)
            time_dirs.append(time)
        except ValueError:
            continue
    return str(max(time_dirs)) if time_dirs else '0'

def run_simulation(case_dir):
    """Run OpenFOAM simulation with direct output to terminal."""
    try:
        process = subprocess.run(['rhoCentralFoam'], cwd=case_dir)
        return process.returncode == 0
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
        return False

def main():
    # Set the case directory (current directory by default)
    case_dir = Path.cwd()
    control_dict_path = case_dir / 'system' / 'controlDict' # Overloaded / for Path objects
    
    # First run with original settings
    print("Starting first run with original settings...")
    success = run_simulation(case_dir)
    
    if success:
        print("First run completed successfully")
        return
    
    print("First run crashed, starting second run with finer time settings...")
    
    # Get the latest time directory
    latest_time = get_latest_time(case_dir)
    
    # Modify controlDict for second run
    new_settings = {
        'startFrom': 'latestTime',
        'writeControl': 'adjustableRunTime',
        'writeInterval': '1e-9',
        'deltaT': '1e-11',  # Set a smaller initial timestep
        'maxCo': '0.1',     # Set a conservative Courant number
    }
    
    # Backup original controlDict
    backup_path = control_dict_path.with_suffix('.backup')
    if not backup_path.exists():
        with open(control_dict_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
    
    # Modify controlDict
    modify_foam_file(control_dict_path, new_settings)
    
    # Run second simulation
    print(f"Starting from time {latest_time} with finer time settings...")
    success = run_simulation(case_dir)
    
    if success:
        print("Second run completed successfully")
    else:
        print("Second run also crashed")
        print("Check the log files for more information")

        latest_time = get_latest_time(case_dir)
    
    # Modify controlDict for third run
    new_settings = {
        'startFrom': 'latestTime',
        'writeControl': 'adjustableRunTime',
        'writeInterval': '1e-11',
        'deltaT': '1e-11',  # Set a smaller initial timestep
        'maxCo': '0.1',     # Set a conservative Courant number
    }
    
    # Backup original controlDict
    backup_path = control_dict_path.with_suffix('.backup')
    if not backup_path.exists():
        with open(control_dict_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
    
    # Modify controlDict
    modify_foam_file(control_dict_path, new_settings)
    
    # Run second simulation
    print(f"Starting from time {latest_time} with finer time settings...")
    success = run_simulation(case_dir)
    
    if success:
        print("Third run completed successfully")
    else:
        print("Third run also crashed")
        print("Check the log files for more information")

    new_settings = {
        'startFrom': 'latestTime',
        'writeControl': 'adjustableRunTime',
        'writeInterval': '1e-6',
        'deltaT': '1e-11',  # Set a smaller initial timestep
        'maxCo': '0.1',     # Set a conservative Courant number
    }

    modify_foam_file(control_dict_path, new_settings)    

if __name__ == '__main__':
    main()