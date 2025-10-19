import pygame
import numpy as np
import math
import heapq

goal = np.empty((3,3), dtype=int)
w = 50 # weight for A* algorithm

class AI:
    def __init__(self, start, goal_param):
        global goal
        goal = goal_param  # final node / goal board
        self.start = Node(start, parent=None) # initial node/ starting board
        self.open_list = [] # list of nodes to be evaluated
        heapq.heappush(self.open_list, (self.start.f, self.start)) # push the starting node to the open list
        self.closed_list = set() # list of nodes already evaluated



def heuristic(state, goal):
        manhattan_distance = 0
        
        pieces_in_place = 0
        goal_i, goal_j = np.where(goal == 1)
        goal_positions = list(zip(goal_i, goal_j)) 
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != 0:  # Don't calculate distance for the empty tile
                    min_distance = float('inf')
                    for goal_i, goal_j in goal_positions:
                        manhattan_distance_tile = abs(i - goal_i) + abs(j - goal_j)  # Calculate the Manhattan distance for this tile
                        if manhattan_distance_tile < min_distance:
                            min_distance = manhattan_distance_tile
                    
                    print(manhattan_distance_tile)
                    manhattan_distance += min_distance
                    if (i, j) in goal_positions:
                        pieces_in_place += 1
                    
        print("Manhattan distance: ", manhattan_distance)
        print("Pieces in place: ", pieces_in_place)
        print("Heuristic: ", (manhattan_distance - pieces_in_place) / len(state))
        return (manhattan_distance - pieces_in_place) / len(state) # We divide because we shift multiple tiles at once

class Node:
    def __init__(self, start,parent):
        self.state = start # initial state of the board
        self.g = 0 # cost from start to current node
        self.h = heuristic(start,goal) # cost from current node to goal
        self.f = self.g + w * self.h # total cost
        self.parent = parent # parent node

    def __lt__(self, other):
        return self.f < other.f

def neighborsNode(parent):
    neighbors = []
    state = parent.state

    for i in range(len(state)):
        # Shift row to the left
        new_state = state.copy()
        new_state[i] = np.roll(new_state[i], -1)
        neighbors.append(Node(new_state,parent))

        # Shift row to the right
        new_state = state.copy()
        new_state[i] = np.roll(new_state[i], 1)
        neighbors.append(Node(new_state,parent))

    for j in range(len(state[0])):
        # Shift column up
        new_state = state.copy()
        new_state[:, j] = np.roll(new_state[:, j], -1)
        neighbors.append(Node(new_state,parent))

        # Shift column down
        new_state = state.copy()
        new_state[:, j] = np.roll(new_state[:, j], 1)
        neighbors.append(Node(new_state,parent))

    return neighbors


def A_star(ai):                                            #Driver function
    #run until open list is empty
    removed_nodes = set()
    
    while ai.open_list:     
        f, process = heapq.heappop(ai.open_list) # current node being processed
        #print("Current:\n", process.state)
       
        hashable_node = tuple(process.state.flatten())
        if hashable_node in removed_nodes:
            continue

        if np.array_equal(process.state, goal): # goal found
            return path(process)            #path to goal found
        
        removed_nodes.add(hashable_node)
        ai.closed_list.add(hashable_node)

        neighbors = neighborsNode(process)
        print("Node has {f} neighbors\n".format(f=len(neighbors)))
        for node in neighbors: 
            print("Neighbor f value:\n", node.f)

        open_set = set()
        
        for node in neighbors:
            node_state = tuple(node.state.flatten())

            if node_state in ai.closed_list:  # Does exist in closed list
                continue  # skip this loop once

            existing_node = next((n for f, n in ai.open_list if np.array_equal(n.state, node.state)), None)  # if exists find node in open_list

            if existing_node is None:  # Does not exist in open list
                heapq.heappush(ai.open_list, (node.f, node))
                open_set.add(node_state)
            else:
                if node.g < existing_node.g:  # better g score for same node found
                    #print(existing_node.state)
                    existing_node.g = node.g
                    existing_node.f = node.f
                    existing_node.parent = node.parent  # change parent to better(earlier parent)
    print("Not possible to reach goal")
    return []

def IDA_star(ai):
    threshold = ai.start.h
    while True:
        temp = search(ai.start, 0, threshold, goal)
        if isinstance(temp, Node):  # If temp is a node, then it's the solution
            return path(temp)
        if temp == float('inf'):
            return [] # No solution
        threshold = temp

def search(node, g, threshold, goal):
    f = g + node.h
    if f > threshold:
        return f
    if np.array_equal(node.state, goal):
        return node  # Return the solution
    min = float('inf')
    neighbors = neighborsNode(node)
    print("Node has {f} neighbors\n".format(f=len(neighbors)))
    for node in neighbors: 
        print("Neighbor f value:\n", node.f)
    for successor in neighbors:
        temp = search(successor, g + 1, threshold, goal)  # Assuming cost of all moves is 1
        if isinstance(temp, Node):  # If temp is a node, then it's the solution
            return temp
        if temp < min:
            min = temp
    return min

def path(node): #construct the path from node to start using node.parent
    path = []
    print("Creating path")
    while node is not None:
        print("Path:\n",node.state)
        path.append(node.state)
        node = node.parent
    return path[::-1]  # Reverse the path to start from the beginning


def neighbors(state):
    neighbors = []
    for i in range(len(state)):
        # Shift row to the left
        new_state = state.copy()
        new_state[i] = np.roll(new_state[i], -1)
        neighbors.append(new_state)

        # Shift row to the right
        new_state = state.copy()
        new_state[i] = np.roll(new_state[i], 1)
        neighbors.append(new_state)

    for j in range(len(state[0])):
        # Shift column up
        new_state = state.copy()
        new_state[:, j] = np.roll(new_state[:, j], -1)
        neighbors.append(new_state)

        # Shift column down
        new_state = state.copy()
        new_state[:, j] = np.roll(new_state[:, j], 1)
        neighbors.append(new_state)

    return neighbors

# Depth-Limited Search
def DLS(start, goal, depth, visited):
    #print(depth)
    if np.array_equal(start,goal):
        return True, [start]

    if depth <= 0:
        return False, []

    visited.add(tuple(start.flatten()))

    for neighbor in neighbors(start):
        if tuple(neighbor.flatten()) not in visited:
            found, path = DLS(neighbor, goal, depth - 1, visited)
            if found:
                return True, [start] + path

    return False, []

# Iterative Deepening Depth-First Search
def IDDFS(start, goal, max_depth):
    for depth in range(max_depth):
        print(depth)
        visited = set()
        found, path = DLS(start, goal, depth, visited)
        if found:
            return path
    return []