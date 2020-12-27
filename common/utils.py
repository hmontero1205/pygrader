"""utils.py: Grading helper functions"""
import os
import subprocess
import shutil

from typing import Callable, Dict, Optional, List

import common.printing as p

KEDR_START = "sudo kedr start {}"
INSMOD = "sudo insmod {}"
RMMOD = "sudo rmmod {}"
KEDR_STOP = "sudo kedr stop {}"
DMESG = "sudo dmesg"
DMESG_C = "sudo dmesg -C"
MAKE = "make clean && make"

# This template will extract all text in [start, EOF)
SED_TO_END = "sed -n '/{0}/,$p' {1}"

def cmd_popen(cmd: str) -> 'Process':
    """Uses subprocess.Popen to run a command, returns the object."""
    prc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                     executable="/bin/bash",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, close_fds=True,
                     universal_newlines=True)
    return prc

def run_cmd(cmd: str, silent: bool = False, shell: bool = True) -> int:
    """Runs cmd and returns the status code."""
    return subprocess.run(cmd, shell=shell, capture_output=silent).returncode

def is_dir(path: str):
    """Checks if path is a directory"""
    if not os.path.isdir(path):
        raise ValueError("{} is not a directory".format(path))

def file_exists(fname: str) -> bool:
    """Checks if fname is a file"""
    return os.path.isfile(fname)

def dir_exists(dir_path: str) -> bool:
    """Checks if dir_path exists (and is a directory)."""
    return os.path.isdir(dir_path)

def prompt_file_name(file_list: Optional[List[str]] = None) -> str:
    """Prompts the user for a file to open"""
    ls_output = os.listdir() if not file_list else file_list

    for i, file in enumerate(ls_output):
        p.print_yellow("({}) {}".format(i+1, file))

    while True:
        try:
            select = int(input("Enter choice number: "))
        except ValueError as _:
            continue

        if 0 < select <= len(ls_output):
            return ls_output[select-1]

def get_file(fname: str) -> str:
    """Checks if fname is in pwd. If not, prompts grader with choices"""
    if file_exists(fname):
        return fname

    p.print_red('_'*85)
    p.print_red(f"Couldn't find {fname}! "
                f"Did the student name it something else?")
    submission_name = prompt_file_name()
    p.print_red('‾'*85)
    return submission_name

def concat_files(outfile: str, file_types: List[str]) -> str:
    """Concats all relevant files in the cwd into 1 file called `outfile`."""
    if file_exists(outfile):
        return outfile

    with open(outfile, "w+") as o:
        for fname in os.listdir():
            if fname != outfile and fname[-2:] in file_types:
                shutil.copyfileobj(open(fname, "r"), o)
    return outfile

def remove_file(fname: str):
    if file_exists(fname):
        os.remove(fname)
    else:
        p.print_red(f"[ OPPS - {fname} does not exist ]")

def extract_between(fname: str, start: str, end: Optional[str] = None,
                    capture: bool = False):
    """Prints the text in fname that's in between start and end"""
    if not end:
        sed_command = SED_TO_END.format(start, fname)
    else:
        sed_command = SED_BETWEEN.format(start, end, fname)
    return subprocess.run(sed_command, shell=True, capture_output=capture)

def extract_function(file_name: str, funct_name: str) -> str:
    if not file_exists(file_name):
        return ""
    stack = []
    started = False
    funct = ""
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            if not funct_name in line and not started:
                continue

            is_prototype = "{" not in line and ";" in line
            if funct_name in line and not is_prototype:
                started = True

            funct += line
            if '{' in line:
                stack.append('{')

            if '}' in line:
                stack.pop()
                if not stack:
                    break

    return funct

def grep_file(fname: str, pattern: str, padding: int = 0) -> int:
    """Greps fname for pattern and returns the status code

    NOTE: Grep output is dumped to the shell."""
    fname = get_file(fname)
    padding_opt = "" if not padding else f"-C {padding}"
    cmd = f"grep --color=always {padding_opt} -E '{pattern}' {fname} "

    return subprocess.run(cmd, shell=True).returncode

def inspect_file(fname: str, pattern: Optional[str] = None,
                 use_pager: bool = True):
    """Displays 'fname', w/ optional pattern highlighted, optionally in less"""
    name = get_file(fname)
    bat_str = f"bat --color=always {name}"
    grep_str = (f"GREP_COLORS='ms=01;91;107' grep --color=always "
                f"-E '^|{pattern}' {'| less -R' if use_pager else ''}")
    if pattern:
        cmd = f"{bat_str} | {grep_str}"
    else:
        cmd = f"bat {fname}"
    subprocess.run(cmd, shell=True)

def inspect_directory(files: List[str], pattern: Optional[str] = None,
                      banner_fn: Optional[Callable] = None):
    """Prompt the user for which file to inspect with optional pattern.

    Args:
        files: List of files in the current directory
            (as reported by os.listdir(os.getcwd())).
        pattern: Optional pattern to highlight in the files.
        banner_fn: Optional function to call before presenting choices
            (used to print some sort of banner).
    """
    while True:
        if banner_fn:
            banner_fn()
        for i, file in enumerate(files):
            p.print_yellow("({}) {}".format(i + 1, file))
        p.print_yellow(f"({len(files) + 1}) "
                       f"{p.CVIOLET2}exit{p.CEND}")
        try:
            choice = int(input(f"{p.CBLUE2}Choice: {p.CEND}"))
        except (ValueError, EOFError):
            continue

        if 0 < choice <= len(files):
            inspect_file(files[choice - 1], pattern)
        elif choice == len(files) + 1:
            break
        else:
            continue

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

def insert_mod(mod: str, kedr: bool = True):
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

def remove_mod_silent(mod: str, kedr: bool = True):
    subprocess.run(RMMOD.format(mod).split(), stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)
    if kedr:
        subprocess.run(KEDR_STOP.format(mod).split(), stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)


def remove_mod(mod: str, dmesg: bool = True, kedr: bool = True):
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

def run_and_prompt(f: Callable):
    """Runs f and then prompts for rerun/shell/continue."""
    while True:
        f()
        p.print_line()
        p.print_yellow("Run test again (a)")
        p.print_yellow("Open shell & run again (s)")
        p.print_yellow("Continue (enter)")

        while True:
            try:
                usr_input = input(f"{p.CBLUE2}Enter an action [a|s]: {p.CEND}")
                break
            except EOFError as _:
                print("^D")
                continue

        if usr_input == 'a':
            continue
        elif usr_input == 's':
            p.print_red("^D/exit to end shell session")
            os.system("bash")
            continue
        else:
            break

def run_and_prompt_multi(test_name_to_callable: Dict[str, Callable],
                         banner_fn: Optional[Callable] = None,
                         finish_msg: Optional[str] = None):
    """Wraps run_and_prompt by offering multiple tests to run.

    Args:
        test_name_to_callable: Maps a test name to a function that executes that
            test.
        banner_fn: Optional function to execute before presenting choices
            (used to print some sort of banner).
        finish_msg: Optional message to print as the exit choice.
    """
    number_to_callable = dict(enumerate(test_name_to_callable.values()))
    finish_msg = "Finish" if not finish_msg else finish_msg
    while True:
        if banner_fn:
            banner_fn()
        for i, test_name in enumerate(test_name_to_callable.keys()):
            p.print_yellow("({}) {}".format(i + 1, test_name))
        p.print_yellow(f"({len(number_to_callable) + 1}) "
                       f"{p.CVIOLET2}{finish_msg}{p.CEND}")
        try:
            choice = int(input(f"{p.CBLUE2}Choice: {p.CEND}"))
        except (ValueError, EOFError):
            continue

        if 0 < choice <= len(number_to_callable):
            def tester_wrapper():
                p.print_line()
                number_to_callable[choice - 1]()
            run_and_prompt(tester_wrapper)
        elif choice == len(number_to_callable) + 1:
            break
        else:
            continue
