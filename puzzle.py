
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import resource
import heapq

## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        # Make sure that the blank tile is not in the first row
        if (self.blank_index > self.n-1):
            # Create new list called up_list
            up_list = self.config[:]
            # Identify new index that the blank will be moved to (1 row up, thus n indices back)
            new_blank_index = self.blank_index - self.n;
            # Set value at the blank_index to be the value at the index the blank will be moved to
            up_list[self.blank_index] = up_list[new_blank_index]
            # Set value of new_blank_index to be 0
            up_list[new_blank_index] = 0
            
            # return new PuzzleState with updated config list, same n (size of board), parent equal to self, action "Up", and cost of 1
            return PuzzleState(up_list, self.n, self, "Up", self.cost+1)
        return None
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        '''
        print(self.blank_index)
        print("orignal before moving down:")
        self.display()
        '''
        # Make sure that blank tile is not in last row (has index less than n*n-n, for example for n=3, 8-puzzle, index should be less than 3*3-3 = 6)
        if (self.blank_index < (self.n*self.n-self.n)):
            # Create new list called down_list
            down_list = self.config[:]
            # Identify new index that the blank will be moved to (1 row down, thus n indices forward)
            new_blank_index = self.blank_index + self.n;
            # Set value at the blank_index to be the value at the index the blank will be moved to
            down_list[self.blank_index] = down_list[new_blank_index]
            # Set value of new_blank_index to be 0
            down_list[new_blank_index] = 0
            
            # return new PuzzleState with updated config list, same n (size of board), parent equal to self, action "Down", and cost of 1
            return PuzzleState(down_list, self.n, self, "Down", self.cost+1)
        return None
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        '''
        print(self.blank_index)
        print("orignal before moving left:")
        self.display()
        '''
        # Make sure that the blank node is not on the left of the board
        if (self.blank_index%self.n !=0):
            # Create new list called left_list
            left_list = self.config[:]
            # Identify new index that the blank will be moved to (1 column left, thus 1 index back)
            new_blank_index = self.blank_index-1;
            # Set value at the blank_index to be the value at the index the blank will be moved to
            left_list[self.blank_index] = left_list[new_blank_index]
            # Set value of new_blank_index to be 0
            left_list[new_blank_index] = 0
            # return new PuzzleState with updated config list, same n (size of board), parent equal to self, action "Left", and cost of 1
            return PuzzleState(left_list, self.n, self, "Left", self.cost+1)
        return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        '''
        print(self.blank_index)
        print("orignal before moving right:")
        self.display()
        '''
        # Make sure that the blank node is not the last node of the list or one of the elements on the right edge of the board
        if ((self.blank_index != (self.n *self.n -1)) and ((self.blank_index+1)%self.n !=0)):
            # Create new list called right_list
            right_list = self.config[:]
            # Identify new index that the blank will be moved to (1 column right, thus 1 index forward)
            new_blank_index = self.blank_index+1;
            # Set value at the blank_index to be the value at the index the blank will be moved to
            right_list[self.blank_index] = right_list[new_blank_index]
            # Set value of new_blank_index to be 0
            right_list[new_blank_index] = 0
            # return new PuzzleState with updated config list, same n (size of board), parent equal to self, action "Left", and cost of 1
            return PuzzleState(right_list, self.n, self, "Right", self.cost+1)
        return None
    
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt
def writeOutput(initial_state, goal_state, nodes_expanded, search_depth, max_search_depth, running_time):
    f = open("output.txt", "w")
    
    path = []
    curr_state = goal_state
    while(curr_state != initial_state):
        path.append(curr_state.action)
        curr_state = curr_state.parent
    path.reverse()
    
    f.write("path_to_goal: " + str(path) + '\n')
    print("path_to_goal: " + str(path) + '\n')
    f.write("cost_of_path: " + str(goal_state.cost) + "\n")
    print("cost_of_path: " + str(goal_state.cost) + "\n")
    f.write("nodes_expanded: " + str(nodes_expanded) + "\n")
    print("nodes_expanded: " + str(nodes_expanded) + "\n")
    f.write("search_depth: " + str(search_depth) + "\n")
    print("search_depth: " + str(search_depth) + "\n")
    f.write("max_search_depth: " + str(max_search_depth) + "\n")
    print("max_search_depth: " + str(max_search_depth) + "\n")
    f.write("running_time: " + str(running_time) + "\n")
    print("running_time: " + str(running_time) + "\n")
    f.write("max_ram_usage: " + str((resource.getrusage(resource.RUSAGE_SELF)[2])/(10**6)) + "\n")
    print("max_ram_usage: " + str((resource.getrusage(resource.RUSAGE_SELF)[2])/(10**6)) + "\n")
    
    f.close()

def bfs_search(initial_state):
    """BFS search"""
    '''
    frontier = Queue.new(initialState)
    explored = Set.new()
    
    while not frontier.isEmpty():
        state = frontier.dequeue()
        explored.add(state)
        
        if goalTest(state):
            return Success(state)
        for neighbor in state.neighbors():
            if neighbor not in frontier.union(explored):
                frontier.enqueue(neighbor)
    return failure
    '''
    starting_time = time.time()
    frontier = [initial_state]   
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    
    explored.add(tuple(initial_state.config))
    
    while len(frontier)>0:
        
        state = frontier.pop(0)
        
        if test_goal(state):
            running_time = time.time() - starting_time
            writeOutput(initial_state, state, nodes_expanded, state.cost, max_search_depth, running_time)
            
            # Success
            return
        
        # get children (neighbors) of state
        state.expand()
        nodes_expanded+=1
        
        for neighbor in state.children:
            if tuple(neighbor.config) not in explored:
            #if (neighbor not in frontier) and (tuple(neighbor.config) not in explored):
                frontier.append(neighbor)
                explored.add(tuple(neighbor.config))
                
                if (neighbor.cost > max_search_depth):
                    max_search_depth = neighbor.cost
    # Failure
    return

def dfs_search(initial_state):
    """DFS search"""
   
    '''
    frontier = Stack.new(initialState)
    explored = Set.new()
    
    while not frontier.isEmpty():
        state = frontier.pop()
        explored.add(state)
        
        if goalTest(state):
            return Success(state)
        for neighbor in state.neighbors():
            if neighbor not in frontier.union(explored):
                frontier.push(neighbor)
    return failure
    '''
    starting_time = time.time()
    frontier = [initial_state]
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    
    explored.add(tuple(initial_state.config))
    
    while len(frontier)>0:
        # Pop from stack in UDLR order
        state = frontier.pop()
        if test_goal(state):
            running_time = time.time() - starting_time
            writeOutput(initial_state, state, nodes_expanded, state.cost, max_search_depth, running_time)
            # Success
            return
        
        state.expand()
        nodes_expanded+=1
        # visit neighbors (push onto stack) in reverse-UDLR order
        for neighbor in state.children[::-1]:
            if tuple(neighbor.config) not in explored:
            #if (neighbor not in frontier) or (tuple(neighbor.config) not in explored):
                frontier.append(neighbor)
                #added this to combine explored and frontier
                explored.add(tuple(neighbor.config))
                
                if (neighbor.cost > max_search_depth):
                    max_search_depth = neighbor.cost
        
    # Failure
    return

def A_star_search(initial_state):
    """A * search"""
    '''
    frontier = Heap.new(initialState)
    explored = Set.new()
    
    while not frontier.isEmpty():
        state = frontier.deleteMin()
        explored.add(state)
        
        if goalTest(state):
            return Success(state)
        
        for neighbor in state.neighbors():
            if neighbor not in frontier.union(explored):
                frontier.insert(neighbor)
            else if neighbor in frontier:
                frontier.decreaseKey(neighbor)
    return failure
    '''
    starting_time = time.time()
    heuristic = initial_state.cost + calculate_total_cost(initial_state)
    
    frontier = []
    heapq.heapify(frontier) #make the frontier into a min heap (Priority Queue)
    # tuple to enter into frontier(cost, move(UDLR), timeinserted, PuzzleState)    
    heapq.heappush(frontier, (heuristic, initial_state.action, time.time(), initial_state))
    
    frontier_with_configs = set()
    frontier_with_configs.add(tuple(initial_state.config))
    
    # tuple to enter into frontier(cost, move(UDLR), timeinserted, PuzzleState)
    explored = set()
    
    nodes_expanded = 0
    max_search_depth = 0
    
    while len(frontier)>0:
        (heuristic, state_action, state_time, state) = heapq.heappop(frontier) # output tuple with heuristic, list of state, and actual state object
        frontier_with_configs.remove(tuple(state.config))
        explored.add(tuple(state.config)) # add the state list to the explored set
        if test_goal(state):
            running_time = time.time() - starting_time
            writeOutput(initial_state, state, nodes_expanded, state.cost, max_search_depth, running_time)
            # Success
            return
        
        state.expand()
        nodes_expanded+=1
        
        for neighbor in state.children:
            neighbor_heuristic = neighbor.cost + calculate_total_cost(neighbor)
                        
            if (tuple(neighbor.config) not in frontier_with_configs) and (tuple(neighbor.config) not in explored):
                
                heapq.heappush(frontier, ((neighbor_heuristic, neighbor.action, time.time(), neighbor)))
                frontier_with_configs.add(tuple(neighbor.config))
                
                if (neighbor.cost > max_search_depth):
                    max_search_depth = neighbor.cost

    # False
    return
def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    # sum up manhattan distances of each tile
    total_cost = 0
    for i in range((state.n)**2):
        total_cost+= calculate_manhattan_dist(i, state.config[i], state.n)
    return total_cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    return (math.fabs(idx-value)%n + int(math.fabs(idx-value)/n))

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    goal_state_list = []
    for i in range((puzzle_state.n)**2):
        goal_state_list.append(i)
    return (puzzle_state.config == goal_state_list)

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()