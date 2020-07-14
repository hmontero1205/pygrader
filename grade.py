#!/usr/bin/python3
import os
import sys
import argparse
import subprocess

sys.path.insert(0, "common")
import common.printing as p
sys.path.insert(0, "hw1")
from hw1 import HW1

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="path to the homework to grade")
    parser.add_argument("student", type=str,
                        help="the name of student/group to grade")
    parser.add_argument("table", type=str, help="table to grade")

    args = parser.parse_args()

    tester = Grader(args.hw, args.student, args.table)

    tester.grade_table(args.table, args.student)

    print("Table {} pts: {}".format(args.table, tester.pts))
    print(tester.comments)

class Grader():

    def __init__(self, hw, student, table):

        self.hw = hw
        self.table = table
        self.student = student
        self.pts = 0
        self.comments = ""

        hw_class = HW1("./hw1", self.student)
        self.rubric = hw_class.rubric

    def print_intro(self, name, part):
        p.prIntro(name, self.hw, part)

    def run_and_prompt(self, section):
        while True:
            # TODO: move below to printing mod
            p.prCyan('-'*85)
            p.prGreen('Grading {}'.format(section.table_item))
            for i, d in enumerate(section.desc):
                p.prLightPurple("{}.{} ({}p): {}".format(section.table_item,
                                                           i+1,
                                                           section.points[i],
                                                           d))
            p.prCyan('-'*85)

            section.tester()

            p.prCyan('-'*85)
            p.prGreen("End test of {}".format(section.table_item))
            p.prCyan('='*85)

            p.prYellow("Run test again (a)")
            p.prYellow("Open shell & run again (s)")
            p.prYellow("Continue (enter)")
            usr_input = input("\033[91mEnter an action [a|s]:  \033[00m")
            if usr_input == 'a':
                continue
            elif usr_input == 's':
                p.prRed("^D/exit to end shell session")
                os.system("bash")
                continue
            else:
                break
        for i, d in enumerate(section.desc):
                p.prLightPurple("{}.{} ({}p): {}".format(section.table_item,
                                                           i+1,
                                                           section.points[i],
                                                           d))
        while True:
            try:
                pts = int(input("{} ({}p): ".format(section.table_item,
                                                    sum(section.points))))
                break
            except ValueError as e:
                p.prRed("Enter an int pls...")
        self.pts += int(pts)
        cmts = input("Comments: ")
        if cmts:
            self.comments += "{}; ".format(cmts)
        print("\n\n")

    def grade_table(self, table_key, student):

        self.print_intro(student, table_key)
        table_keys = [*self.rubric.keys()]

        if table_key not in table_keys:
            return 0

        table = self.rubric[table_key]

        for section in table:
            self.run_and_prompt(table[section])

if __name__ == '__main__':
    main()
