"""submissions.py: Utils that help dealing with submissions"""

import pickle
from datetime import datetime, timedelta
import common.printing as printing

def check_late(deadline_path, iso_timestamp):
    """Checks if iso_timestamp is past the deadline

    Arguments:
        deadline_path: Location of the serialized datetime object
            representing the deadline (e.g. ~/.grade/hw1/.deadline)
        iso_timestamp: The ISO timestamp to compare against deadline
            (e.g. git log -n 1 --format='%aI')
    """
    submission = datetime.fromisoformat(iso_timestamp)
    with open(deadline_path, "rb") as d:
        deadline = pickle.load(d)

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
