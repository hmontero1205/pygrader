#!/usr/bin/python3
import os
import sys
import argparse

sys.path.insert(0, "printing")
from printing import Printing as p

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="path to the homework to grade")
    parser.add_argument("part", type=int, help="part of the homework to grade")
    parser.add_argument("student", type=str, help="the name of student/group to grade")

    args = parser.parse_args()

    print(args.hw, args.part, args.student)

class Grader():

    def __init__(self, hw, part, student):

        self.hw = hw
        self.part = part 
        self.student = student


    def cmd(self, cmd):
        pass

    def setup(self, hw, student):
        pass

    def cleanup(self):
        pass

    def run_test(part, student):
        pass


if __name__ == '__main__':
    main()
