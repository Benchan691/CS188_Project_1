# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    "*** YOUR CODE HERE ***"
    s = util.Stack()
    visited_before = set()

    start_state = problem.getStartState()
    s.push((start_state, []))

    while not s.isEmpty():
        cs, actions = s.pop()

        if cs in visited_before:
            continue

        visited_before.add(cs)

        if problem.isGoalState(cs):
            return actions

        for next_state, action, cost in problem.getSuccessors(cs):
            new_actions = actions + [action]
            s.push((next_state, new_actions))

    return []


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    s = util.Queue()
    visited_before = set()

    start_state = problem.getStartState()
    s.push((start_state, []))

    while not s.isEmpty():
        cs, actions = s.pop()

        if cs in visited_before:
            continue

        visited_before.add(cs)

        if problem.isGoalState(cs):
            return actions

        for next_state, action, cost in problem.getSuccessors(cs):
            if next_state not in visited_before:
                new_actions = actions + [action]
                s.push((next_state, new_actions))

    return []


def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    s = util.PriorityQueue()
    visited_before = set()

    start_state = problem.getStartState()
    s.push((start_state, [], 0), 0)

    while not s.isEmpty():
        cs, actions, current_cost = s.pop()

        if cs in visited_before:
            continue

        visited_before.add(cs)

        if problem.isGoalState(cs):
            return actions

        for next_state, action, step_cost in problem.getSuccessors(cs):
            if next_state not in visited_before:
                new_actions = actions + [action]
                new_cost = current_cost + step_cost
                s.update((next_state, new_actions, new_cost), new_cost)

    return []


def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    s = util.PriorityQueue()
    best_g = {}

    start_state = problem.getStartState()

    # the stack stores three values : (state, actions, cost_so_far)
    # Priority is: cost_so_far + heuristic
    s.push((start_state, [], 0), heuristic(start_state, problem))
    best_g[start_state] = 0

    while not s.isEmpty():
        cs, actions, current_cost = s.pop()

        # If we found a path with a higher cost, than one already found, ignore it.
        if current_cost > best_g.get(cs, float('inf')):
            continue

        if problem.isGoalState(cs):
            return actions

        for next_state, action, step_cost in problem.getSuccessors(cs):
            new_cost = current_cost + step_cost

            # If we've found a better or new path to the successor, add it to the s
            if next_state not in best_g or new_cost < best_g[next_state]:

                best_g[next_state] = new_cost

                new_actions = actions + [action]

                priority = new_cost + heuristic(next_state, problem)

                s.push((next_state, new_actions, new_cost), priority)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
