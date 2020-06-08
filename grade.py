#!/usr/bin/python3
import os
import sys
import argparse
import subprocess

sys.path.insert(0, "printing")
sys.path.insert(0, "hw1")
from printing import Printing as p
from hw1 import HW1
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="path to the homework to grade")
    parser.add_argument("part", type=int, help="part of the homework to grade")
    parser.add_argument("student", type=str, help="the name of student/group to grade")

    args = parser.parse_args()

    tester = Grader(args.hw, args.part, args.student)

    tester.run_test(1, args.student)

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, close_fds=True,
                     universal_newlines=True)
    p.wait()
    return p

def check_file(fneme):
    if os.path.isfile(fname):
        return 0 
    else:
        return 1

class Grader():

    def __init__(self, hw, part, student):

        self.hw = hw
        self.part = part 
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
        if check_file(fname):
            raise ValueError("{} does not exist".format(fname))


    def compile_code(self, fname):
        pass

    def inster_mod(self, mod, kedr=True):
        pass

    def remove_mod(self, mod, kedr=True):
        pass

    def checkout_branch(self, branch):
        pass

    def print_intro(self, name, part):
        p.prCyan("="*85)
        p.prIntro(name, part)
        p.prCyan("-"*85)

    def run_test(self, part, student):

        student_dir = os.path.join(self.hw_root, student)
        grade_dir = os.path.join(student_dir, 'hw1')
        os.chdir(grade_dir)

        self.print_intro(sudent, part)

        for item in self.rubric:
            for n,j in enumerate(self.rubric[item]):
                part_dir = os.path.join(grade_dir, j['dir'])
                os.chdir(part_dir)
                p.prCyan("grade {}.{}: {}".format(item, n+1, j['desc']))
                p.prCyan("-"*85)
                for i in j['cmd']:
                    #cmd = run_cmd(i)
                    #print(cmd.stdout.read())
                    os.system(i)
                print('\n')
                p.prCyan("-"*85)



if __name__ == '__main__':
    main()
