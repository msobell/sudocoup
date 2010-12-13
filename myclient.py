#! /usr/bin/env python
"""
Usage: %s <name>

Solves the Sudokill problem (http://cs.nyu.edu/courses/fall10/G22.2965-001/)
"""
import os
import sys
import time
import math
HOST = localhost
PORT = 44444
prev_move = None
start_time = time.time()

class BoardState:
    def __init__(self, line):
        self.inp = line.split('|')[1:]
        self.board = None

        # ADD|0 0 0 1 3 4 0 8 9|3 0 0 0 0 5 0 0 0| ... |0 2 0 0 1 0 0 6 0
        # make a 2D array
        for i in range(len(self.inp)):
            row = self.inp[i].split(' ')
            self.board.append([])
            for j in range(len(row)):
                self.board[i].append(int(row[j]))

    def printBoard(self):
        for row in self.board:
            print row

    def same_row(self,i,j): return (i/9 == j/9)
    def same_col(self,i,j): return (i-j) % 9 == 0
    def same_block(self,i,j): return (i/27 == j/27 and i%9/3 == j%9/3)

    def find_moves(self,prev_row,prev_col):
        moves = []
        x = prev_row * 9 + prev_col
        y = prev_row * 9 + prev_col
        x -= x % 9 # start at the beginning of the row
        y %= 9
        first = True
        # do it for the row
        while not first and (x+1 % 9) != 0: # try each number until the end of the row
            first = False
            if self.board[x] == 0: # spot isn't already taken
                excluded_numbers = set()
                for y in range(81):
                    if same_row(x,y) or same_col(x,y) or same_block(x,y):
                        excluded_numbers.add(self.board[y])

                for n in range(0,9):
                    if n not in excluded_numbers:
                        moves.append([x,n])
            x += 1

        # and for the column
        first = True
        while not first and y <= 81: # try each number until the end of the row
            first = False
            if self.board[y] == 0: # spot isn't already taken
                excluded_numbers = set()
                for x in range(81):
                    if same_row(x,y) or same_col(x,y) or same_block(x,y):
                        excluded_numbers.add(self.board[x])

                for n in range(0,9):
                    if n not in excluded_numbers:
                        moves.append([y,n])
            y += 9

        return moves
                        

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def printTime():
    print "Time:\t\t" + repr(round(time.time() - start_time,4))
        
def make_move( line ):
    b = BoardState( line )
    print "Current board:"
    b.printBoard()
    
    try:
        prev_row = int(prev_move.split(' ')[0])
        prev_col = int(prev_move.split(' ')[1])
    except:
        print "no prev move!"

    b.find_moves(prev_row,prev_col)

    
## From:
## Charles J. Scheffold
## cjs285@nyu.edu
def SReadLine (conn):
    data = ""
    while True:
        c = conn.recv(1)
        if not c:
            time.sleep(1)
            break
        data = data + c
        if c == "\n" or c == "\r":
            print data
            break
    return data

if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    # Open connection to evasion server
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))
    print "Connected to", HOST, "port", PORT

    join = repr(sys.argv[1]) + "\n"
    s.send(join)

    while True:
        # Read status line
        data = SReadLine (s)
        line = string.strip (data)

        print line

        if len(line.split(' ')) == 4:
            prev_move = line.split(' ')
        if "ADD" in line:
            make_move( line )

    printTime()
