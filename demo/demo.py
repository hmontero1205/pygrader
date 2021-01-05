"""demo.py: Sample grading logic for a coding assignment"""

from typing import Optional
import os
import sys

import git

from common.hw_base import HW, directory
import common.utils as u
import common.printing as pr

HW_ROOT = "demo"
DEMO_ALIASES = {"tutorial", "demo", "meme"}
RUBRIC_NAME = "demo_rubric.json"

class DEMO(HW):
    """Grading rubic and tests for demo assignment
    Attributes:
        scripts_dir: The directory containing the grading scripts
        submission_dir: The submission directory
        submitter: The name of the student/team
        rubric: Python representation of the rubric
        exit_handler: SIGINT handler
    """

    def __init__(self, submitter: Optional[str]):
        # Set up the minimum to at least dump grades for all students
        super().__init__("demo", RUBRIC_NAME)
        self.submitter = submitter

        if submitter:
            self.submission_dir = os.path.join(self.hw_workspace, self.submitter)

            try:
                u.is_dir(self.submission_dir)
            except ValueError:
                sys.exit("Please run hw_setup before grading")

            os.chdir(self.submission_dir)

            self.repo = git.Repo(self.submission_dir)

            if not self.setup():
                sys.exit(f"Couldn't setup {submitter}'s submission!")

        # Initialize other properties here
        self.written_answers = "written_answers.txt"

    def exit_handler(self, _signal, _frame):
        """Handler for SIGINT"""
        pr.print_cyan("\n[ Exiting demo grader... ]")
        self.cleanup()
        sys.exit()

    def setup(self) -> bool:
        """Do any necessary setup for the submission"""
        # In this case, we aren't pulling from a repo or untaring something.
        # Let's just make sure the submission is clean.
        self.cleanup()
        return True

    def cleanup(self):
        """Post demo cleanup"""
        # Remove any local changes the grader may have made 
        self.repo.git.checkout("--", "*")
        self.repo.git.checkout("master")
        self.repo.git.clean("-f", "-d")

    @directory("root")
    def grade_A1(self):
        """A1: check for compilation artifacts"""
        # -a for all files
        # -C for colorized output
        # -I to ignore the .git dir
        u.run_cmd("tree -a -C -I '.git'")

    @directory("root")
    def grade_A2(self):
        """A2: git commits"""
        cmd = ("git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%C"
               "reset %s %Cgreen(%cD) %C(bold blue)<%an>%Creset' "
               "--abbrev-commit")
        u.run_cmd(cmd)

    @directory("root")
    def grade_B1(self):
        """B1: written answers"""
        u.extract_between(self.written_answers, # File
                          "= Q1 =", # Top barrier
                          "= Q2 =", # Bottom barrier
                          ) # This call displays the student's answer for Q1

        u.prompt_continue() # Don't display Q2 until grader presses enter

        u.extract_between(self.written_answers, "= Q2 =", "= Q3 =")
        u.prompt_continue()
        u.extract_between(self.written_answers, "= Q3 =", "======")

    @directory("swap") # cd into swap/ before running function
    def grade_C1(self):
        """C1: static analysis"""
        input(f"{pr.CVIOLET2}[ Press enter to view Makefile ]{pr.CEND}")
        u.inspect_file("Makefile") # Opens file in bat (a better cat)

        input(f"\n{pr.CVIOLET2}[ Press enter to view swap() ]{pr.CEND}")
        swap_fn = u.extract_function("swap.c", "swap")
        u.inspect_string(swap_fn, lang="c")

    @directory("swap")
    def grade_C2(self):
        """C2: dynamic analysis"""
        if u.compile_code(): # Non-zero exit code (e.g. compilation failed)
            return

        swap = u.cmd_popen(f"{os.path.join(os.getcwd(), 'swap')} 1 2")
        out, code = swap.communicate()

        if code:
            pr.print_red("[ Non-zero exit code ]")

        print(out)
        if out.splitlines()[1] == "After: 2 1":
            pr.print_green("[ PASS ]")
        else:
            pr.print_red("[ FAIL ] Didn't match 'After: 2 1'")

