pygrader Demo
=============
This fake assignment is meant to demonstrate how to use the pygrader framework
to grade your assignments and to get a feel for the grading flow from start to
finish.

Note that in this assignment, student submissions take the form of git patches
conveniently placed in `fake-submissions/`. In reality, the pygrader framework
is meant to support several submission formats (e.g. tarballs from Courseworks,
Github repos).

Create a Rubric
---------------
Before beginning to grade, you need to establish a rubric for the assignment.
The motivation here is that a rubric will result in more consistent, organized,
and transparent grading.

In the pygrader framework, we specify rubrics in JSON format. See
[here](../README.md#repo-overview) for more discussion on that format. The demo
rubric in `rubric.json` is loosely based on a rubric from COMS 4118. Here's a
breakdown of each section:

    "late_penalty": 0.2,

This sets the late penalty for the assignment to 20%, s.t. 20% of however many
points a submission earns are deducted from the final grade.

    "A": {
        "A1": {
            "name": "A1",
            "points_per_subitem": [ -5 ],
            "desc_per_subitem": [ "Tracked compilation artifacts" ]
        },

        "A2": {
            "name": "A2",
            "points_per_subitem": [ -5 ],
            "desc_per_subitem": [ "Less than 5 meaningful git commits" ]
        }
    },

Table A is usually meant for deductive items – flat penalties applied to
submissions for things like minor spec violations. Here, I specified two
disjoint rubric items: A1 and A2. They are separate penalties and a submission
could in theory have both applied. The minimum score for a submission is
calculated by `min(raw_score, 0)`.

    "B": {
        "B1": {
            "name": "B1",
            "points_per_subitem": [
                5,
                5,
                5
            ],
            "desc_per_subitem": [ 
                "Correct WQ1 answer",
                "Correct WQ2 answer",
                "Correct WQ3 answer"
            ]
        }
    },

After the deductive table A, we usually have one table per part of the
assignment. In this demo assignment, we have two "parts": a written part and a
coding part. Table B is meant for the written part of the assignment. With three
written questions, we divide B1 into three subitems (B1.1-3).

    "C": {
        "C1": {
            "name": "C1",
            "points_per_subitem": [
                5,
                5
            ],
            "desc_per_subitem": [ 
                "Correct Makefile dependencies",
                "Attempts to complete swap() implementation"
            ]
        },

        "C2": {
            "name": "C2",
            "points_per_subitem": [
                5,
                10
            ],
            "desc_per_subitem": [ 
                "Make builds without warnings",
                "Swaps the two numbers"
            ]
        }
    }

Part 2 of this mock assignment is the coding portion. In table C, we have two
rubric items: C1 (static analysis) and C2 (dynamic analysis). Each item is
further divided into subitems, one for each item of that analysis.

This assignment is thus out of 40pts.

Implement Grading Logic
-----------------------
Once the rubric is done, the next step is to code up the actual grading logic.
Every assignment has a `grader.py` which contains this logic. We grade on the
granularity of rubric items so I've implemented the functions
`grade_{A1, A2, B1, C1, C2}()`. This was straightforward to do because most of
the logic I needed was already implemented in `common/utils.py` and
`common/submissions.py`.

I want to make a point of the written portion of this demo assignment. Having a
solid grading infrastructure is a big motivating factor for moving away from
free-form assignments. Giving assignments more structure makes grading (and
automation) a lot easier. Here, we assume that students are given a "skeleton"
repo to start with. We give the students a text file with sections to put their
answers into instead of letting them format it however they'd like. This let's
us take advantage of the `extract_between()` utility to quickly pick out answers
so graders don't have to comb through text files manually. This principle also
extends to code. In COMS 4118, we often gave students code that prints results
and had them instead implement the logic to produce those results. This made it
very easy for us to parse through output and automate comparisons.

Preparing to Grade
------------------
See [Dependency Installation](../README.md#dependency-installation) to make sure
you have all the necessary packages installed. Next, run the following command
to prepare the grading workspace:

    ~/pygrader $ ./hw_setup.py demo

See [Pre-grading Setup](../README.md##pre-grading-setup) on more discussion on
what the grading workspace looks like. You'll be prompted to enter the
assignment's soft deadline – that is, the latest time that submissions are
considered on-time. This is used to detect late submissions and apply a late
penalty. Enter some date after `01/05/21` to avoid all submissions being marked
late. Feel free to change this to an earlier time to see how late submissions
are treated.

Grade!
------
I've made three mock submissions for you to play with: `student{1,2,3}`. Check
out the [Tips](../README.md##tips) on different ways of running the
grader. Here's a few common ways:

    ~/pygrader $ ./grade.py demo student1

The default mode of operation – this will grade from the beginning to the end of
the rubric, skipping any items you've already graded.

    ~/pygrader $ ./grade.py -r demo student1 --code=A

Regrade (`-r`) this submission on rubric table A (`--code=A`). This forces the
grader to rerun tests and reprompt you for grades/comments. It will also show
you what you previously entered.


After running the tests for a rubric item, you'll be prompted with these action
choices:

    Run test again (a)
    Open shell & run again (s)
    Continue (enter)
    Enter an action [a|s]:

This is meant to give the grader more flexibility. You can run the test again
(a) if you want to verify output or see if there is non-deterministic behavior.
You can also drop into a shell (s) to make a hotfix or inspect the submission
contents yourself and then rerun the test. The grader will not reset local
changes when you rerun a particular test which means a hotfix can affect the
result!

Getting Scores
--------------
In COMS 4118, we organize our grades in Google Sheets before pushing them to
Courseworks using
[canvas-wrangler](https://github.com/cs3157/boatswain#canvas-wrangler), a script
part of a library of utilities for managing Courseworks and Github workflows. To
get them onto the Google spreadsheet, pygrader can dump (`-d`) grades for the
entire assignment in tsv format:

    ~/pygrader $ ./grade.py -d demo
    student1	40
    student2	30	(C2.2) Numbers are unswapped
    student3	35	(C2.1) Implicit declaration warning

    Average across 3 graded submission(s): 35.0


You can copy the first three rows and paste it into Google Sheets using the
"paste values only" option (cmd+shift+v on my Mac). This will split each row
into three columns.

There are a couple of modes that you can dump in, too:

    ~/pygrader $ ./grade.py -d demo student2  # Dump a student's grade
    student2	30	(C2.2) Numbers are unswapped

    ~/pygrader $ ./grade.py -d demo --code=C2  # Dump grades for a rubric item
    student1	15
    student2	5	(C2.2) Numbers are unswapped
    student3	10	(C2.1) Implicit declaration warning

    Average across 3 graded submission(s): 10.0
