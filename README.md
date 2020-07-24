[![pylint](https://github.com/cs4118/new_grading_scripts/workflows/pylint/badge.svg)](https://github.com/cs4118/new_grading_scripts/actions?query=workflow%3Apylint)
# Guide

## Setting up the env

- Obtain `hw1.tgz` as follows:  Download the zipped submissions file from
  Courseworks, unzip, and place all tarballs in a directory called `hw1`.
  Then, make a tarball out of that. TODO: make this process better.

- Run `./hw_setup.py hw1 -f {path to hw1.tgz}`

This will create a dir called `.grade/` in your `HOME` dir. In addition to
serving as the workspace for grading submissions, grades and the hw deadline
will also be stored here. The directory will look like this:
```
~
\_ .grade/
    \_ hw1/
       \_ .grades.json
       \_ .deadline
       \_ uni1/
       \_ uni2/
       |
       |
       \_ uni3/
```

## Running the grading script
```
Usage: grade.py [-h]
              [--amend | --continue | --grade-only | --regrade | --test-only]
              hw student table

Entry point to grade OS HWs

positional arguments:
  hw            homework # to grade
  student       the name of student/group to grade
  table         table to grade

optional arguments:
  -h, --help    show this help message and exit
  --amend       Amend comment without rerunning test for that item
  --continue    Continue from last graded item
  --grade-only  Grade without running any tests
  --regrade     Regrade an item
  --test-only   Run tests without grading
```

NOTES
- amend hasn't been implemented
- regrade might be redundant
