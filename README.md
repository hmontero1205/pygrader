[![pylint](https://github.com/cs4118/new_grading_scripts/workflows/pylint/badge.svg)](https://github.com/cs4118/new_grading_scripts/actions?query=workflow%3Apylint)

# pygrader
Grading infrastructure for Jae's COMS 4118, primarily written in Python.

# Guide
## Dependency Installation
Run the following:
```
./install_dependencies.sh
```

This will make sure you have all the necessary apt packages and python3 libraries installed.
## Pre-grading Setup
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

Note that we don't store numeric values for subitem grades here. By simply storing `true`/`false`, we are able to rescale grades without having to regrade. All you'd have to do to rescale an assignment is to update the `hwN/hwN_rubric.json` and then re-dump grades to make sure you have the updated numbers.

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
  submitter             the name of student/group to grade

optional arguments:
  -h, --help            show this help message and exit
  -c [CODE], --code [CODE]
                        rubric item (e.g. A, B4) to grade; defaults to all
  -g, --grade-only      grade without running any tests
  -t, --test-only       run tests without grading
  -r, --regrade         do not skip previously graded items
  -d, --dump-grades     dump grades for this homework -- all if no submitter
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

# Repo Overview
This section provides a high-level explanation of the design for this grader. For specifics, we have tried to add comments in the code where needed. Here's some terminology you'll see throughout the repo:
- Rubric Table: Our rubrics are organized by tables (roughly mapping to each part of an assignment). Tables are denoted by 1 letter (A-Z).
- Rubric Item: This is the granularity at which we run tests. A rubric item is denoted by a its table letter and a number (e.g. A1, C3). A rubric item may be composed of one or more subitems.
- Rubric Subitem: This is the granularity at which we award points. For each test (rubric item), we usually have a few subitems. These are denoted by its corresponding item code followed by a number (e.g. A1.1, C3.2).
- Grades: Super overloaded in this repo xD. Here, it means the actual grading record for a given submission (how many points were awarded and comments left by the TA).
## Rubrics and HW Classes
There are a few building blocks that make up the homework representation in this grader.
### Rubric Files
HW assignments have a corresponding rubric found in `hwN/hwN_rubric.json` that look something like this:
```
{
    "B": {
        "B1": {
            "name": "B1",
            "points_per_subitem": [
                1,
                2,
                3
            ],
            "desc_per_subitem": [
                "foo",
                "bar",
                "foobar"
            ]
        },
        "B2": {
            ...
        }
    },

    "C": {
      ...
    }
}
```
We see that each table code is mapped to a mapping from rubric item code to rubric item information. For each rubric item, we have its `name` , `points_per_subitem`, and `desc_per_subitem`. Again, we have test functions per rubric item (B1), but we grade per subitem (B1.1, B1.2, B1.3).


### HW Base Class (`common/hw_base.py`).
This is the base class that concrete hw instances will extend when instantiated. This class is mainly responsible for parsing the rubric JSON file and connecting RubricItems with their corresponding `grade_ItemCode()` function. These functions are defined by the concrete hw class. This class also provides some default/common functionality.
### Concrete HW Classes (`hwN/hwN.py`)
These classes extend the HW base class and actually implement the tester functions for each rubric item. This is where the core grading logic for each assignment lives.
## `grade.py` (the Grader)
The main entrypoint to the grading infrastructure. Here, the concrete hw class is instantiated and the grades JSON file is parsed. Then, as defined by the Grader command-line flags, rubric items' tester functions are called and the TA is prompted for points/comments (after each tester function). Grades are synchronized to the filesystem after each rubric item is graded. The Grader alternatively offers an easy way to pretty-print grades (via dump mode).
## `common/grades.py`
The Grades object exposes a minimal interface for the Grader to access/update a submission's grading progress. If the Grader is being run in dump mode, the Grades object is used to traverse through `grades.json` and pretty-print all the submissions' grades.
## `common/utils.py`
This library offers a bunch of functions that are often used in grading logic. We've tried to simplify common operations (compilation, value comparison, file inspection, etc.) into easy-to-use functions.
## `common/submissions.py`
This library contains logic related to our git/GitHub workflow. Our late submission detector and some tag/branch logic is stored here.
## `common/printing.py`
This library essentially wraps `print()` with colors. This is meant to be a little more flexible than some pylibrary like `termcolor`, although it might be worth looking into that.

# Acknowledgement
- Written by Dave and Hans in Summer 2020
