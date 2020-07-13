#!/usr/bin/python3
import os
import sys
import argparse
import subprocess

sys.path.insert(0, "printing")
from printing import Printing
p = Printing()
sys.path.insert(0, "hw1")
from hw1 import HW1

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("hw", type=str, help="path to the homework to grade")
    parser.add_argument("student", type=str, help="the name of student/group to grade")
    parser.add_argument("table", type=str, help="table to grade")

    args = parser.parse_args()

    tester = Grader(args.hw, args.student, args.table)

    tester.run_test(args.table, args.student)

class Grader():

    def __init__(self, hw, student, table):

        self.hw = hw
        self.table = table
        self.student = student

        hw_class = HW1("./hw1", self.student)
        self.rubric = hw_class.rubric

    def print_intro(self, name, part):
        p.prCyan("="*85)
        p.prIntro(name, part)
        p.prCyan("="*85)

    def run_test(self, table_key, student):

        self.print_intro(student, table_key)
        table_keys = [*self.rubric.keys()]
        
        if table_key not in table_keys:
            return 0

        table = self.rubric[table_key]

        for section in table:
            table[section].test_item()

if __name__ == '__main__':
    main()
