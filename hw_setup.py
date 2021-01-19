#!/usr/bin/env python3.7
"""hw_setup.py: Prepares grading enviorment"""
import argparse
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
from common import printing

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
    printing.print_magenta("[ Recording assignment deadline... ]")
    while True:
        try:
            raw_deadline = input("Soft deadline (MM/DD/YY HH:MM AM/PM): ")
            # Let's make sure it actually parses
            _ = datetime.strptime(raw_deadline, "%m/%d/%y %I:%M %p")
            break
        except ValueError as _:
            print("Incorrect format!")

    # Write the deadline to ~.grade/hwN/deadline.txt
    with open("deadline.txt", "w") as d:
        d.write(raw_deadline)

def _prompt_overwrite(hw_name: str, hw_path: str):
    while True:
        try:
            res = input(f"{hw_name} is already set up. Overwrite? [y/n]: ")
        except EOFError:
            print("^D")
        if res == "n":
            print(f"Ready to grade {hw_name}!")
            sys.exit()
        elif res == "y":
            break

    shutil.rmtree(hw_path)

def main():
    """Prompts for homework deadline and prepares submissions for grading"""
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="the hw to setup (e.g. hw1)")
    parser.add_argument("-s", "--submissions", dest="submissions", type=str,
            help="path to zipfile containing all hw1 submissions")
    args = parser.parse_args()

    root = os.path.join(Path.home(), '.grade')
    create_dir(root)

    pygrader_dir = Path(__file__).resolve().parent

    os.chdir(root)

    if os.path.isdir(args.hw):
        _prompt_overwrite(args.hw, args.hw)
    create_dir(args.hw)
    os.chdir(args.hw)

    setup_script = os.path.join(pygrader_dir, args.hw, 'setup')
    if os.path.isfile(setup_script) and os.access(setup_script, os.X_OK):
        os.system(setup_script)

    record_deadline()
    print(f"Ready to grade {args.hw}!")

if __name__ == '__main__':
    main()
