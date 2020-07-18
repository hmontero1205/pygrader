#!/usr/bin/python3

"""grade.py: Generic grading framework"""

import os
import argparse

from common import printing as p
from hw1.hw1 import HW1

def main():
    """Entry-point into the grader"""
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
    """Represents the current hw grading session

    Attributes:
        hw: Homework # being graded (e.g. hw1)
        table: Table code being graded (based on AP/OS-style rubrics)
        student: Team/uni of the submission
        pts: Points this submission has earned
        comments: Comments left by the grader for this submission
        rubric: The Rubric object representing this homework
    """

    def __init__(self, hw, student, table):
        self.hw = hw
        self.table = table
        self.student = student
        self.pts = 0
        self.comments = ""

        hw_class = HW1("./hw1", self.student)
        self.rubric = hw_class.rubric

    def print_intro(self, name, part):
        """Print the intro banner for this session"""
        p.print_intro(name, self.hw, part)

    def run_and_prompt(self, section):
        """Runs a grading item and prompts for actions afterwards"""
        while True:
            # TODO: move below to printing mod
            p.print_cyan('-'*85)
            p.print_green('Grading {}'.format(section.table_item))
            for i, desc in enumerate(section.desc):
                p.print_light_purple("{}.{} ({}p): {}"
                                     .format(section.table_item,
                                             i+1,
                                             section.points[i],
                                             desc))
            p.print_cyan('-'*85)

            section.tester()

            p.print_cyan('-'*85)
            p.print_green("End test of {}".format(section.table_item))
            p.print_cyan('='*85)

            p.print_yellow("Run test again (a)")
            p.print_yellow("Open shell & run again (s)")
            p.print_yellow("Continue (enter)")
            usr_input = input("\033[91mEnter an action [a|s]:  \033[00m")
            if usr_input == 'a':
                continue
            elif usr_input == 's':
                p.print_red("^D/exit to end shell session")
                os.system("bash")
                continue
            else:
                break
        for i, desc in enumerate(section.desc):
            p.print_light_purple("{}.{} ({}p): {}".format(section.table_item,
                                                          i+1,
                                                          section.points[i],
                                                          desc))
        while True:
            try:
                pts = int(input("{} ({}p): ".format(section.table_item,
                                                    sum(section.points))))
                break
            except ValueError as _:
                p.print_red("Enter an int pls...")
        self.pts += int(pts)
        cmts = input("Comments: ")
        if cmts:
            self.comments += "{}; ".format(cmts)
        print("\n\n")

    def grade_table(self, table_key, student):
        """Starts interactive session for grading the table"""
        self.print_intro(student, table_key)
        table_keys = [*self.rubric.keys()]

        if table_key not in table_keys:
            return 0

        table = self.rubric[table_key]

        for section in table:
            self.run_and_prompt(table[section])

if __name__ == '__main__':
    main()
