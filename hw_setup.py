#!/usr/bin/env python3.7
"""hw_setup.py: Prepares grading enviorment"""
import argparse
import sys
import os
import shutil
import getpass
from pathlib import Path
from datetime import datetime
from common import printing

DEADLINE = None

def create_dir(name):
    """Wrapper around mkdir"""
    if not os.path.isdir(name):
        access = 0o700
        try:
            os.mkdir(name, access)
        except OSError:
            sys.exit(f"Creation of the directory {name} failed")
        else:
            print(f"Successfully created the directory {name}")

def record_deadline():
    """Reads in a deadline and stores it"""
    global DEADLINE  # pylint: disable=W0603
    if os.path.exists("deadline.txt"):
        return
    if not DEADLINE:
        printing.print_magenta("[ Recording assignment deadline... ]")
        while True:
            try:
                raw_deadline = input("Soft deadline (MM/DD/YY HH:MM AM/PM): ")
                # Let's make sure it actually parses
                _ = datetime.strptime(raw_deadline, "%m/%d/%y %I:%M %p")
                DEADLINE = raw_deadline
                break
            except ValueError as _:
                print("Incorrect format!")

    # Write the deadline to ~.grade/hwN/deadline.txt
    with open("deadline.txt", "w") as d:
        d.write(DEADLINE)

def _prompt_overwrite(hw_name: str, hw_path: str) -> bool:
    while True:
        try:
            res = input(f"{hw_name} is already set up. Overwrite? [y/n]: ")
        except EOFError:
            print("^D")
        if res == "n":
            return False
        elif res == "y":
            break

    shutil.rmtree(hw_path)
    return True

def main():
    """Prompts for homework deadline and prepares submissions for grading"""
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str,
                        help="the assignment to setup (e.g. hw1)")
    parser.add_argument("...", type=str, nargs=argparse.REMAINDER,
                        help="any arguments for assignment setup script")
    parsed = parser.parse_args()

    run_dir = os.getcwd()
    tas = []

    ta_file = os.path.join(Path.home(), 'tas.txt')
    if os.path.exists(ta_file):
        with open(os.path.join(Path.home(), 'tas.txt'), "r") as f:
            tas = f.read().splitlines()

    tas.append(getpass.getuser())

    for ta in tas:
        print(f"==={ta.rstrip()}===")
        os.chdir(run_dir)
        root = os.path.join(Path.home(), '.grade',
                            ta if ta != getpass.getuser() else '')
        create_dir(root)

        pygrader_dir = Path(__file__).resolve().parent
        hw_dir = os.path.join(pygrader_dir, parsed.hw)
        if not os.path.isdir(hw_dir):
            sys.exit(f"Unsupported assignment: {parsed.hw}")

        os.chdir(root)

        if (os.path.isdir(parsed.hw)
            and not _prompt_overwrite(parsed.hw, parsed.hw)):
            continue
        create_dir(parsed.hw)
        os.chdir(parsed.hw)

        setup_script = os.path.join(hw_dir, 'setup')
        if os.path.isfile(setup_script):
            if os.system(f"{setup_script} {' '.join(getattr(parsed, '...'))}"):
                sys.exit("Setup failed.")

        record_deadline()
    print(f"Ready to grade {parsed.hw}!")

if __name__ == '__main__':
    main()
