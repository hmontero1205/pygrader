[![pylint](https://github.com/cs4118/new_grading_scripts/workflows/pylint/badge.svg)](https://github.com/cs4118/new_grading_scripts/actions?query=workflow%3Apylint)

# pygrader
Grading infrastructure for Jae's COMS 4118, primarily written in Python.

# Guide

## Setup
Generally speaking, you run the following before beginning to grade an assignment: 
```
./hw_setup.py hwN
```

This will create a dir called `.grade/` in your `HOME` directory. In addition to
serving as the workspace for grading submissions, grades (awarded points & comments) and the hw deadline will  be stored here. The directory will look something like this:
```
~
\_ .grade/
    \_ hwN/
       \_ grades.json
       \_ deadline.txt
       \_ hwN
```

For GitHub-based assignments, the `hwN` subdirectory will be a clone of the skeleton code and is used for pulling in submissions tags. For Canvas-based assignments, there will be a directory for each student (see [hw1/README.md](hw1/README.md) for more details).

### grades.json
This is a JSON representation of your grading progress for a given hw. It takes the following form:
```
{
  "name1": {
    "is_late": false,
    "scores": {
      "A1.1": {
        "award": false,
        "comments": "test didn't pass"
      },
      "A1.2": {
        "award": null,
        "comments": null
      }
    }
  },
  "name2": {
    ...
  }
}

```
Each submission you grade will be recorded here. This file is updated as you grade. You can also manually update this file. Here's a breakdown of the fields:
- `is_late` is a boolean indicating whether or not any part of the submission was submitted after the deadline (stored in `deadline.txt`). This is used to apply the late penalty when you run `./grade --dump hwN`. This field is updated by the grader if it finds that the submission is late.
- `scores` maps a rubric subitem to its grading result. The `award` and `comments` start off as `null`, which means you haven't graded that subitem yet. When dumping grades, subitems that have `award = null` are not included.
    - `award` is a boolean indicating whether or not the submission passed this test.
    - `comments` is a text field for leaving comments for that item. When dumping grades, all comments (empty or not) are prepended with the subitem code. (e.g. (A1.1) test didn't pass).

### deadline.txt
This is a plain-text file that contains the deadline for the assignment. This date is written when running `hw_setup.py` but can also be manually updated later. For example:
```
02/02/20 11:59 PM
```
The grader will compare this date with the timestamp on the latest commit of the submission (or tag for Github-based assignments). The `is_late` field is set to `true` if the submission is late. The late penalty (defined in `common/submissions.py`) is then applied when dumping grades.

## Running the grading script
```
usage: grade.py [-h] [-c [CODE]] [-g | -t] [-r | -d] hw [student]

OS HW Grading Framework

positional arguments:
  hw                    homework # to grade
  student               the name of student/group to grade

optional arguments:
  -h, --help            show this help message and exit
  -c [CODE], --code [CODE]
                        rubric item (e.g. A, B4) to grade; defaults to all
  -g, --grade-only      grade without running any tests
  -t, --test-only       run tests without grading
  -r, --regrade         do not skip previously graded items
  -d, --dump-grades     dump grades for this homework -- all if no student
                        specified
```

# Tips
- Simply running `./grade.py <hw> <student>` will run through the entire rubric
  and skip any previously graded items.
- If a submission crashes the grader/VM, restart and run
  `./grade.py --grade-only <hw> <student> <item that crashed>`. This will
  allow you to assign points/comments to that rubric item without rerunning the
  problematic tests.
- There are a few modes for dumping grades. Below are some examples. The first
  mode can be used for getting a tsv-string to copy-paste into a spreadsheet.
  The other modes can be used for reference (e.g. average grade for particular
  rubric item).
    - `./grade.py --dump <hw>`: all grades with late penalty applied.
    - `./grade.py --dump <hw> --code=<code>`: all grades for rubric item `code`
    - `./grade.py --dump <hw> <student> --code=<code>`: student's grades for
      rubric item `code`.

# Repo Overview (TODO)
This section provides a high-level explanation of the design for this grader. For specifics, we have tried to add comments in the code where needed. 
## Rubrics and HW Classes
## `grade.py`
## `common/utils.py`
## `submissions.py`
## `printing.py`

# Acknowledgement
- Written by Dave and Hans in Summer 2020