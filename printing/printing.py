

class Printing():
    
    def __init__(self):
        self.name = "printig color"

    def prRed(self, skk): print("\033[91m{}\033[00m" .format(skk))
    def prGreen(self, skk): print("\033[92m{}\033[00m" .format(skk))
    def prYellow(self, skk): print("\033[93m{}\033[00m" .format(skk))
    def prLightPurple(self, skk): print("\033[94m{}\033[00m" .format(skk))
    def prPurple(self, skk): print("\033[95m{}\033[00m" .format(skk))
    def prCyan(self, skk): print("\033[96m{}\033[00m" .format(skk))
    def prLightGray(self, skk): print("\033[97m{}\033[00m" .format(skk))
    def prBlack(self, skk): print("\033[98m{}\033[00m" .format(skk))
    def prIntro(self, team, part): print("\033[96m{}\033[00m \033[95m {}\033[00m \033[96m {}\033[00m \033[95m {}\033[00m".format(" Grading Team:", team, "part:", part))

