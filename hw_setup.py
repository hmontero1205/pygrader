#!/usr/bin/python3
"""hw_setup.py: Prepares grading enviorment"""
import argparse
import sys
import os
import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from git import Repo
from common import printing

GITHUB_HW_ORG = "cs4118-hw"

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

def _clone_via_ssh(repo_name: str, init_submodules: bool):
    repo = f"{GITHUB_HW_ORG}/{repo_name}"
    printing.print_purple(f"[ Cloning {repo}... ]")
    repo_obj = Repo.clone_from(f"git@github.com:{repo}.git", repo_name)

    if init_submodules:
        # This hw requires submodules in the grader to be initialized.
        repo_obj.git.submodule("update", "--init", "--recursive")
        repo_obj.git.submodule("update", "--remote")

def main():
    """Prompts for homework deadline and prepares submissions for grading"""
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="the hw to setup (e.g. hw1)")
    parser.add_argument("-s", "--submissions", dest="submissions", type=str,
            help="path to tgz file containing all hw1 submissions")
    args = parser.parse_args()

    s_path = os.path.abspath(args.submissions) if args.submissions else None

    root = os.path.join(Path.home(), '.grade')
    create_dir(root)

    os.chdir(root)
    if args.hw in ('hw1', 'linux-list'):
        if not s_path:
            sys.exit("hw1 usage: ./hw_setup hw1 -s <submission tarball path>")
        if not args.submissions or (not os.path.isfile(s_path) or
                not tarfile.is_tarfile(s_path)):
            sys.exit(f"Please provide a valid tarball. "
                     f"Couldn't read file at {s_path}!")

        if os.path.isdir("hw1"):
            _prompt_overwrite(args.hw, "hw1")

        shutil.copy(s_path, "./hw1.tgz")  # TODO: should I use os.path.join?
        with tarfile.open("hw1.tgz", "r:gz") as tar:
            # This will create the hw1 directory assuming the tarball was made
            # out of a dir called hw1 xD
            tar.extractall()

        os.chdir("hw1")

        # TODO This logic is sketchy because Canvas is inconsistent with how
        # submissions are named. Maybe we should use the Canvas API?
        for fname in os.listdir():
            if os.path.isfile(fname) and tarfile.is_tarfile(fname):
                without_ext = fname.split(".tgz")[0]
                try:
                    uni = without_ext.split("-")[1]
                except IndexError as _:
                    uni = without_ext.split("_")[-1]
                uni = uni.strip("_")

                create_dir(uni)
                shutil.move(fname, os.path.join(uni, f"{uni}.tgz"))

    elif args.hw in ('hw3', 'hw4', 'hw5'):
        if os.path.isdir(args.hw):
            _prompt_overwrite(args.hw, args.hw)

        # Creates .grade/hw3 if it isn't there or if we want to overwrite.
        create_dir(args.hw)

        os.chdir(args.hw)

        _clone_via_ssh(args.hw, init_submodules=(args.hw in ('hw5',)))
    else:
        pass

    record_deadline()
    print(f"Ready to grade {args.hw}!")

if __name__ == '__main__':
    main()
