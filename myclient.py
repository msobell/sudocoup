#! /usr/bin/env python
"""
Usage: %s <name>

Solves the Sudokill problem (http://cs.nyu.edu/courses/fall10/G22.2965-001/)
"""
import os
import sys
import time
import math
import socket
import string
import random
HOST = "localhost"
PORT = 44444
start_time = time.time()
v = False
vv = False

class BoardState:
    def __init__(self, line):
        self.inp = line.split('|')[1:]
        self.board = []

        # ADD|0 0 0 1 3 4 0 8 9|3 0 0 0 0 5 0 0 0| ... |0 2 0 0 1 0 0 6 0
        # make a 2D array
        # for i in range(len(self.inp)):
        #     row = self.inp[i].split(' ')
        #     self.board.append([])
        #     for j in range(len(row)):
        #         self.board[i].append(int(row[j]))

        for i in self.inp:
            for j in i.split(' '):
                self.board.append(int(j))

    def printBoard(self):
        count = 0
        for i in self.board:
            if (count % 9) == 0:
                print ""
            print i,
            count += 1

    def same_row(self,i,j): return (i/9 == j/9)
    def same_col(self,i,j): return (i-j) % 9 == 0
    def same_block(self,i,j): return (i/27 == j/27 and i%9/3 == j%9/3)

    def find_moves(self,prev_row,prev_col):
        moves = []
        x = prev_row * 9 + prev_col
        x -= x % 9 # start at the beginning of the row
        first = True
        # do it for the row
        while first or (x % 9) != 0: # try each number until the end of the row
            first = False
            if v:
                print "X",x
            if self.board[x] == 0: # spot isn't already taken
                excluded_numbers = set()
                for y in range(81):
                    if self.same_row(x,y) or self.same_col(x,y) or self.same_block(x,y):
                        if vv:
                            print "Adding",self.board[y],"to excluded numbers"
                        excluded_numbers.add(self.board[y])

                for n in range(0,9):
                    if n not in excluded_numbers:
                        moves.append([x,n])
            x += 1

        # and for the column
        y = prev_row * 9 + prev_col
        y = y % 9
        if v:
            print "starting y:",y
        first = True

        while first or y <= 81: # try each number until the end of the row
            first = False
            if v:
                print "Y",y
            if y > len(self.board)-1:
                if v:
                    print "y > board size",y,len(self.board)
                break
            if self.board[y] == 0: # spot isn't already taken
                excluded_numbers = set()
                for x in range(81):
                    if self.same_row(x,y) or self.same_col(x,y) or self.same_block(x,y):
                        if vv:
                            print "Adding",self.board[y],"to excluded numbers"
                        excluded_numbers.add(self.board[x])

                for n in range(0,9):
                    if n not in excluded_numbers:
                        moves.append([y,n])
            y += 9

        return moves

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def printTime():
    print "Time:",repr(round(time.time() - start_time,2))
        
def format_move(x):
    # 81 n
    if v:
        print "Formatting move:",x
        print x[0]/9,x[0]%9,x[1]
    return(("%s %s %s\n") % (repr(x[0]/9),repr(x[0]%9),repr(x[1])))

def make_move( line, prev_move ):
    b = BoardState( line )
    if v:
        print "Current board:"
        b.printBoard()
    
    if prev_move is not None:
        prev_row = int(prev_move[0])
        prev_col = int(prev_move[1])
    else:
        print "\nno prev move!",prev_move
        prev_row = 5
        prev_col = 5

    if v:
        print "Finding moves",prev_row,prev_col
    moves = b.find_moves(prev_row,prev_col)

    if v:
        print "Moves:\n",moves

    if len(moves) == 0:
        print "I resign... Dammit"
        exit_game()

    return format_move(moves[random.randint(0,len(moves)-1)]) # random move :-/

def exit_game():
    printTime()
    print "Game over... womp womp"
    sys.exit(0)

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

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        usage()
        sys.exit(1)

    # verbose
    if "-v" in sys.argv:
        v = True
        vv = False
    elif "-vv" in sys.argv:
        v = True
        vv = True
    else:
        v = False
        vv = False

    # Open connection to evasion server
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))
    print "Connected to", HOST, "port", PORT

    join = repr(sys.argv[1]) + "\n"
    s.send(join)

    prev_move = None
    my_move = None

    while True:
        # Read status line
        data = SReadLine (s)
        line = string.strip (data)

        print line

        if len(line.split(' ')) == 3:
            if v:
                print "Length of line.split == 3",line.split(' ')
                if my_move is not None:
                    print "My prev move",my_move.strip().split(' ')
                print "checking if they're equal"
            if my_move is None:
                if v:
                    print "they're not"
                prev_move = line.split(' ')
            elif my_move.strip() == line:
                if v:
                    print "Guess that was my move..."
            else:
                prev_move = line.split(' ')
        if "ADD" in line:
            if v:
                print "Making move with",line,prev_move
            my_move = make_move( line, prev_move )
            print "My move:",my_move
            s.send( my_move )

        if "GAME OVER" in line:
            exit_game()

    s.close()
