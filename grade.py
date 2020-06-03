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




if __name__ == '__main__':
    main()
