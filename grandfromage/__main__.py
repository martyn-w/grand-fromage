#print "IN MAIN.PY"

from __init__ import *
import argparse


def main():
    parser = argparse.ArgumentParser(description="Grand Fromage")
    parser.add_argument('command')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    #print parser
    args = parser.parse_args()
    print args

if __name__ == '__main__':
    main()

#print Tracker

