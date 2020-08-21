#!/usr/bin/python3

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
        hw:         the hw subclass
        root:       ~/.grade/hw{1,...,8} contains the grade_dir, deadline.txt,
                    and grades.json
        student:    the team/student to be graded
    """

    def __init__(self, hw, root, rubric_file):
        self.hw = hw
        self.root = os.path.join(Path.home(), ".grade", root)
        self.rubric = self.create_rubric(rubric_file)
        self.signal_handler = self.exit_handler
        self.grade_dir = None

    def create_rubric(self, rubric_file):

        #TODO check if file exists

        with open(rubric_file, "r") as f:
            rubric_json = json.load(f)

        rubric = {}
        for table_k, table_v in rubric_json.items():
            if table_k not in rubric:
                rubric[table_k] = {}

            for item in table_v:
                ri_obg = RubricItem(
                            table_v[item]['name'],
                            list(zip(table_v[item]['points_per_subitem'],
                                    table_v[item]['desc_per_subitem'])),
                            getattr(self, "grade_" + item, self.grade))
                rubric[table_k][item] = ri_obg
        return rubric

    def do_cd(self, path):
        part_dir = os.path.join(self.grade_dir, path)
        u.is_dir(part_dir)
        os.chdir(part_dir)

    def exit_handler(self, _signal, _frame):
        """Handler for SIGINT"""
        printing.print_cyan("\n[ Exiting hw3 grader... ]")
        self.cleanup()
        sys.exit()

    def check_late_submission(self):
        """Grabs the latest commit timestamp to compare against the deadline"""
        proc = u.cmd_popen("git log -n 1 --format='%aI'")
        iso_timestamp, _ = proc.communicate()

        return subs.check_late(os.path.join(self.root, "deadline.txt"),
                               iso_timestamp.strip('\n'))

    def grade(self):
        print("this item is not implemented (should open shell)")

    def setup(self):
        pass

    def cleanup(self):
        pass
