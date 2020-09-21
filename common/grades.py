"""
grades.py: Logic for storing points/comments while grading
"""
import os
import sys
import json
from typing import Set, Dict, Union, Optional, Tuple

import common.utils as utils

LATE_PENALTY = .2

# Probably better to just look at a grades.json
GradesDictType = Dict[str, # Submitter
                      Dict[str, Union[bool, # is_late
                                      Dict[str, # subitem_code
                                           Dict[str, # award/comments
                                                Union[bool, str]]]]]]

class Grades():
    """Represents the grades for the current hw

    Attributes:
        grades_file: the JSON file with grades
        rubric: the rubric object for a given hw
        submitter: The uni/team we're currently grading
        _grades: Maps submitter -> (is_late, (item -> (pts, comments)))
    """
    def __init__(self, grades_file, rubric, name):
        self.grades_file = os.path.abspath(grades_file)
        self.rubric = rubric
        self.submitter = name
        self._grades = self.load_grades()

        if self.submitter and self.submitter not in self._grades:
            # This is the first time grading the submission
            self.add_submission_entry()
        self.synchronize()

    def _get_defined_rubric_subitems(self) -> Set[str]:
        subitems = set()
        for table_code in sorted(self.rubric.keys()):
            for item_code in sorted(self.rubric[table_code].keys()):
                item = self.rubric[table_code][item_code]
                for subitem_code in range(1, len(item.subitems) + 1):
                    code = f"{item_code}.{subitem_code}"
                    if code in subitems:
                        sys.exit(f"Rubric subitem '{code}' defined twice!")

                    subitems.add(code)

        return subitems

    def load_grades(self) -> GradesDictType:
        """Returns a dictionary representation of the TA's grades thus far"""
        if not utils.file_exists(self.grades_file):
            # The TA hasn't started grading this hw yet
            return dict()

        with open(self.grades_file, "r") as f:
            grades = json.load(f)

        # Let's traverse over the rubric and make sure to adjust the dict if
        # anything has changed.
        defined_subitems = self._get_defined_rubric_subitems()
        for grade_info in grades.values():
            scores = grade_info["scores"]
            present_subitems = set(scores.keys())

            for code in defined_subitems.symmetric_difference(present_subitems):
                if code not in defined_subitems:
                    scores.pop(code)
                    continue

                assert code not in present_subitems
                scores[code] = {"award": None, "comments": None}


        return grades

    def add_submission_entry(self):
        """Create a new entry for student/team with null fields"""
        self._grades[self.submitter] = dict()
        self._grades[self.submitter]["is_late"] = False
        rubric_scores = dict()
        for table_code in sorted(self.rubric.keys()):
            for item_code in sorted(self.rubric[table_code].keys()):
                item = self.rubric[table_code][item_code]
                for subitem_code in range(1, len(item.subitems) + 1):
                    code = f"{item_code}.{subitem_code}"
                    # None means that it hasn't been graded yet
                    rubric_scores[code] = {"award": None, "comments": None}
        self._grades[self.submitter]["scores"] = rubric_scores

    def __getitem__(self, rubric_subitem) -> Dict[str, Union[bool, str]]:
        """Wrapper around self._grades for convenience"""
        return self._grades[self.submitter]["scores"][rubric_subitem]

    def synchronize(self):
        """Write out the grades dictionary to the filesystem"""
        with open(self.grades_file, "w") as f:
            # Indent for pretty printing :^)
            json.dump(self._grades, f, indent=4, sort_keys=True)

    def is_graded(self, code: str, name: Optional[str] = None) -> bool:
        """Checks if a subitem has been graded yet"""
        if not name:
            name = self.submitter
        # TODO: yikes, 4 dictionary accesses xD. is there a better way?
        return (self._grades[name]["scores"][code]["award"]
                is not None)

    def is_late(self, name: Optional[str] = None) -> bool:
        """Getter for is_late"""
        if not name:
            name = self.submitter
        return self._grades[name]["is_late"]

    def set_late(self, opt: bool):
        """Setter for is_late"""
        self._grades[self.submitter]["is_late"] = opt

    def dump_grades(self, submitter: str, rubric_code: str):
        all_pts = 0
        graded_submissions = 0

        if submitter:
            self.print_submission_grades(submitter, rubric_code)
        else:
            for name in sorted(self._grades):
                is_graded, total_pts = self.print_submission_grades(name,
                                                                    rubric_code)
                all_pts += total_pts
                if is_graded:
                    graded_submissions += 1


            avg = (round(all_pts / graded_submissions, 2) if graded_submissions
                   else 0)
            print(f"\nAverage across {graded_submissions} "
                  f"graded submission(s): {avg}")


    def print_submission_grades(
            self, name: Optional[str] = None,
            rubric_code: Optional[str] = None) -> Tuple[bool, float]:
        """Prints (uni, pts, comments) in tsv format

        Returns:
            A tuple with two members: a bool indicating whether or not this
            submission was even graded yet and a float representing the total
            score of this submission. If it hasn't been graded yet, this float
            should be zero.

            NOTE: We only apply the late penalty if the TA requested ALL grades
            (such that rubric_code = 'ALL'.
        """
        if not name:
            name = self.submitter

        if not rubric_code:
           rubric_code = "ALL"

        total_pts = 0
        all_comments = []
        graded = False
        submission_scores = self._grades[name]["scores"]

        for rubric_item_mappings in self.rubric.values():
            for item_code, rubric_item in rubric_item_mappings.items():
                if(rubric_code != "ALL"
                   and not item_code.startswith(rubric_code)
                   or not self.is_graded(f"{item_code}.1", name)):
                    continue
                graded = True
                for i, (pts, _) in enumerate(rubric_item.subitems, 1):
                    code = f"{item_code}.{i}"
                    raw_pts = pts if submission_scores[code]["award"] else 0
                    total_pts += raw_pts
                    ta_comments = submission_scores[code]["comments"]
                    item_comments = ""

                    if (((raw_pts and item_code.startswith("A"))
                        or (not raw_pts and not item_code.startswith("A"))) or
                            ta_comments):
                        # Always print the code if points were not awarded for
                        # a subitem. Table A is deductive points though, so
                        # we prepend the code if it was awarded.

                        # If a section only has one item, print A2 instead of
                        # A2.1 since that's how we stylize our rubrics.
                        pretty_code_name = (item_code
                                            if len(rubric_item.subitems) == 1
                                            else code)
                        item_comments += f"({pretty_code_name})"

                    if ta_comments:
                        item_comments += f" {ta_comments}"

                    if item_comments:
                        all_comments.append(item_comments)

        # We assume that if the TA wants ALL submission grades, that they'll
        # also want to apply late penalities (they're about to finalize grades).
        # Otherwise, we just just dump raw grades for reference.
        if rubric_code == "ALL" and self.is_late(name):
            all_comments.insert(0, "(LATE)")
        concatted_comments = "; ".join(all_comments)

        if rubric_code == "ALL" and self.is_late(name):
            total_pts = round(total_pts * (1 - LATE_PENALTY), 2)

        total_pts = max(total_pts, 0)

        if graded:
            print(name, total_pts, concatted_comments, sep='\t')
        else:
            print(name, "n/a", "n/a", sep='\t')

        return graded, total_pts
