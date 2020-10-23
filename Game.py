from __future__ import print_function
import copy
import random

# declaring global variables
startTurn = 1 # black starts first
startCoordinates = [[8,8],[1,1],[5,5],[4,4]] # possible starting coordinates
neighbour = [[-1,0],[1,0],[0,-1],[0,1]] # possible directions
firstTurn = 1
bestUtility = 33 # utility value of winning move

"""
contains the current board, whose turn it is, and depth of the game
"""
class GameState:
    def __init__(self,board,turn,depth):
        self.board = board
        self.turn = turn
        self.depth = depth

    # initializes starting position
    def __init__ (self):
        self.board = [[0,0,0,0,0,0,0,0,0],[0,1,2,1,2,1,2,1,2],[0,2,1,2,1,2,1,2,1],[0,1,2,1,2,1,2,1,2],[0,2,1,2,1,2,1,2,1],
              [0,1,2,1,2,1,2,1,2],[0,2,1,2,1,2,1,2,1],[0,1,2,1,2,1,2,1,2],[0,2,1,2,1,2,1,2,1]]
        self.turn = firstTurn
        self.depth = 0

    # returns board
    def getBoard(self):
        return self.board

    # returns whose turn it is
    def getTurn(self):
        return self.turn

    # returns depth
    def getDepth(self):
        return self.depth

    # when game is over, return winner
    def isGameOver(self):
        if len(actions(self)) == 0:
            return [True,abs(3-self.turn)]
        return [False]

    """
    moves piece from start to finish, and removes opponent's piece in between
    """
    def movePiece(self, start, finish):
        self.board[finish[0]][finish[1]] = self.board[start[0]][start[1]]
        self.removePiece(start)
        direction = [0,0]
        direction[0] = (finish[0] - start[0])/(abs(finish[0]-start[0]) + abs(finish[1]-start[1]))
        direction[1] = (finish[1] - start[1])/(abs(finish[0]-start[0]) + abs(finish[1]-start[1]))
        position = [0,0]
        position[0] = start[0] + direction[0]
        position[1] = start[1] + direction[1]
        while(position[0]!=finish[0] or position[1]!=finish[1]):
            self.removePiece(position)
            position[0] = position[0] + direction[0]
            position[1] = position[1]+direction[1]

    # removes a piece
    def removePiece(self, pos):
        self.board[pos[0]][pos[1]] = 0

    # switch player's turn, increase depth
    def nextTurn(self):
        self.turn = abs(3-self.turn)
        self.depth = self.depth + 1

    # check the whole board for empty coordinates
    def emptyCoordinates(self):
        empty = []
        for i in range(1,len(self.getBoard())):
            for j in range(1,len(self.getBoard()[i])):
                if self.board[i][j] == 0:
                    empty.append([i,j])
        return empty

    # copies content of gameState
    def makeEqual(self,gameState):
        for i in range (len(self.getBoard())):
            for j in range (len(self.getBoard()[i])):
                self.board[i][j] = gameState.getBoard()[i][j]
        self.turn = gameState.getTurn()
        self.depth = gameState.getDepth()

    # print the whole board
    def printBoard(self):
        for i in range (1,len(self.getBoard())):
            for j in range (1,len(self.getBoard()[i])):
                print (self.getBoard()[i][j],end='')
            print (" ")

    # check if the action is valid
    def isValidAction(self,action):
        if(action[1][0] == 0 and action[1][1] == 0):
            return True
        
        if (self.getBoard()[action[0][0]][action[0][1]] != self.getTurn()):
            print ("the position doen't have a piece")
            return False
        if (self.getBoard()[action[1][0]][action[1][1]] != 0):
            print ("final position isn't empty")
            return False
        
        direction = [0,0]
        direction[0] = (action[1][0] - action[0][0])/(abs(action[1][0]-action[0][0]) + abs(action[1][1]-action[0][1]))
        direction[1] = (action[1][1] - action[0][1])/(abs(action[1][0]-action[0][0]) + abs(action[1][1]-action[0][1]))
        position = [0,0]
        position[0] = action[0][0] + direction[0]
        position[1] = action[0][1] + direction[1]
        counter = 0
        while(position[0]!=action[1][0] or position[1]!=action[1][1]):
            counter += 1
            if (counter % 2 == 1):
                if(self.getBoard()[position[0]][position[1]] != abs(3 - self.getTurn())):
                    print("we're jumping over something weird")
                    return False
            if (counter % 2 == 0):
                if(self.getBoard()[position[0]][position[1]] != 0):
                    return False
            position[0] = position[0] + direction[0]
            position[1] = position[1] + direction[1]
        return True
        

    # converts an action into a game state
    def actionToState(self, action):
        if (action[1][0] == 0 and action[1][1] == 0):
            self.removePiece(action[0])
            self.nextTurn()
        else:
            self.movePiece(action[0],action[1])
            self.nextTurn()

"""
check if coordinate is valid, i.e. inside board
"""
def isValid(coord):
    if (coord[0]<= 8 and coord[0]>0 and coord[1]<=8 and coord[1]>0):
        return True
    return False

"""
check current game state for all possible actions in the next turn
"""
def actions(gameState):
    possibleActions = []

    if gameState.getDepth() == 0:
        return firstMove(gameState)

    if gameState.getDepth() == 1:
        return secondMove(gameState)
    
    for i in range(1,len(gameState.getBoard())):
        for j in range(1,len(gameState.getBoard()[i])):
            if (gameState.getBoard()[i][j]!=0):
                possibleActions.extend(moves(gameState,[i,j]))
            
    return possibleActions

# black moves first
def firstMove(gameState):
    possibleActions = []
    action = [[0,0],[0,0]]
    for i in startCoordinates:
        action[0][0] = i[0]
        action[0][1] = i[1]
        possibleActions.append(action)
    return possibleActions

# first white move
def secondMove(gameState):
    possibleActions = []
    action = [[0,0],[0,0]]
    if len(gameState.emptyCoordinates()) != 1:
        return "ERROR!!!"
    coordinate = gameState.emptyCoordinates()[0]

    for i in neighbour:
        if(isValid([coordinate[0] + i[0],coordinate[1] + i[1]])):
            action[0][0] = coordinate[0] + i[0]
            action[0][1] = coordinate[1] + i[1]
            possibleActions.append(action)
    return possibleActions

"""
given a piece, return all possible moves starting from that piece
"""
def moves(gameState,coordinate):
    possibleActions = []
    curC = [0,0]
    action = [[0,0],[0,0]]
    for i in neighbour:
        curC[0] = coordinate[0]
        curC[1] = coordinate[1]
        action[0][0] = coordinate[0]
        action[0][1] = coordinate[1]
        while True:
            if(not isValid([curC[0] + 2*i[0],curC[1] + 2*i[1]])):
                break
            if(gameState.getBoard()[curC[0] + 2*i[0]][curC[1] + 2*i[1]] != 0):
                break
            if (gameState.getBoard()[curC[0] + i[0]][curC[1] + i[1]] != abs(3-gameState.getTurn())):
                break
            action[1][0] = curC[0]+2*i[0]
            action[1][1] = curC[1]+2*i[1]
            possibleActions.append(action)
            curC[0] = curC[0]+2*i[0]
            curC[1] = curC[1]+2*i[1]
    return possibleActions

    
"""
returns approximate utility - the number of black pieces that can move minus the number of white pieces that can move
"""
def utilityFunction(gameState):
    utility = 0
    if gameState.isGameOver()[0]:
        if gameState.isGameOver()[1] == 1:
            return bestUtility
        return -bestUtility
            
    for i in range (1,len(gameState.getBoard())):
        for j in range (1, len(gameState.getBoard()[i])):
            if gameState.getBoard()[i][j] != 0:
                if len(moves(gameState,[i,j])) >= 1:
                    if gameState.getBoard()[i][j] == 1:
                        utility = utility + 1
                    else:
                        utility = utility - 1
    return utility

"""
if __name__ == "__main__":
    gameState = GameState()
    action = [[0,0],[0,0]]
    gameState.printBoard()
    while (gameState.isGameOver()[0] == False):
        randomAction = random.choice(actions(gameState))
        action = [row[:] for row in randomAction]
        print (action)
        gameState.actionToState(action)
        gameState.printBoard()
    whoWon = "player " + str(gameState.isGameOver()[1]) + " won!"
    print(whoWon)
"""
    
    
    
