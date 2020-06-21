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
MAKE        = "make clean && make"

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
        self.hw_root = hw_class.root
        print("hw_root: ", self.hw_root)
        self.grade_dir = hw_class.grade_dir
        print("grade_dir: ", self.grade_dir)

        os.chdir(hw_class.grade_dir)


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

    def insert_mod(self, mod, kedr=True):
        if subprocess.call(DMESG_C.split()) != 0:
            pass
        if subprocess.call(KEDR_START.format(mod).split()) != 0:
            pass
        if subprocess.call(INSMOD.format(mod).split()) != 0:
            pass


    def remove_mod(self,  mod, dmesg=True, kedr=True):
        if subprocess.call(RMMOD.format(mod).split()) != 0:
            pass
        if subprocess.call(KEDR_STOP.format(mod).split()) != 0:
            pass
        
        if dmesg:
            os.system(DMESG)

    def checkout_branch(self, branch):
        pass

    def print_intro(self, name, part):
        p.prCyan("="*85)
        p.prIntro(name, part)
        p.prCyan("-"*85)

    def run_file(self, fname, cd):
        save_dir = os.path.abspath(os.getcwd())
        os.chdir(cd)
        print(os.getcwd())
        #subprocess.call(fname, shell=True)
        os.system(fname)
        os.chdir(save_dir)
    
    def run_commend(self, cmd):
        os.system(cmd)

    def grade_section(self, section, key):
        desc = section['desc']
        points = section['points']
        cmds = section['cmd']
        os.chdir(section['dir'])
        
        p.prPurple("Grading Item {}: ".format(key))
        p.prCyan(desc)
        p.prCyan('-'*85)

        for cmd in cmds:
            func = cmd['type']
            args = cmd['args']

            if func == 'inspect':
                self.inspect_file(args[0], args[1])
            elif func == 'insert':
                os.system(MAKE)
                self.insert_mod(args[0])
            elif func == 'remove':
                dmesg = False if len(args) > 1 else True
                self.remove_mod(args[0], dmesg)
            elif func == 'run_commend':
                self.run_commend(args[0])
            elif func == 'execute':
                self.run_file(args[0], args[1])



    def run_test(self, table_key, student):


        self.print_intro(student, table_key)
        
        table_keys = [*self.rubric.keys()]
        
        if table_key not in table_keys:
            return 0

        table = self.rubric[table_key]

        for section in table:
            #print(key)

            #print(table[key])
            
            while True:

                self.grade_section(table[section], section)

                p.prRed("Run test again? (Y/n)")

                inval = input()

                if inval != 'Y':
                    break

            p.prCyan('-'*85) 
            '''
            desc = table[key]['desc']
            p.prPurple("Grading Item {}: ".format(key))
            p.prCyan(desc)
            p.prCyan('-'*85)
            
            if not fname:
                fname = table[key]['file']
            if table[key]['type'] == 'inspect':
                args = table[key]['arg']
                self.inspect_file(fname, args)
            elif table[key]['type'] == 'insert_remove':
                self.insert_mod(fname+'.ko')
                self.remove_mod(fname)
        

            print() 
            p.prCyan('-'*85)

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
        '''

if __name__ == '__main__':
    main()
