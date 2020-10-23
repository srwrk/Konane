import Game
import math


# declare global variables
plusInf = float("inf")
negInf = -plusInf
evaluationNum = 0
numOfChildren = 0
nonLeaves = 0
cutoff = 0

"""
minimax algorithm, taken from class slides, limits depth to prespecified number
"""
def minMaxDecision(gameState):
    global evaluationNum
    global numOfChildren
    global nonLeaves
    global cutoff
    global capDepth
    nonLeaves += 1
    action = [[0,0],[0,0]]
    maximum = negInf
    childState = Game.GameState()
    depth = gameState.getDepth()
    for a in Game.actions(gameState):
        numOfChildren += 1
        childState.makeEqual(gameState)
        childState.actionToState(a)
        currentValue = minValue(childState,depth)
        if currentValue > maximum :
            maximum = currentValue
            action = [row[:] for row in a]
    return action

# part of MiniMax algorithm
def maxValue(gameState,depth):
    global evaluationNum
    global numOfChildren
    global nonLeaves
    global cutoff
    global capDepth
    childState = Game.GameState()
    if(gameState.getDepth() - depth >=capDepth or gameState.isGameOver()[0]):
        evaluationNum += 1
        return Game.utilityFunction(gameState)

    nonLeaves += 1
    maximum = negInf
    for a in Game.actions(gameState):
        numOfChildren += 1
        childState.makeEqual(gameState)
        childState.actionToState(a)
        maximum = max(maximum,minValue(childState,depth))
    return maximum

# part of MiniMax algorithm
def minValue(gameState,depth):
    global evaluationNum
    global numOfChildren
    global nonLeaves
    global cutoff
    global capDepth
    childState = Game.GameState()
    if(gameState.getDepth() - depth>=capDepth or gameState.isGameOver()[0]):
        evaluationNum += 1
        return Game.utilityFunction(gameState)

    nonLeaves += 1
    minimum = plusInf
    for a in Game.actions(gameState):
        numOfChildren += 1
        childState.makeEqual(gameState)
        childState.actionToState(a)
        minimum = min(minimum,maxValue(childState,depth))
    return minimum

"""
Minimax algorithm with alpha-beta pruning, taken from class textbook. Depth is capped at a prespecified number,
"""
def minimax_alpha_beta(gameState,alpha,beta,depth):
    global evaluationNum
    global numOfChildren
    global nonLeaves
    global cutoff
    global capDepth
    bestAction = [[0,0],[0,0]]
    childState = Game.GameState()
    if(depth >= capDepth or gameState.isGameOver()[0]):
        evaluationNum += 1
        return [Game.utilityFunction(gameState),None]
    nonLeaves += 1
    if gameState.getTurn() == 1:
        for a in Game.actions(gameState):
            numOfChildren += 1
            childState.makeEqual(gameState)
            childState.actionToState(a)
            currentMM = minimax_alpha_beta(childState,alpha,beta,depth+1)
            if currentMM[0] >= beta:
                cutoff += 1
                return [currentMM[0],None]
            if currentMM[0] > alpha:
                alpha = currentMM[0]
                bestAction = [row[:] for row in a]
        return [alpha,bestAction]

    for a in Game.actions(gameState):
        numOfChildren += 1
        childState.makeEqual(gameState)
        childState.actionToState(a)
        currentMM = minimax_alpha_beta(childState,alpha,beta,depth+1)
        if currentMM[0] <= alpha:
            cutoff += 1
            return [currentMM[0],None]
        if currentMM[0] < beta:
            beta = currentMM[0]
            bestAction = [row[:] for row in a]
    return [beta,bestAction]
        
# translates letter into a directional vector
def switch(string):
    switcher = {
        "U": [-1,0],
        "D": [1,0],
        "L": [0,-1],
        "R": [0,1]
    }
    return switcher.get(string, "invalid direction")

# prints out what action took place, including starting piece, direction, and number of jumps
def printAction(action):
    if(action[1][0] ==0 and action[1][1] == 0):
        print("Remove "+ str(action[0][0])+" "+str(action[0][1]))
        return
    coorX = action[0][0]
    coorY = action[0][1]
    if (action[0][0] == action[1][0]):
        if (action[0][1]<action[1][1]):
            direction = "R"
            jump = (action[1][1] - action[0][1])/2
        else:
            direction = "L"
            jump = (action[0][1] - action[1][1])/2
    else:
        if (action[0][0]<action[1][0]):
            direction = "D"
            jump = (action[1][0] - action[0][0])/2
        else:
            direction = "U"
            jump = (action[0][0] - action[1][0])/2
    print(str(coorX)+" "+str(coorY)+" "+direction+" "+str(jump))

"""
computer vs. computer game
"""
def compVSComp(typeOfAlg):
    # minimax
    if(typeOfAlg == 1):
        gameState = Game.GameState()
        gameState.printBoard()
        while (gameState.isGameOver()[0] == False):
            action = minMaxDecision(gameState)
            gameState.actionToState(action)
            printAction(action)
            gameState.printBoard()
        print(str(gameState.isGameOver()[1]) + " won the game!\n")
        print("# of static evaluations: "+ str(evaluationNum))
        print("avarage branching factor: " + str(float(numOfChildren)/nonLeaves))
        print("number of cutoffs: "+ str(cutoff))
        return

    # minimax with alpha-beta pruning
    if(typeOfAlg == 2):
        gameState = Game.GameState()
        gameState.printBoard()
        while (gameState.isGameOver()[0] == False):
            action = minimax_alpha_beta(gameState,negInf,plusInf,0)[1]
            printAction(action)
            gameState.actionToState(action)
            gameState.printBoard()
        print(str(gameState.isGameOver()[1]) + " won the game!\n")
        print("# of static evaluations: "+ str(evaluationNum))
        print("avarage branching factor: " + str(float(numOfChildren)/nonLeaves))
        print("number of cutoffs: "+ str(cutoff))
        return

    else:
        print ("The type of algorithm is invalid")

"""
person vs. computer game
"""
def personVSComp(typeOfAlg):
    # minimax with alpha-beta pruning
    if(typeOfAlg == 2):
        turn = int(input("which player is the computer? (1 for black, 2 for White): "))
        gameState = Game.GameState()
        action = [[0,0],[0,0]]
        while (gameState.isGameOver()[0] == False):
            if (gameState.getTurn()==turn):
                action = minimax_alpha_beta(gameState,negInf,plusInf,0)[1]
                printAction(action)
            else:
                if(gameState.getDepth() == 0 or gameState.getDepth() == 1):
                    var = raw_input("Which Piece Do You Want To Remove? ")
                    action[0][0] = int(var.split(" ")[0])
                    action[0][1] = int(var.split(" ")[1])
                    action[1][0] = 0
                    action[1][1] = 0
                else:
                    var = raw_input("Please input your move in this format: \" X Y DIRECTION NUMBER_OF_JUMPS \".\nNote that directions are U, D, L, and R.\n")
                    coorX = int(var.split(" ")[0])
                    coorY = int(var.split(" ")[1])
                    direction = switch(var.split(" ")[2])
                    jumps = int(var.split(" ")[3])
                    action[0][0] = coorX
                    action[0][1] = coorY
                    action[1][0] = coorX + 2*jumps*direction[0]
                    action[1][1] = coorY + 2*jumps*direction[1]
                    if(not gameState.isActionValid(action)):
                        print("The Action Is Not Valid.")
                        return
            gameState.actionToState(action)
            print gameState.getDepth()
            gameState.printBoard()
        print(str(gameState.isGameOver()[1]) + " won the game!\n")
        return

    # minimax
    if(typeOfAlg == 1):
        turn = int(input("which player is the computer? (1 for black, 2 for White): "))
        gameState = Game.GameState()
        action = [[0,0],[0,0]]
        while (gameState.isGameOver()[0] == False):
            if (gameState.getTurn()==turn):
                action = minMaxDecision(gameState)
                printAction(action)
            else:
                if(gameState.getDepth() == 0 or gameState.getDepth() == 1):
                    var = raw_input("Which Piece Do You Want To Remove? ")
                    action[0][0] = int(var.split(" ")[0])
                    action[0][1] = int(var.split(" ")[1])
                    action[1][0] = 0
                    action[1][1] = 0
                else:
                    var = raw_input("Please input your move in this format: \" X Y DIRECTION NUMBER_OF_JUMPS \".\nNote that directions are U, D, L, and R.\n")
                    coorX = int(var.split(" ")[0])
                    coorY = int(var.split(" ")[1])
                    direction = switch(var.split(" ")[2])
                    jumps = int(var.split(" ")[3])
                    action[0][0] = coorX
                    action[0][1] = coorY
                    action[1][0] = coorX + 2*jumps*direction[0]
                    action[1][1] = coorY + 2*jumps*direction[1]
            gameState.actionToState(action)
            print gameState.getDepth()
            gameState.printBoard()
        print(str(gameState.isGameOver()[1]) + " won the game!\n")
        return

    print ("The type of algorithm is invalid")
        
if __name__ == "__main__":
    
    global capDepth

    # asks user for mode of play
    answer = raw_input("Mode of Play: Do you want to player versus a computer? Y/N\n")
    typeOfAlgo = int(raw_input("What kind of algorithm do you want to use? Press 1 for MiniMax and 2 for MiniMax with Alpha-Beta Pruning.\n"))
    capDepth = 2*int(raw_input("For your algorithm, what do you want the cap ply to be?\n"))
    
    if(answer == "Y"):
        personVSComp(typeOfAlgo)
    elif(answer == "N"):
        compVSComp(typeOfAlgo)
    else:
        print ("The mode of play in invalid")
       
