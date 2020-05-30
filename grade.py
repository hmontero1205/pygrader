import os
import sys

sys.path.insert(0, "printing")
from printing import Printing as p

def main():
    p.prRed("this is an error")
    #prGreen("this is good")
    #prYellow("this is yellow")
    #prLightPurple("not sure")
    #prCyan("use for dividers")

    #
    #prCyan("="*75)
    #prIntro("d++", "5")
    #prCyan("-"*75)

if __name__ == '__main__':
    main()
