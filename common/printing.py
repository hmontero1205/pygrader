"""
TODO:
    1. Make color sequences variables
    2. Offer functions like wrapRed(string)
    3. All pretty printing should be defined here (intro/outro...)
"""


def prRed(skk): print("\033[91m{}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[95m{}\033[00m" .format(skk))
def prPurple(skk): print("\033[35m{}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m{}\033[00m" .format(skk))
def prIntro(team, hw, part):
    prCyan("="*85)
    print("\033[96m{}\033[00m \033[95m{}\033[00m \033[96m {}\033[00m \033[95m{}\033[96m  {}\033[00m \033[95m{}\033[00m".format("Team:", team, "HW:", hw, "Rubric Table:", part))
    prCyan("="*85)
