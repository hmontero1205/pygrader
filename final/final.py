#!/usr/bin/python3

"""final.py: Grading logic for Fridge"""

from typing import Optional
import os
import sys

import git

from common.submissions import checkout_to_team_master, tag
from common.hw_base import HW, directory
import common.utils as u
import common.printing as printing

HW_NAME = "final"
HW6_ALIASES = {HW_NAME, "exam2"}
RUBRIC_NAME = "final_rubric.json"
Q_START = "Q{}"
Q_END = "================================================================================"
GITDIFF = "git difftool --tool=vimdiff2 `git rev-list HEAD | tail -n 1` HEAD {}"
COMMITCOUNT = "git rev-list | wc -l"

class Final(HW):
    """Grading rubic and tests for OS HW5: fridge

    Attributes:
        scripts_dir: The directory containing the hw1 grading scripts
        submission_dir: The submission directory
        submitter: The name of the student/team
        rubric: Python representation of the rubric
        exit_handler: SIGINT handler
    """

    def __init__(self, submitter: Optional[str]):
        # Set up the minimum to at least dump grades for all students
        super().__init__(HW_NAME, RUBRIC_NAME)
        self.submitter = submitter

        self._correct_answers = os.path.join(self.scripts_dir, "written_answers.txt")

        if submitter:
            self.submission_dir = os.path.join(self.hw_workspace, HW_NAME)

            try:
                u.is_dir(self.submission_dir)
            except ValueError:
                sys.exit("Please run hw_setup before grading")

            os.chdir(self.submission_dir)
            self._written_answers = "written_answers.txt"

            self.repo = git.Repo(self.submission_dir)

            if not self.setup():
                sys.exit(f"Couldn't pull {submitter}'s submission!")

    def exit_handler(self, _signal, _frame):
        """Handler for SIGINT"""
        printing.print_cyan("\n[ Exiting final grader... ]")
        self.cleanup()
        sys.exit()

    def setup(self) -> bool:
        return checkout_to_team_master(self.repo, HW_NAME, self.submitter)

    def cleanup(self):
        """Post final cleanup"""
        self.repo.git.checkout("--", "*")
        self.repo.git.checkout("master")
        self.repo.git.clean("-f", "-d")

    @property
    def written_answers(self):
        self._written_answers = u.get_file(self._written_answers)
        return self._written_answers

    @property
    def correct_answers(self):
        self._correct_answers = u.get_file(self._correct_answers)
        return self._correct_answers

    @directory("root")
    def grade_A1(self):
        if u.run_cmd(COMMITCOUNT) > 1: 
            printing.print_green("[ PASS: at least 1 commit ]")
        else:
            printing.print_red("[ FAIL: no attempt ]")
        

    def _extract_from_file(self, fname, start, end=None):

        if not end: 
            result = u.extract_between(fname,
                                   Q_START.format(start),
                                   Q_START.format(end), True)
        else:
            result = u.extract_between(fname,
                                   Q_START.format(start),
                                   Q_END, True)

        if result.returncode != 0:
            printing.print_red("[ Fail: could not extract answer dropping into shell ]")
            print(result.stderr)
            os.system("bash")
            return -1
        return result.stdout

    def _extract_correct(self, start, end=None):
        return self._extract_from_file(self.correct_answers, start, end)

    def _extract_answer(self, start, end=None):
        return self._extract_from_file(self.written_answers, start, end)

    @directory("root")
    def grade_B1(self):
        sa = self._extract_answer(1, 2)
        ca = self._extract_correct(1, 2)
        if sa == -1:
            return

        printing.print_magenta("[ Students answer ]")
        print(sa)
        printing.print_cyan("[ Correct Answer ]")
        printing.print_cyan(ca)

    @directory("root")
    def grade_B2(self):
        sa = self._extract_answer(2,3)
        ca = self._extract_correct(2,3)
        if sa == -1:
            return

        printing.print_magenta("[ Students answer ]")
        print(sa)
        printing.print_cyan("[ Correct Answer ]")
        printing.print_cyan(ca)

    @directory("root")
    def grade_B3(self):
        sa = self._extract_answer(3)
        ca = self._extract_correct(3)
        if sa == -1:
            return
        
        printing.print_magenta("[ Students Answer ]")
        print(sa)
        printing.print_cyan("[ Correct Answer ]")
        printing.print_cyan(ca)
    
    @directory("taskfs")
    def grade_C1(self):
        printing.print_magenta(" Lookup ]")
        input("[ Press enter to view taskfs.c ]")
        u.inspect_file("taskfs.c")

    @directory("taskfs")
    def grade_C2(self):
        pass

    @directory("taskfs")
    def grade_C3(self):
        pass

