#!/usr/bin/python3
"""
setting up the hw dir by first creating a .grade/ in $HOME and subdir for each
hw
"""
import argparse
import sys
import os
import pickle
import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from pytz import timezone

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
    """Reads in a deadline, localizes it to NYC time, and serializes it"""
    # Takes into account DST
    nyc_tz = timezone("America/New_York")

    raw_deadline = datetime.strptime(input("Soft deadline (MM/DD/YY HH:MM AM/PM): "),
            "%m/%d/%y %I:%M %p")

    # Add 59 seconds for precision, add NY time for tzinfo
    deadline = nyc_tz.localize(raw_deadline.replace(second=59, tzinfo=None))

    # Write the deadline datetime obj to ~.grade/hwN/.deadline
    with open(".deadline", "wb") as d:
        pickle.dump(deadline, d)

def main():
    """Prompts for homework deadline and prepares submissions for grading"""
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="the hw to setup (e.g. hw1)")
    parser.add_argument("--submissions", dest="submissions", type=str,
            help="path to tgz file containing all hw1 submissions")
    args = parser.parse_args()

    root = os.path.join(Path.home(), '.grade')
    create_dir(root)

    os.chdir(root)
    if args.hw == 'hw1':
        if not args.submissions or (not os.path.isfile(args.submissions) or
                not tarfile.is_tarfile(args.submissions)):
            raise ValueError("please provide a valid tar file")

        if os.path.isdir("hw1"):
            res = input("HW1 is already set up. Overwrite? [Y/n]: ")
            if res != "Y":
                print(f"Ready to grade {args.hw}!")
                sys.exit()

            shutil.rmtree("hw1")

        shutil.copy(args.submissions, "./hw1.tgz")  # TODO: should I use os.path.join?
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

    elif args.hw == 'hw3':
        pass
    else:
        pass

    record_deadline()
    print(f"Ready to grade {args.hw}!")

if __name__ == '__main__':
    main()
