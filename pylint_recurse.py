#! /usr/bin/env python
"""
this module runs pylint on all python scripts found in a directory tree
"""

import os
import re
import sys

try:
    BASE_DIRECTORY = sys.argv[1]
except IndexError:
    print("No directory specified, defaulting to current working directory")
    BASE_DIRECTORY = os.getcwd()

def check(module, results):
    """ apply pylint to the file specified if it is a *.py file """

    if module[-3:] == ".py":

        print("CHECKING {}".format(module))
        pout = os.popen('pylint {}'.format(module), 'r')
        for line in pout:
            if  re.match("E....:.", line):
                print(line)
            if "Your code has been rated at" in line:
                print(line)
                score = re.findall(r"[1]?\d.\d\d", line)[0]
                results['total'] += float(score)
                results['count'] += 1

def main():
    """ main procedure """

    results = {'total':0.0, 'count':0}

    print("Looking for *.py scripts in subdirectories of {}".format(BASE_DIRECTORY))
    print("=" * 100)

    for root, dummy_dirs, files in os.walk(BASE_DIRECTORY):
        for name in files:
            filepath = os.path.join(root, name)
            check(filepath, results)

    print("=" * 100)
    print("{} modules found".format(results['count']))
    print("AVERAGE SCORE = {:.02f}".format((results['total'] / results['count'])))

if __name__ == "__main__":
    main()
