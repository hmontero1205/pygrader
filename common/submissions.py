"""submissions.py: Utils that help dealing with submissions"""

import os
from typing import Callable
from datetime import datetime, timedelta
from pytz import timezone
import git
import common.printing as printing

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

    if not deadline_string:
        return False

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

def checkout_to_team_branch(
        repo: git.Repo, team_repo_id: str,
        team: str, branch_name: str = "master") -> bool:
    repo.git.checkout(branch_name)  # Make sure we're on the branch (skel).
    try:
        repo.git.remote("rm", team)
    except git.GitError:
        # We haven't added this team as a remote yet.
        pass

    # Remove all tags just in case.
    for tag_ref in repo.tags:
        repo.delete_tag(tag_ref)

    repo.create_remote(team, f"git@github.com:{team_repo_id}.git")

    repo.git.fetch(team, "--tags")
    repo.git.fetch(team, "master")

    # Let's checkout to the team's branch.
    team_branch = f"{team}-{branch_name}"
    try:
        repo.git.branch('-D', team_branch)  # Just in case it exists already.
    except git.GitError:
        # This branch doesn't exist.
        pass

    repo.git.checkout("-b", team_branch, f"{team}/{branch_name}")

    return True

def tag(tag_name: str) -> Callable:  # pylint: disable=unused-argument
    """Decorator function that checks out to tag_name before the test.

    If tag_name is 'master', we checkout to the submission's master branch,
    which has been pulled down and named after the submission
    (see checkout_to_team_branch()). If the checkout fails, we open a shell
    for the grader to resolve the issue.
    """

    def function_wrapper(test_func):
        def checkout_to_tag_then_test(hw_instance):
            nonlocal tag_name
            current_tag = hw_instance.repo.git.describe("--always")
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

def to_branch(hw_instance, branch_name: str):
    current_branch = hw_instance.repo.git.rev_parse("--abbrev-ref", "HEAD")
    target_branch = f"{hw_instance.submitter}-{branch_name}"
    if current_branch != target_branch:
        # Clean first
        hw_instance.repo.git.checkout("--", "*")
        try:
            hw_instance.repo.git.checkout(target_branch)
            printing.print_green(f"[ Checked out to {branch_name} ]\n")
        except git.GitError:
            printing.print_red(f"[ Couldn't checkout to {branch_name} ]")
            printing.print_cyan(
                    "[ Opening shell -- ^D/exit when resolved ]")
            os.system("bash")
    else:
        # No cleaning in case the TA made necessary changes to the
        # submission that we don't want to throw away
        printing.print_green(f"[ Checked out to {branch_name} ]\n")

    hw_instance.repo.git.clean("-f", "-d")

def branch(branch_name: str) -> Callable:  # pylint: disable=unused-argument
    """Decorator function that checks out submitter-branch_name before the test.

    This is assumed to be in reference to a submission branch, which follows the
    naming convention 'submitter-branch_name' (see checkout_to_team_branch()).
    If the checkout fails, we open a shell for the grader to resolve the issue.
    """

    def function_wrapper(test_func):
        def checkout_to_branch_then_test(hw_instance):
            nonlocal branch_name
            to_branch(hw_instance, branch_name)
            return test_func(hw_instance)

        return checkout_to_branch_then_test

    return function_wrapper

def apply_patch(repo: git.Repo, patch_path: str) -> bool:
    """Applies a patch to the current dir (assumed to be a repo)"""
    try:
        repo.git.am(patch_path)
    except git.GitError as e:
        print(e)
        return False

    return True
