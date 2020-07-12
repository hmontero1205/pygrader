#!/usr/bin/python3
import os
import sys
import subprocess

KEDR_START  = "sudo kedr start {}"
INSMOD      = "sudo insmod {}"
RMMOD       = "sudo rmmod {}"
KEDR_STOP   = "sudo kedr stop {}"
DMESG       = "sudo dmesg"
DMESG_C     = "sudo dmesg -C"
MAKE        = "make clean && make"

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, close_fds=True,
                     universal_newlines=True)
    p.wait()
    return p

def is_dir(path):
    if not os.path.isdir(path):
        raise ValueError("{} is not a directory".format(path))

def file_exist(fname):
    if os.path.isfile(fname):
        return 1 
    else:
        return 0

def grep_file(fname, grep):
    if not file_exist(fname):
        raise ValueError("{} does not exist".format(fname))
    subprocess.run(grep, shell=True)

def compile_code(cd):
    pass

def insert_mod(mod, kedr=True):
    if subprocess.call(DMESG_C.split()) != 0:
        pass
    if subprocess.call(KEDR_START.format(mod).split()) != 0:
        pass
    if subprocess.call(INSMOD.format(mod).split()) != 0:
        pass


def remove_mod(mod, dmesg=True, kedr=True):
    if subprocess.call(RMMOD.format(mod).split()) != 0:
        pass
    if subprocess.call(KEDR_STOP.format(mod).split()) != 0:
        pass
    
    if dmesg:
        os.system(DMESG)

def run_file(fname, cd):
    save_dir = os.path.abspath(os.getcwd())
    os.chdir(cd)
    print(os.getcwd())
    #subprocess.call(fname, shell=True)
    os.system(fname)
    os.chdir(save_dir)

def run_commend(self, cmd):
    os.system(cmd)
