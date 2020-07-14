#!/usr/bin/python3
import os
import sys
import subprocess

sys.path.append(os.path.abspath('../printing'))
import printing as p

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

def get_file_manually():
    ls = os.listdir()

    for i,f in enumerate(ls):
        p.prYellow("({}) {}".format(i+1, f))

    while True:
        select = int(input("What file do you want to select? (enter a number)"))
        if select <= len(ls):
            return ls[select-1]


def grep_file(fname, grep):
    if not file_exist(fname):
        p.prYellow('_'*85)
        p.prYellow('The student file has a diffrent name')
        fname = get_file_manually()
        p.prYellow('‾'*85)


    grep = grep.format(fname=fname)

    print(grep)
    subprocess.run(grep, shell=True)
def inspect_file(fname):
    if not file_exist(fname):
        p.prYellow('_'*85)
        p.prYellow('The student file has a diffrent name')
        fname = get_file_manually()
        p.prYellow('‾'*85)


    subprocess.run("less {}".format(fname), shell=True)

def compile_code():
    ls = os.listdir()
    if "Makefile" not in ls:
        #prob try to run manually
        print(get_file_manually())

    subprocess.run(MAKE, shell=True)

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

def run_commend(cmd):
    os.system(cmd)
