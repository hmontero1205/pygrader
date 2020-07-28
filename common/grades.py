"""
grades.py: Logic for storing points/comments while grading
"""
import os
import json
import common.utils as utils

LATE_PENALTY = .2

class Grades():
    """Represents the grades for the current hw

    Attributes:
        grades_file: the JSON file with grades
        rubric: the rubric object fot a given hw
        submission_name: The uni/team we're currently grading
        _grades: Maps submission_name -> (is_late, (item -> (pts, comments)))
    """
    def __init__(self, grades_file, rubric, name):
        self.grades_file = os.path.abspath(grades_file)
        self.rubric = rubric
        self.submission_name = name
        self._grades = self.load_grades()

        if self.submission_name and self.submission_name not in self._grades:
            # This is the first time grading the submission
            self.add_submission_entry()

    def load_grades(self):
        """Returns a dictionary representation of the TA's grades thus far"""
        if not utils.file_exists(self.grades_file):
            # The TA hasn't started grading this hw yet
            return dict()

        with open(self.grades_file, "r") as f:
            return json.load(f)

    def add_submission_entry(self):
        """Create a new entry for student/team with null fields"""
        self._grades[self.submission_name] = dict()
        self._grades[self.submission_name]["is_late"] = False
        rubric_scores = dict()
        for table_key in sorted(self.rubric.keys()):
            for section in sorted(self.rubric[table_key].keys()):
                # None means that it hasn't been graded yet
                rubric_scores[section] = {"points": None, "comments": None}
        self._grades[self.submission_name]["scores"] = rubric_scores

    def __getitem__(self, rubric_item):
        """Wrapper around self._grades for convenience"""
        return self._grades[self.submission_name]["scores"][rubric_item]

    def synchronize(self):
        """Write out the grades dictionary to the filesystem"""
        with open(self.grades_file, "w") as f:
            # Indent for pretty printing :^)
            json.dump(self._grades, f, indent=4)

    def is_graded(self, section, name=None):
        """Checks if an item has been graded yet"""
        if not name:
            name = self.submission_name
        # TODO: yikes, 4 dictionary accesses xD. is there a better way?
        return (self._grades[name]["scores"][section]["points"]
                is not None)

    def is_late(self, name=None):
        """Getter for is_late"""
        if not name:
            name = self.submission_name
        return self._grades[name]["is_late"]

    def set_late(self, opt):
        """Setter for is_late"""
        self._grades[self.submission_name]["is_late"] = opt

    def dump_grades(self, submission_name, rubric_code):
        all_pts = 0
        graded_submissions = 0

        if submission_name:
            self.print_submission_grades(submission_name, rubric_code)
        else:
            for name in self._grades:
                is_graded, total_pts = self.print_submission_grades(name,
                                                                    rubric_code)
                all_pts += total_pts
                if is_graded:
                    graded_submissions += 1


            avg = all_pts / graded_submissions if graded_submissions else 0
            print(f"\nAverage across {graded_submissions} "
                  f"graded submission(s): {avg}")


    def print_submission_grades(self, name=None, rubric_code=None):
        """Prints (uni, pts, comments) in tsv format"""
        if not name:
            name = self.submission_name

        if not rubric_code:
           rubric_code = "ALL"

        total_pts = 0
        all_comments = []
        graded = False
        submission_scores = self._grades[name]["scores"]

        for item in submission_scores.keys():
            if not self.is_graded(item, name):
                continue

            if rubric_code != "ALL" and not item.startswith(rubric_code):
                continue

            graded = True
            total_pts += submission_scores[item]["points"]
            item_comments = submission_scores[item]["comments"]
            if item_comments:
                all_comments.append(item_comments)

        if rubric_code == "ALL" and self.is_late(name):
            all_comments.insert(0, "(LATE)")
        concatted_comments = "; ".join(all_comments)

        if rubric_code == "ALL" and self.is_late(name):
            total_pts = max(total_pts * (1 - LATE_PENALTY), 0)

        if graded:
            print(f"{name}\t{total_pts}\t{concatted_comments}")
        else:
            print(f"{name}\tn/a\tn/a")

        return graded, total_pts
