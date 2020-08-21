#!/usr/bin/python3

"""grade.py: Generic grading framework"""

import os
import sys
import signal
import argparse
import subprocess

import common.printing as p
from common.grades import Grades
from hw1.hw1 import HW1, HW1_ALIASES
from hw3.hw3 import HW3, HW3_ALIASES

GRADES_FILE = "./grade.json"

GRADES_FILE = "./grade.json"

def main():
    """Entry-point into the grader"""
    parser = argparse.ArgumentParser(description="OS HW Grading Framework")

    parser.add_argument("hw", type=str, help="homework to grade")
    parser.add_argument("student", type=str, nargs="?", default=None,
                        help="the name of student/group to grade")
    parser.add_argument("-c", "--code", type=str, nargs="?", default="all",
                        help=("rubric item (e.g. A, B4) to grade; "
                              "defaults to all"))

    grading_mode = parser.add_mutually_exclusive_group()
    grading_mode.add_argument("-g", "--grade-only", action="store_true",
                              help="grade without running any tests",
                              dest="grade_only")
    grading_mode.add_argument("-t", "--test-only", action="store_true",
                        help=("run tests without grading"), dest="test_only")
    script_mode = parser.add_mutually_exclusive_group()
    script_mode.add_argument("-r", "--regrade", action="store_true",
                             help="do not skip previously graded items",
                             dest="regrade")
    script_mode.add_argument("-d", "--dump-grades", action="store_true",
                             help=("dump grades for this homework -- "
                                   "all if no student specified"),
                             dest="dump_grades")

    args = parser.parse_args()
    env = {
            "regrade": args.regrade,
            "grade_only": args.grade_only,
            "test_only": args.test_only,
            "dump_grades": args.dump_grades
          }

    rubric_code = args.code if args.code else "all"

    tester = Grader(args.hw, args.student, rubric_code, env)
    if args.dump_grades:
        tester.grades.dump_grades(args.student, rubric_code.upper())
        sys.exit()

    if not args.student:
        sys.exit("unspecified student/team")
    tester.grade()

    # TODO: add progress/percentage complete?
    p.print_light_purple("\n[ Pretty-printing pts/comments up until now... ]")
    tester.grades.print_submission_grades()

    # clean up
    tester.hw_class.cleanup()

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
        self.hw_class = self._get_hw_class()

        signal.signal(signal.SIGINT, self.hw_class.signal_handler)

        self.grades_file = os.path.join(self.hw_class.root, "grades.json")
        self.grades = Grades(self.grades_file, self.hw_class.rubric,
                             self.student)

    def _get_hw_class(self):
        if self.hw.lower() in HW1_ALIASES:
            return HW1(self.student)
        elif self.hw.lower() in HW3_ALIASES:
            return HW3(self.student)
        else:
            sys.exit(f"Unsupported assignment: {self.hw}")

    def print_intro(self, part):
        p.print_intro(self.student, self.hw, part)

    def print_header(self, section):
        p.print_double()
        p.print_green('Grading {}'.format(section.table_item))
        self.print_desc(section)
        p.print_double()

    def print_desc(self, section):
        for i, (pts, desc) in enumerate(section.desc, 1):
            p.print_light_purple("{}.{} ({}p): {}".format(section.table_item,
                                                          i, pts, desc))

    def ask_action(self):
        p.print_yellow("Run test again (a)")
        p.print_yellow("Open shell & run again (s)")
        p.print_yellow("Continue (enter)")

        while True:
            try:
                usr_input = input(f"{p.CBLUE2}Enter an action [a|s]:  {p.CEND}")
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

    def print_section_grade(self, code):
        if self.grades.is_graded(code):
            # We've graded this already. Let's show the current grade.
            awarded = self.grades[code]["award"]
            comments = self.grades[code]["comments"]
            p.print_green(f"[ Previous Grade: awarded={awarded} "
                          f"comments='{comments}']")

    def prompt_grade(self, section):
        """Prompts the TA for pts/comments"""
        # self.print_desc(section)
        for i, (pts, desc) in enumerate(section.desc, 1):
            subitem_code = f"{section.table_item}.{i}"
            p.print_light_purple(f"{subitem_code} ({pts}p): {desc}")
            self.print_section_grade(subitem_code)
            while True:
                try:
                    award = input(f"{p.CBLUE2}Award? [y/n]: {p.CEND}")
                    if award in ('y', 'n'):
                        break
                except EOFError as _:
                    print("^D")
                    continue
            while True:
                try:
                    comments = input(f"{p.CBLUE2}Comments: {p.CEND}")
                    break
                except EOFError as _:
                    print("^D")
                    continue

            self.grades[subitem_code]["award"] = (award == 'y')
            self.grades[subitem_code]["comments"] = comments

        self.grades.synchronize()

    def _check_valid_table(self, table_key):
        """Given a key (i.e A, C, N) check if its a valid rubric table"""

        keys = [*self.hw_class.rubric.keys()]
        if table_key not in keys:
            raise ValueError(f"{self.hw} does not have table {table_key}")

    def _check_valid_item(self, item_key):
        """Given a table item (i.e. A1, B2, D9) check if it is valid.

        Assumes the table is valid (use _check_valid_table() for validation on
        that).
        """
        keys = [*self.hw_class.rubric[item_key[0]].keys()]
        if item_key not in keys:
            raise ValueError(f"{self.hw} does not have rubric item {item_key}")

    def grade(self):
        # The intro should be modified to account for when we grade all vs.
        # one section vs. one table
        key = self.table
        self.print_intro(key)
        if key.lower() == 'all':
            self.grade_all()
        elif key.isalpha():
            # e.g. A, B, C, ...
            table = key.upper()
            self._check_valid_table(table)
            self.grade_table(table)
        else:
            # e.g. A1, B4, ...
            table = key[0].upper()
            item = key.upper()
            self._check_valid_table(table)
            self._check_valid_item(item)
            section = self.hw_class.rubric[table][item]
            self.grade_section(section)

    def grade_all(self):
        for table in self.hw_class.rubric:
            self.grade_table(table)

    def grade_table(self, table_key):

        table = self.hw_class.rubric[table_key]

        for section in table:
            self.grade_section(table[section])

    def grade_section(self, section):
        if (not self.env["regrade"]
            and self.grades.is_graded(f"{section.table_item}.1")):
            p.print_yellow(
                    f"[ {section.table_item} has been graded, skipping... ]")
            return

        # if -g is not provided, run tests else skip tests
        if not self.env["grade_only"]:
            run = True
            while run:
                self.print_header(section)
                section.tester()
                p.print_line()
                run = self.ask_action()

        # if -t is not provided, ask for grade. If -t is provided skip
        if not self.env["test_only"]:
            p.print_line()
            is_late = self.hw_class.check_late_submission()
            if is_late:
                self.grades.set_late(True)
            # self.print_desc(section)
            # self.print_section_grade(section)
            self.prompt_grade(section)
            print()
        else:
            # Let the grader know if the item was graded yet
            self.print_section_grade(section)


if __name__ == '__main__':
    main()
