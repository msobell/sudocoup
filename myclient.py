#! /usr/bin/env python
"""
Usage: %s

Solves the Sudokill problem (http://cs.nyu.edu/courses/fall10/G22.2965-001/)
"""
import os
import sys
import time
import math
start_time = time.time()


def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def printTime():
    print "Time:\t\t" + repr(round(time.time() - start_time,4))
        
if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

   printTime()
