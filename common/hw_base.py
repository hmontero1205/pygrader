"""hw.py: Base class for all HW's"""

import os
import sys
import json
from pathlib import Path

from common.rubric_item import RubricItem
import common.utils as u
import common.printing as printing
import common.submissions as subs

class HW():
    """Grading Base Class

    Attributes:
        hw: the hw #
        root: Path of the form '~/.grade/hw{1,...,8}', which contains the
            grade_dir, deadline.txt, and grades.json
        grade_dir: The student/team's submission directory.
    """

    def __init__(self, hw, root, rubric_file):
        self.hw = hw
        self.root = os.path.join(Path.home(), ".grade", root)
        self.rubric = self.create_rubric(rubric_file)
        self.grade_dir = None  # Populated in subclasses.

    def create_rubric(self, rubric_file):
        """Parses a JSON rubric file into a Python representation."""

        #TODO check if file exists
        with open(rubric_file, "r") as f:
            rubric_json = json.load(f)

        rubric = {}
        for table_k, table_v in rubric_json.items():
            if table_k not in rubric:
                rubric[table_k] = {}

            for item in table_v:
                # TODO: If the grade_* doesn't exist, should we link our generic
                # grade() function?
                ri_obg = RubricItem(
                            table_v[item]['name'],
                            list(zip(table_v[item]['points_per_subitem'],
                                    table_v[item]['desc_per_subitem'])),
                            getattr(self, "grade_" + item, self.grade))
                rubric[table_k][item] = ri_obg
        return rubric

    def do_cd(self, path):
        """Changes directory relative to the root of the student submission.

        For example, if you had the following:
            hw3
            \_ part1
               \_ part1-sub

        and you wanted to cd into part1-sub, you would run
        `do_cd(os.path.join('part1', 'part1-sub'))`.
        """
        part_dir = os.path.join(self.grade_dir, path)
        u.is_dir(part_dir)
        os.chdir(part_dir)

    def exit_handler(self, _signal, _frame):
        """Handler for SIGINT

        Note: this serves as a template for how the subclasses should do it.
        The subclass is free to override this function with more hw-specific
        logic.
        """
        printing.print_cyan("\n[ Exiting generic grader... ]")
        self.cleanup()
        sys.exit()

    def check_late_submission(self):
        """Grabs the latest commit timestamp to compare against the deadline"""
        proc = u.cmd_popen("git log -n 1 --format='%aI'")
        iso_timestamp, _ = proc.communicate()

        return subs.check_late(os.path.join(self.root, "deadline.txt"),
                               iso_timestamp.strip('\n'))

    def grade(self):
        """Generic grade function."""
        # TODO or should we raise NotImplementedError instead?
        printing.print_red("[ Opening shell, ^D/exit when done. ]")
        os.system("bash")

    def setup(self):
        """Performs submission setup (e.g. untar, git checkout tag)."""

    def cleanup(self):
        """Performs cleanup (kills stray processes, removes mods, etc.)."""
