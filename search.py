# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""
import copy
import sys
import time
import util
from spade import pyxf
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    xsb = pyxf.xsb('/Users/zephyrYin/Documents/tools/XSB/bin/xsb')
    xsb.load('./maze.P')
    xsb.load('./dfs.P')
    startTime = time.clock()
    result = xsb.query('solve(X).')
    print time.clock() - startTime
    print result
    path = result[0]['X']
    tempList = path[1:-1].split(',')
    pathList = [int(x) for x in tempList]

    return path2Action(pathList)

def path2Action(pathList):
    e = Directions.EAST
    n = Directions.NORTH
    s = Directions.SOUTH
    w = Directions.WEST

    actionList = []
    for i in range(0, len(pathList) - 1):
        if pathList[i] > pathList[i+1]:
            if pathList[i] - pathList[i+1] == 1:
                actionList.append(w)
            else:
                actionList.append(s)
        elif pathList[i] < pathList[i+1]:
            if pathList[i+1] - pathList[i] == 1:
                actionList.append(e)
            else:
                actionList.append(n)
    return actionList

def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"

    "*** YOUR CODE HERE ***"
    startTime = time.clock()
    mazeFilePath = './maze.P'
    foodList = getFoodStatus(mazeFilePath)
    permutationList = getPermutations(foodList)                 # get all the 24 permutations of food list

    file = open(mazeFilePath)
    lines = file.readlines()

    pathLists = []
    xsb = pyxf.xsb('/Users/zephyrYin/Documents/tools/XSB/bin/xsb')
    for i in range(len(permutationList)):
        reviseMazeFile(mazeFilePath, lines, permutationList[i])
        xsb.load(mazeFilePath)
        xsb.load('./bfs.P')
        result = xsb.query('solve(F).')
        fullPath = result[0]['F']
        tempList = fullPath[1:-1].split(',')
        pathList = [int(x) for x in tempList]
        print pathList
        pathLists.append(pathList)
    shortestPath = getShortest(pathLists)                       # find a shortest path
    print 'time cost:'
    print time.clock() - startTime
    return path2Action(shortestPath)

def getShortest(pathList):
    minLen = sys.maxint
    if len(pathList) == 1:
        return pathList[0]
    index = 0
    for i in range(len(pathList)):
        if len(pathList[i]) < minLen:
            minLen = len(pathList[i])
            index = i
    return pathList[index]

def reviseMazeFile(path, lines, foodList):
    cnt = 0
    for i in range(len(lines)):
        if 'food' in lines[i]:
            left = lines[i].index('(')
            right = lines[i].index(')')
            line = lines[i][0:left+1] + foodList[cnt] + lines[i][right:len(lines[i])]
            lines = lines[0:i] + [line] + lines[i+1:len(lines)]
            cnt = cnt + 1
        if cnt >= len(foodList):
            break
    file = open(path,'w')
    for line in lines:
        file.write(str(line))
    file.close()

def getFoodStatus(path):
    file = open(path)
    lines = file.readlines()
    foodList = []
    for line in lines:
        if 'food' in line:
            left = line.index('(')
            right = line.index(')')
            foodIndex = line[left+1:right]
            foodList.append(foodIndex)
    file.close()
    return foodList

def getPermutations(list):
    if len(list) < 2:
        return list
    result = []
    permutations(list, result, 0)
    return result

def permutations(list, result, cur):
    if cur >= len(list):
        result.append(copy.deepcopy(list))
        return
    for i in range(cur, len(list)):
        list[cur], list[i] = list[i], list[cur]
        permutations(list, result, cur+1)
        list[cur], list[i] = list[i], list[cur]

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    mazeFile = 'maze.P'
    heuFile = 'heu.P'
    createHeuFile(problem, heuristic, heuFile)
    xsb = pyxf.xsb('/Users/zephyrYin/Documents/tools/XSB/bin/xsb')
    xsb.load('./maze.P')
    xsb.load('./heu.P')
    xsb.load('./astar.P')
    startTime = time.clock()
    result = xsb.query('solve(P/C).')
    print time.clock() - startTime
    path = result[0]['P']
    tempList = path[1:-1].split(',')
    pathList = [int(x) for x in tempList]
    print pathList
    return path2Action(pathList)

def createHeuFile(problem, heuristic, heuFileName):
    file = open(heuFileName, 'w')
    heuList = []
    height = problem.walls.width - 2
    width = problem.walls.height - 2
    for w in range(1, width+1):
        for h in range(1, height+1):
            if problem.walls[h][w]:
                continue
            index = (w-1) * height + h
            cost = heuristic((h,w), problem)
            heuList.append((index, cost))
    for l in heuList:
        file.write('heuristic(' + str(l[0]) + ', ' +str(l[1]) + ').')
        file.write('\n')
    file.close()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch