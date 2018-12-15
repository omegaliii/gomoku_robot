#import pygame
#from pygame.locals import *
from sys import exit
from boardstate import *
from gomoku import Gomoku
#from render import GameRender
from gomoku_ai import *

def transform(mat):
    #input: int 2d array
    #output: BoardState 2d array
    states = [BoardState.EMPTY, BoardState.BLACK, BoardState.WHITE]
    rt = []
    for i in range(len(mat)):
        rt_row = []
        for j in range(len(mat[i])):
            rt_row.append(states[mat[i][j]])
        rt.append(rt_row)
    return rt

def calculator(mat):
    #input: (2d array) boardstate
    #output: (tuple,2 elements) position
    gomoku = Gomoku()
    for i in range(N):
        for j in range(N):
            gomoku.set_chessboard_state(i,j,mat[i][j])

    ai = gomokuAI(gomoku, BoardState.BLACK, 1)
    #render = GameRender(gomoku)
    result = BoardState.EMPTY
    boolean, position = ai.one_step()
    return position

def check_win(mat,digit):
    #input: a matrix -- N*N gomoku board
    #input: an int -- represent which player is currently checked
    #output: None if digit is invalid, "player" if player wins, "robot" if robot wins
    #print: "player wins" or "robot wins" or nothing
    player = None
    if digit == 1:
        player = "player"
    if digit == 2:
        player = "robot"
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if i + 4 < len(mat):
                #down
                if mat[i][j] == digit and mat[i+1][j] == digit and mat[i+2][j] == digit and mat[i+3][j] == digit and mat[i+4][j] == digit:
                    print(player + " wins!")
                    return player
                if j + 4 < len(mat[i]):
                    #righr down
                    if mat[i][j] == digit and mat[i+1][j+1] == digit and mat[i+2][j+2] == digit and mat[i+3][j+3] == digit and mat[i+4][j+4] == digit:
                        print(player + " wins!")
                        return player
                if j - 4 >= 0:
                    #left down
                    if mat[i][j] == digit and mat[i+1][j-1] == digit and mat[i+2][j-2] == digit and mat[i+3][j-3] == digit and mat[i+4][j-4] == digit:
                        print(player + " wins!")
                        return player
            if j + 4 < len(mat[i]):
                #right
                if mat[i][j] == digit and mat[i][j+1] == digit and mat[i][j+2] == digit and mat[i][j+3] == digit and mat[i][j+4] == digit:
                    print(player + " wins!")
                    return player
    return None

def detector(ori,new):
    #1 represents player's chess piece
    #input:orginal matrix, new matrix
    #output:(list of tuple) erase & draw
    #extra output:(list of tuple) reminder: let player put his/her chess pieces on the board in order to recover game
    valid = True
    erase = []
    draw = []
    reminder = []
    one_step = False #record whether access player's new step
    for i in range(len(ori)):
        for j in range(len(ori[i])):
            if ori[i][j] != new[i][j]:
                if ori[i][j] == 0 and new[i][j] == 1 and not one_step:
                    one_step = True
                else:
                    valid = False
    if valid:
        tr_new = transform(new)
        draw.append(calculator(tr_new))
        return erase,draw
    else:
        for i in range(len(ori)):
            for j in range(len(ori[i])):
                if ori[i][j] != new[i][j] and new[i][j] != 0:
                    erase.append((i,j))
                    new[i][j] = 0 #revise the new matrix, possibly produce bug
        for i in range(len(ori)):
            for j in range(len(ori[i])):
                if ori[i][j] != new[i][j]:
                    if ori[i][j] == 1:
                        reminder.append((i,j))
                        new[i][j] = 1
                    else:
                        draw.append((i,j))
                        new[i][j] = 2
    return erase,draw



#run in terminal
if __name__ == '__main__':

    """
    #change the AI here, bigger the depth stronger the AI
    f = open('boardmatrix1.txt', 'r')
    matrixboard = []
    for i in range(15):
        row = f.readline()
        introw = []
        while "," in row:
            introw.append(int(row[:row.find(",")]))
            row = row[row.find(",")+1:]
        matrixboard.append(introw)
    """

    #test case 1:
    mat4 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]

    mat5 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    mat5_2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    mat_win1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,2,1,0,0,0,0,0,0],
    [0,0,0,0,0,2,1,1,0,2,0,0,0,0,0],
    [0,0,0,0,0,0,2,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    mat_win2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,2,0,0,0,0,2,1,0,0,0,0,0],
    [0,0,0,1,2,0,0,2,1,0,0,0,0,0,0],
    [0,0,0,0,0,2,1,1,0,2,1,0,0,0,0],
    [0,0,0,0,0,1,2,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,2,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    #print(detector(mat4,mat5)) #valid len(draw) = 1
    #print(detector(mat5,mat4)) #erase:[],draw:[]
    #print(detector(mat5,mat5_2)) #len(erase) = 1,len(draw) = 1
    check_win(mat_win2,2)
