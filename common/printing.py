"""printing.py: Colored output helpers"""

def print_red(s):
    """Prints s in red"""
    print("\033[91m{}\033[00m" .format(s))

def print_green(s):
    """Prints s in green"""
    print("\033[92m{}\033[00m" .format(s))

def print_yellow(s):
    """Prints s in yellow"""
    print("\033[93m{}\033[00m" .format(s))

def print_light_purple(s):
    """Prints s in light purple"""
    print("\033[95m{}\033[00m" .format(s))

def print_purple(s):
    """Prints s in purple"""
    print("\033[35m{}\033[00m" .format(s))

def print_cyan(s):
    """Prints s in cyan"""
    print("\033[96m{}\033[00m" .format(s))

def print_light_gray(s):
    """Prints s in light gray"""
    print("\033[97m{}\033[00m" .format(s))

def print_black(s):
    """Prints s in black"""
    print("\033[98m{}\033[00m" .format(s))

def print_intro(team, hw, part):
    """Prints the intro banner for the grading script"""
    print_cyan("="*85)
    print("\033[96m{}\033[00m \033[95m{}\033[00m \033[96m {}\033[00m \033[95m{}"
          "\033[96m  {}\033[00m \033[95m{}\033[00m".format("Team:", team,
                                                           "HW:", hw,
                                                           "Rubric Table:",
                                                           part))
    print_cyan("="*85)
