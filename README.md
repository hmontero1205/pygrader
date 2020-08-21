[![pylint](https://github.com/cs4118/new_grading_scripts/workflows/pylint/badge.svg)](https://github.com/cs4118/new_grading_scripts/actions?query=workflow%3Apylint)

# pygrader
Grading infrastructure for Jae's COMS 4118, primarily written in Python.

# Guide

## Setting up the env

- Obtain `hw1.tgz` as follows:  Download the zipped submissions file from
  Courseworks, unzip, and place all tarballs in a directory called `hw1`.
  Then, make a tarball out of that. TODO: make this process better.

- Run `./hw_setup.py hw1 -f {path to hw1.tgz}`

This will create a dir called `.grade/` in your `HOME` dir. In addition to
serving as the workspace for grading submissions, grades and the hw deadline
will also be stored here. The directory will look like this (for hw1):
```
~
\_ .grade/
    \_ hw1/
       \_ grades.json
       \_ deadline.txt
       \_ uni1/
          \_ uni1.tgz
       \_ uni2/
          \_ uni2.tgz
       |
       |
       \_ uniN/
          \_ uniN.tgz
```

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

# Acknowledgement
- Written by Dave and Hans in Summer 2020