"""submissions.py: Utils that help dealing with submissions"""

import os
from typing import Callable
from datetime import datetime, timedelta
from pytz import timezone
import git
import common.printing as printing

HW_ORG = "cs4118-hw"

def check_late(deadline_path, iso_timestamp):
    """Checks if iso_timestamp is past the deadline

    Arguments:
        deadline_path: Location of the recorded assignment deadline
            (e.g. ~/.grade/hw1/deadline.txt)
        iso_timestamp: The ISO timestamp to compare against deadline
            (e.g. git log -n 1 --format='%aI')
    """
    submission = datetime.fromisoformat(iso_timestamp)

    with open(deadline_path, "r") as d:
        deadline_string = d.readline()

    raw_deadline = datetime.strptime(deadline_string, "%m/%d/%y %I:%M %p")

    nyc_tz = timezone("America/New_York")
    deadline = nyc_tz.localize(raw_deadline.replace(second=59, tzinfo=None))

    if submission <= deadline:
        printing.print_green("[ SUBMISSION ON TIME ]")
        return False

    # Let's calculaute the difference
    diff = submission - deadline

    # Wow this is like a page table walk xD
    days, hrs_r = divmod(diff, timedelta(days=1))
    hrs, mins_r = divmod(hrs_r, timedelta(hours=1))
    mins, secs_r = divmod(mins_r, timedelta(minutes=1))
    secs, _ = divmod(secs_r, timedelta(seconds=1))

    printing.print_red(f"[SUBMISSION LATE]: Submitted {days} days, "
                       f"{hrs} hrs, {mins} mins, "
                       f"and {secs} secs late")
    return True

def checkout_to_team_master(
        repo: git.Repo, hw_name: str, team: str) -> bool:
    repo.git.checkout("master")  # Make sure we're already on master (skel).
    try:
        repo.git.remote("rm", team)
    except git.GitError:
        # We haven't added this team as a remote yet.
        pass

    # Remove all tags just in case.
    for tag_ref in repo.tags:
        repo.delete_tag(tag_ref)

    repo_name = f"{hw_name}-{team}"
    repo.create_remote(team, f"git@github.com:{HW_ORG}/{repo_name}.git")

    repo.git.fetch(team, "--tags")
    repo.git.fetch(team, "master")

    # Let's checkout to the team's master branch to start out.
    try:
        repo.git.branch('-D', team)  # Just in case it exists already.
    except git.GitError:
        # This branch doesn't exist.
        pass

    repo.git.checkout("-b", team, f"{team}/master")

    return True

def tag(tag_name: str) -> Callable:  # pylint: disable=unused-argument
    """Decorator function that checks out to tag_name before the test.

    If tag_name is 'master', we checkout to the submission's master branch,
    which has been pulled down and named after the submission
    (see checkout_to_team_master()). If the checkout fails, we open a shell
    for the grader to resolve the issue.
    """

    def function_wrapper(test_func):
        def checkout_to_tag_then_test(hw_instance):
            nonlocal tag_name
            current_tag = hw_instance.repo.git.describe()
            if tag_name != current_tag:
                # Clean first
                hw_instance.repo.git.checkout("--", "*")
                try:
                    if tag_name == "master":
                        tag_name = f"{hw_instance.submitter}"
                        hw_instance.repo.git.checkout(tag_name)
                        printing.print_green(
                                f"[ Checked out to {tag_name}/master ]\n")
                    else:
                        hw_instance.repo.git.checkout(tag_name)
                        printing.print_green(f"[ Checked out to {tag_name} ]\n")
                except git.GitError:
                    printing.print_red(f"[ Couldn't checkout to {tag_name} ]")
                    printing.print_cyan(
                            "[ Opening shell -- ^D/exit when resolved ]")
                    os.system("bash")
            else:
                # No cleaning in case the TA made necessary changes to the
                # submission that we don't want to throw away
                printing.print_green(f"[ Checked out to {tag_name} ]\n")

            hw_instance.repo.git.clean("-f", "-d")
            return test_func(hw_instance)

        return checkout_to_tag_then_test

    return function_wrapper
