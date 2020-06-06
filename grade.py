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

    print(args.hw, args.part, args.student)

    tester = Grader(args.hw, args.part, args.student)

    tester.run_test(1, args.student)

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT, close_fds=True,
                     universal_newlines=True)
    p.wait()
    return p

class Grader():

    def __init__(self, hw, part, student):

        self.hw = hw
        self.part = part 
        self.student = student

        hw_class = HW1()
        self.rubric = hw_class.rubric
        self.root = hw_class.root

        self.saved_cwd = os.getcwd()
        os.chdir(hw_class.root)

        print(self.rubric)



    def setup(self, hw, student):
        pass

    def cleanup(self):
        pass

    def run_test(self, part, student):

        os.chdir(student+'/hw1')


        p.prCyan("="*85)
        p.prIntro("d++", "all")
        p.prCyan("-"*85)

        for item in self.rubric:
            for n,j in enumerate(self.rubric[item]):
                os.chdir(j['dir'])
                p.prCyan("grade {}.{}: {}".format(item, n+1, j['desc']))
                p.prCyan("-"*80)
                for i in j['cmd']:
                    cmd = run_cmd(i)
                    print(cmd.stdout.read())
                print('\n')
                p.prCyan("-"*85)



if __name__ == '__main__':
    main()
