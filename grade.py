#!/usr/bin/python3

"""grade.py: Generic grading framework"""

import os
import json
import signal
import argparse
import subprocess

import common.printing as p
import common.utils as utils
from hw1.hw1 import HW1

def main():
    """Entry-point into the grader"""
    parser = argparse.ArgumentParser(description="Entry point to grade OS HWs")

    parser.add_argument("hw", type=str, help="homework # to grade")
    parser.add_argument("student", type=str,
                        help="the name of student/group to grade")
    parser.add_argument("table", type=str, help="table to grade")

    flags = parser.add_mutually_exclusive_group()
    flags.add_argument("--amend", action="store_true", help=("Amend comment "
        "without rerunning test for that item"), dest="amend")
    flags.add_argument("--continue", action="store_true", help=("Continue "
        "from last graded item"), dest="continue_grader")
    flags.add_argument("--grade-only", action="store_true", help=("Grade "
        "without running any tests"), dest="grade_only")
    flags.add_argument("--regrade", action="store_true", help="Regrade an item",
        dest="regrade")
    flags.add_argument("--test-only", action="store_true", help=("Run tests "
        "without grading"), dest="test_only")

    args = parser.parse_args()
    env = {
            "amend": args.amend,
            "continue_grader": args.continue_grader,
            "grade_only": args.grade_only,
            "regrade": args.regrade,
            "test_only": args.test_only
          }

    # TODO: is passing in args.table twice redundant?
    tester = Grader(args.hw, args.student, args.table, env)
    tester.grade(args.table)
    tester.pretty_print_grades()

class Grader():
    """Represents the current hw grading session

    Attributes:
        hw: Homework # being graded (e.g. hw1)
        table: Table code being graded (based on AP/OS-style rubrics)
        student: Team/uni of the submission
        hw_class: The object representing this homework (rubric, testers)
        env: Flags determining grader behavior (see main routine for argsparse)
        grades_file: Path to JSON file containing session grades
        grades: Maps (uni/team) -> (rubric item -> (pts, comments))
    """
    def __init__(self, hw, student, table, env):
        self.hw = hw
        self.table = table
        self.student = student
        self.env = env
        self.grades = dict()  # TODO: we should keep a LATE flag in here

        self.hw_class = HW1(self.student)
        signal.signal(signal.SIGINT, self.hw_class.signal_handler)

        # Let's check if we have a grading session already
        self.grades_file = os.path.join(self.hw_class.root, ".grades.json")
        if utils.file_exists(self.grades_file):
            with open(os.path.join(self.grades_file), "r") as f:
                self.grades = json.load(f)

        # Is this our first time grading this student? If so, create a new
        # entry with null fields.
        if self.student not in self.grades.keys():
            self.grades[self.student] = dict()
            for table_key in sorted(self.hw_class.rubric.keys()):
                for section in sorted(self.hw_class.rubric[table_key].keys()):
                    # None means that it hasn't been graded yet
                    self.grades[self.student][section] = {"pts": None,
                                                          "comments": None}

    def pretty_print_grades(self):
        """Prints (uni, pts, comments) in tsv format"""
        total_pts = 0
        all_comments = ""
        student_grades = self.grades[self.student]
        for item in student_grades.keys():
            if student_grades[item]["pts"] is None:
                continue

            total_pts += student_grades[item]["pts"]
            item_comments = student_grades[item]["comments"]
            if item_comments:
                all_comments += f"{item_comments}; "
        print(f"{self.student}\t{total_pts}\t{all_comments}")
        with open(os.path.join(self.grades_file), "w") as f:
            json.dump(self.grades, f, indent=4)  # Indent for pretty printing :)

    def print_intro(self, part):
        p.print_intro(self.student, self.hw, part)

    def print_header(self, section):
        p.print_double()
        p.print_green('Grading {}'.format(section.table_item))
        self.print_desc(section)
        p.print_double()

    def print_desc(self, section):
        for i, d in enumerate(section.desc):
            p.print_light_purple("{}.{} ({}p): {}".format(section.table_item,
                i+1, d[0], d[1]))

    def ask_action(self):
        p.print_yellow("Run test again (a)")
        p.print_yellow("Open shell & run again (s)")
        p.print_yellow("Continue (enter)")

        while True:
            try:
                usr_input = input(f"{p.CRED}Enter an action [a|s]:  {p.CEND}")
                break
            except EOFError as _:
                print("^D")
                continue

        if usr_input == 'a':
            return True
        elif usr_input == 's':
            p.print_red("^D/exit to end shell session")
            subprocess.run("bash", shell=True)
            return True
        else:
            return False

    def apply_grade(self, section):
        if self.grades[self.student][section.table_item]["pts"] is not None:
            # We've graded this already. Let's show the current grade.
            pts = self.grades[self.student][section.table_item]["pts"]
            cmts = self.grades[self.student][section.table_item]["comments"]
            p.print_green(f"[ Previously,  {pts} / '{cmts}']")

        while True:
            try:
                pts = int(input("{} ({}p): ".format(section.table_item,
                    sum(x[0] for x in section.desc))))
                break
            except (ValueError, EOFError) as e:
                if isinstance(e, EOFError):
                    print("^D")
                continue

        self.grades[self.student][section.table_item]["pts"] = pts
        cmts = input("Comments: ")
        self.grades[self.student][section.table_item]["comments"] = cmts

    def check_if_graded(self, sec_code):
        return self.grades[self.student][sec_code]["pts"] is not None

    def grade(self, key):
        # The intro should be modified to account for when we grade all vs.
        # one section vs. one table
        self.print_intro(key)
        if key == 'all':
            self.grade_all()
        elif key.isalpha():
            # e.g. A, B, C, ...
            self.grade_table(key)
        else:
            # e.g. A1, B4, ...
            table = key[0]
            section = self.hw_class.rubric[table][key]
            self.grade_section(section)

    def grade_all(self):
        for table in self.hw_class.rubric:
            self.grade_table(table)

    def grade_table(self, table_key):

        # TODO: figure out where exactly this should be called...
        # Also, we need to set some sort of flag in the grades dict
        self.hw_class.check_late_submission()
        table_keys = [*self.hw_class.rubric.keys()]

        if table_key not in table_keys:
            return 0

        table = self.hw_class.rubric[table_key]

        for section in table:
            self.grade_section(table[section])

    def grade_section(self, section):
        if (self.env["continue_grader"]
            and self.check_if_graded(section.table_item)):
            p.print_yellow(f"[ {section.table_item} has been graded, skipping... ]")
            return

        if not self.env["grade_only"]:
            run = True
            while run:
                # TODO: move below to printing mod
                self.print_header(section)
                section.tester()
                p.print_line()
                run = self.ask_action()
        if not self.env["test_only"]:
            p.print_line()
            self.print_desc(section)
            self.apply_grade(section)
            print("\n\n")

if __name__ == '__main__':
    main()
