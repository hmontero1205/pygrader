"""submissions.py: Utils that help dealing with submissions"""

from datetime import datetime, timedelta
from pytz import timezone
import common.printing as printing

def check_late(deadline_path, iso_timestamp):
    """Checks if iso_timestamp is past the deadline

    Arguments:
        deadline_path: Location of the recorded assignment deadline
            (e.g. ~/.grade/hw1/.deadline.txt)
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
