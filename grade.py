#!/usr/bin/python3
import os
import sys
import argparse
import subprocess

sys.path.insert(0, "printing")
sys.path.insert(0, "hw1")
from printing import Printing as p
from hw1 import HW1


KEDR_START  = "sudo kedr start {}"
INSMOD      = "sudo insmod {}"
RMMOD       = "sudo rmmod {}"
KEDR_STOP   = "sudo kedr stop {}"
DMESG       = "sudo dmesg"
DMESG_C     = "sudo dmesg -C"

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="path to the homework to grade")
    parser.add_argument("table", type=str, help="table to grade")
    parser.add_argument("student", type=str, help="the name of student/group to grade")

    args = parser.parse_args()

    tester = Grader(args.hw, args.table, args.student)

    tester.run_test(args.table, args.student)

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, close_fds=True,
                     universal_newlines=True)
    p.wait()
    return p

def check_file(fname):
    if os.path.isfile(fname):
        return 0 
    else:
        return 1

class Grader():

    def __init__(self, hw, table, student):

        self.hw = hw
        self.table = table
        self.student = student

        hw_class = HW1()
        self.rubric = hw_class.rubric
        self.hw_root = os.path.abspath(hw_class.root)

        self.saved_cwd = os.getcwd()
        os.chdir(hw_class.root)


    def setup(self, hw, student):
        pass

    def cleanup(self):
        pass

    def inspect_file(self, fname, grep):
        #if check_file(fname):
         #   raise ValueError("{} does not exist".format(fname))
        
        sed = grep.format(fname)
        os.system(sed)


    def compile_code(self, cd):
        save_dir = os.path.abspath(os.getcwd())
        wd = os.path.join(save_dir, cd)
        os.chdir(wd)
        print(os.getcwd())
        os.system("make")
        os.chdir(save_dir)

    def insert_mod(self, cd, mod, kedr=True):
        save_dir = os.path.abspath(os.getcwd())
        wd = os.path.join(save_dir, cd)
        os.chdir(wd)
        if subprocess.call(DMESG_C.split()) != 0:
            pass
        if subprocess.call(KEDR_START.format(mod).split()) != 0:
            pass
        if subprocess.call(INSMOD.format(mod).split()) != 0:
            pass

        os.chdir(save_dir)


    def remove_mod(self, cd,  mod, kedr=True):
        save_dir = os.path.abspath(os.getcwd())
        wd = os.path.join(save_dir, cd)
        os.chdir(wd)
        if subprocess.call(RMMOD.format(mod).split()) != 0:
            pass
        if subprocess.call(KEDR_STOP.format(mod).split()) != 0:
            pass

        os.system(DMESG)
        os.chdir(save_dir)

    def checkout_branch(self, branch):
        pass

    def print_intro(self, name, part):
        p.prCyan("="*85)
        p.prIntro(name, part)
        p.prCyan("-"*85)

    def run_code(self, cd, fname):
        save_dir = os.path.abspath(os.getcwd())
        wd = os.path.join(save_dir, cd)
        os.chdir(wd)
        print(os.getcwd())
        subprocess.call(fname, shell=True)
        os.chdir(save_dir)


    def run_test(self, table, student):

        student_dir = os.path.join(self.hw_root, student)
        grade_dir = os.path.join(student_dir, 'hw1')
        os.chdir(grade_dir)

        self.print_intro(student, table)

        for item in self.rubric[table]:

            for grade in item:
                p.prCyan("-"*85)
                print(' ', grade['desc'])
                p.prCyan("-"*85)
                while True:
                    if grade['type'] == 'inspect':
                        self.inspect_file(grade['file'], grade['param'])
                    elif grade['type'] == 'compile':
                        cd = grade['dir']
                        self.compile_code(cd)

                    elif grade['type'] == 'insert':
                        cd = grade['dir']
                        fname = grade['file']
                        self.insert_mod(cd, fname)

                    elif grade['type'] == 'remove':
                        cd = grade['dir']
                        fname = grade['file']
                        self.remove_mod(cd, fname)
                    elif grade['type'] == 'run':
                        cd = grade['dir']
                        fname = grade['file']
                        self.run_code(cd, fname)

                    p.prRed("Run test again? (Y/n)")
                    text = input()

                    if text != 'Y':
                        break


if __name__ == '__main__':
    main()
