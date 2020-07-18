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

def run_cmd(cmd):
    """Runs cmd using subprocess and returns the resulting object"""
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, close_fds=True,
                            universal_newlines=True)
    proc.wait()
    return proc

def is_dir(path):
    """Checks if path is a directory"""
    if not os.path.isdir(path):
        raise ValueError("{} is not a directory".format(path))

def file_exist(fname):
    """Checks if fname is a file"""
    return os.path.isfile(fname)

def get_file_manually():
    """Prompts the user for a file to open"""
    ls_output = os.listdir()

    for i, file in enumerate(ls_output):
        p.print_yellow("({}) {}".format(i+1, file))

    while True:
        select = int(input("What file do you want to select? (enter a number)"))
        if select <= len(ls_output):
            return ls_output[select-1]


def grep_file(fname, pattern):
    """Greps fname for pattern and prints the result

    TODO: this isn't actually being used as a grep.. it just wraps
    subprocess.run. Actually wrap the grep command.
    """
    if not file_exist(fname):
        p.print_yellow('_'*85)
        p.print_yellow('The student file has a diffrent name')
        fname = get_file_manually()
        p.print_yellow('‾'*85)


    pattern = pattern.format(fname=fname)

    subprocess.run(pattern, shell=True)

def inspect_file(fname):
    """Opens fname in less"""
    if not file_exist(fname):
        p.prYellow('_'*85)
        p.prYellow('The student file has a diffrent name')
        fname = get_file_manually()
        p.prYellow('‾'*85)


    subprocess.run("less {}".format(fname), shell=True)

def compile_code():
    """Compiles the current directory (either with Make or manually)"""
    ls_output = os.listdir()
    if "Makefile" not in ls_output:
        #prob try to run manually
        print(get_file_manually())

    subprocess.run(MAKE, shell=True)

def insert_mod(mod, kedr=True):
    """Calls insmod with mod and optionally attaches KEDR"""
    if subprocess.call(DMESG_C.split()) != 0:
        pass
    if kedr and subprocess.call(KEDR_START.format(mod).split()) != 0:
        pass
    if subprocess.call(INSMOD.format(mod).split()) != 0:
        pass


def remove_mod(mod, dmesg=True, kedr=True):
    """Performs module removal

    Calls rmmod with mod, optionally detaches KEDR, and optionally dumps the
    kernel log buffer using dmesg
    """
    if subprocess.call(RMMOD.format(mod).split()) != 0:
        pass
    if kedr and subprocess.call(KEDR_STOP.format(mod).split()) != 0:
        pass
    if dmesg:
        os.system(DMESG)

def run_command(cmd):
    """Wrapper on os.system()"""
    os.system(cmd)
