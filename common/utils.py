"""utils.py: Grading helper functions"""
import os
import subprocess

import common.printing as p

KEDR_START = "sudo kedr start {}"
INSMOD = "sudo insmod {}"
RMMOD = "sudo rmmod {}"
KEDR_STOP = "sudo kedr stop {}"
DMESG = "sudo dmesg"
DMESG_C = "sudo dmesg -C"
MAKE = "make clean && make"

# This template will extract all text in [start, end)
SED_BETWEEN = "sed -n '/{0}/,/{1}/{{/{1}/!p}}' {2}"

# This template will extract all text in [start, EOF)
SED_TO_END = "sed -n '/{0}/,$p' {1}"

def cmd_popen(cmd):
    prc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, close_fds=True,
                     universal_newlines=True)
    return prc

def run_cmd(cmd, silent=False) -> int:
    """Runs cmd in a shell and returns the status code."""
    return subprocess.run(cmd, shell=True, capture_output=silent).returncode

def is_dir(path):
    """Checks if path is a directory"""
    if not os.path.isdir(path):
        raise ValueError("{} is not a directory".format(path))

def file_exists(fname):
    """Checks if fname is a file"""
    return os.path.isfile(fname)

def prompt_file_name():
    """Prompts the user for a file to open"""
    ls_output = os.listdir()

    for i, file in enumerate(ls_output):
        p.print_yellow("({}) {}".format(i+1, file))

    while True:
        try:
            select = int(input("Enter choice number: "))
        except ValueError as _:
            continue

        if 0 < select <= len(ls_output):
            return ls_output[select-1]

def get_file(fname):
    """Checks if fname is in pwd. If not, prompts grader with choices"""
    if file_exists(fname):
        return fname

    p.print_red('_'*85)
    p.print_red(f"Couldn't find {fname}! "
                f"Did the student name it something else?")
    submission_name = prompt_file_name()
    p.print_red('‾'*85)
    return submission_name

def extract_between(fname, start, end=None):
    """Prints the text in fname that's in between start and end"""
    if not end:
        sed_command = SED_TO_END.format(start, fname)
    else:
        sed_command = SED_BETWEEN.format(start, end, fname)
    os.system(sed_command)

def grep_file(fname, pattern):
    """Greps fname for pattern and prints the result

    TODO: this isn't actually being used as a grep.. it just wraps
    subprocess.run. Actually wrap the grep command.
    """
    fname = get_file(fname)

    pattern = pattern.format(fname=fname)

    subprocess.run(pattern, shell=True)

def inspect_file(fname, pattern=None):
    """Opens fname in less, optionally greps for a pattern first."""
    name = get_file(fname)
    bat_str = f"bat --color=always {name}"
    grep_str = (f"GREP_COLORS='ms=01;91;107' grep --color=always "
                f"-E '^|{pattern}' | less -R")
    if pattern:
        cmd = f"{bat_str} | {grep_str}"
    else:
        cmd = f"bat {fname}"
    subprocess.run(cmd, shell=True)

def compile_code():
    """Compiles the current directory (either with Make or manually)"""
    ls_output = os.listdir()
    if "Makefile" not in ls_output:
        # Let's let the grader figure it out
        os.system("bash")

    p.print_cyan("[ Compiling... ]")
    ret = subprocess.call(MAKE, shell=True)

    if ret != 0:
        p.print_red("[ OOPS ]")
    else:
        p.print_green("[ OK ]")

def insert_mod(mod, kedr=True):
    """Calls insmod with mod and optionally attaches KEDR"""
    if subprocess.call(DMESG_C.split()) != 0:
        pass

    if kedr:
        p.print_cyan(f"[ Starting KEDR for {mod} ]")
        if subprocess.call(KEDR_START.format(mod).split()) != 0:
            p.print_red("[ OOPS ]")
        else:
            p.print_green("[ OK ]")

    p.print_cyan(f"[ Inserting module {mod} ]")
    if subprocess.call(INSMOD.format(mod).split()) != 0:
        p.print_red("[ OOPS ]")
    else:
        p.print_green("[ OK ]")

def remove_mod_silent(mod, kedr=True):
    subprocess.run(RMMOD.format(mod).split(), stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)
    if kedr:
        subprocess.run(KEDR_STOP.format(mod).split(), stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)


def remove_mod(mod, dmesg=True, kedr=True):
    """Performs module removal

    Calls rmmod with mod, optionally detaches KEDR, and optionally dumps the
    kernel log buffer using dmesg
    """
    p.print_cyan(f"[ Removing module {mod} ]")
    if subprocess.call(RMMOD.format(mod).split()) != 0:
        p.print_red("[ OOPS ]")
    else:
        p.print_green("[ OK ]")

    if kedr:
        p.print_cyan(f"[ Stopping KEDR for {mod} ]")
        if subprocess.call(KEDR_STOP.format(mod).split()) != 0:
            p.print_red("[ OOPS ]")
        else:
            p.print_green("[ OK ]")
    if dmesg:
        p.print_cyan("[ Dumping kernel log buffer... ]")
        os.system(DMESG)

def compare_values(observed: int, expected: int, desc: str,
                   silent: bool = False) -> bool:
    """Compares two values and (optionally) prints comparison results.

    Args:
        observed: Value observed
        expected: Expected value
        desc: The name of what we're comparing
        silent: Whether or not to print results.

    Returns:
        bool representing whether or not the values were the same.
    """
    if observed == expected:
        if not silent:
            p.print_green(f"[ OK: Got {observed}/{expected} {desc} ]")

        return True

    if not silent:
        p.print_red(f"[ FAIL: Got {observed}/{expected} {desc} ]")

    return False
