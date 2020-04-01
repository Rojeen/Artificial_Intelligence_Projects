#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
#import time
import copy
#import statistics

ROW = "ABCDEFGHI"
COL = "123456789"
tile_grids = [['A1','A2','A3','B1','B2','B3','C1','C2','C3'], ['A4','A5','A6','B4','B5','B6','C4','C5','C6'], ['A7','A8','A9','B7','B8','B9','C7','C8','C9'], \
              ['D1','D2','D3','E1','E2','E3','F1','F2','F3'], ['D4','D5','D6','E4','E5','E6','F4','F5','F6'], ['D7','D8','D9','E7','E8','E9','F7','F8','F9'], \
              ['G1','G2','G3','H1','H2','H3','I1','I2','I3'], ['G4','G5','G6','H4','H5','H6','I4','I5','I6'], ['G7','G8','G9','H7','H8','H9','I7','I8','I9']]

# From skeleton
def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

# From skeleton
def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def create_curr_val_dict(board):
    """Helper function to set the keys in the dictionary as A1...I9 with 
    corresponding values at that position """

    curr_val_dict = {}
    for r in ROW:
        for c in COL:
            curr_val_dict[r+c] = board[r+c] 

    return curr_val_dict

def initialize_domain_dict(board, dependency_dict):
    """Helper function to initialize a dictionary with the values in the domain of 
    positions that need to be determined. Do not add the original/unchangeable 
    set positions to the dictionary."""

    domain_dict = {}
    for r in ROW:
        for c in COL:
            if board[r+c] != 0:
                domain_dict[r+c] = [board[r+c]]
            else:
                domain_dict[r+c] = [1,2,3,4,5,6,7,8,9]
                # loop through all dependent tiles for the current tile
                for dependent_tile in dependency_dict[r+c]:
                    # if the dependent tile has an assigned value, remove it from domain_dict[r+c]
                    #print(board[dependent_tile])
                    #time.sleep(1)
                    if (board[dependent_tile] != 0) and (board[dependent_tile] in domain_dict[r+c]):
                        #print("remove from board")
                        domain_dict[r+c].remove(board[dependent_tile])
                    #print("domain_dict[r+c]: " + str(domain_dict[r+c]))       
    return domain_dict

def determine_MRV(curr_val_dict, domain_dict):
    
    domain_items = domain_dict.items()
    
    MRV_tile = ''
    MRV_domain_len = 11
    
    # determine the MRV
    for item in domain_items:
        
        # make sure that the item is not assigned a value yet, its length is smaller than MRV_val
        if (curr_val_dict[item[0]] == 0) and (len(item[1]) < MRV_domain_len):
            
            MRV_tile = item[0]
            MRV_domain_len = len(item[1])
    
    return MRV_tile

def forward_check_selection(value, MRV_tile, domain_dict, curr_val_dict, dependency_dict):
    for tile in dependency_dict[MRV_tile]:
        # if the tile has not been assigned and it contains the value in its domain
        if (curr_val_dict[tile] == 0) and (value in domain_dict[tile]):
            # if the tile only has that value in its domain, return None
            if len(domain_dict[tile]) == 1:
                return None
            else:
                # remove the value from the domain of the tile
                #print("remove " + str(value) + " from domain of " + str(tile))
                domain_dict[tile].remove(value)
    domain_dict[MRV_tile] = value
    return domain_dict


def check_selection(value, MRV_tile, curr_val_dict, dependency_dict):
    for tile in dependency_dict[MRV_tile]:
        if curr_val_dict[tile] == value:
            return False
    return True

#same as backtrack(assingment, csp) in lecture notes
# textbook p. 215
def backtracking_helper(curr_val_dict, domain_dict, dependency_dict): # returns a solution, or failure
    #print("start of backtracking_helper")
    #print("curr_val_dict: " + str(curr_val_dict))
    #print("domain_dict: " + str(domain_dict))
    
    '''if assignment is complete, return assignment'''
    if 0 not in curr_val_dict.values(): 
        return curr_val_dict
    
    '''var = select_unassigned_var(csp) AKA MRV'''
    MRV_tile = determine_MRV(curr_val_dict, domain_dict) # find the tile that is the MRV (ex. will be B2)
    #print("MRV_tile: " + MRV_tile)
    
    '''for each value in order_domain_values(var, assignment, csp)'''
    for value in domain_dict[MRV_tile]:  # try each value in the domain of the MRV tile
        #print("check " + str(value) + " in domain of MRV tile")
        
        # store original domain_dict
        original_domain_dict = copy.deepcopy(domain_dict)
        
        '''if value is consistent with assignment'''
        if check_selection(value, MRV_tile, curr_val_dict, dependency_dict):
            #print(str(value) + " is consistent with assingnment")
            
            '''add {var = value} to assignment'''  
            curr_val_dict[MRV_tile] = value # set the current value of the MRV_tile to the checked value in  curr_val_dict
            #print("add " + str(value) + " to assignment")
           
            # apply forward checking on all tiles that will be affected by the value for the MRV to reduce variable demands
            '''inferences = inference(csp, var,value)'''
            forward_check_dict = forward_check_selection(value, MRV_tile, domain_dict, curr_val_dict, dependency_dict)
            #print("apply forward checking")
            
            '''if inferences != failure'''
            if forward_check_dict != None:
                #print("forwardchecking passed")
                
                #print("set domain_dict to copy of forward_check_dict")
                '''add inferences to assignment'''
                domain_dict = forward_check_dict.copy()
                
                #print("recursively call backtrack with curr_val_dict, domain_dict")
                '''result = backtrack(assignment, csp)'''
                result = backtracking_helper(curr_val_dict, domain_dict, dependency_dict) #result = backtrack(assignmnet, csp)
                
                '''if result != failure, then return result'''
                if result != None: #if result != failure
                    #print("result is not None so return result: " + str(result))
                    return result
            #print("forwardchecking did not pass so revert assigments")
            '''remove {var = value} and inferences from assignment'''
            #print("set value of MRV (" + str(MRV_tile) + ") back to 0")
            # set the value of the MRV back to 0
            curr_val_dict[MRV_tile] = 0 # set the MRV back to 0
            
            # Revert the domains (remove inferences from assignment) using deep copy
            domain_dict = copy.deepcopy(original_domain_dict)
            #print("revert domain_dict back to original: " + str(domain_dict))
    
    # return Failure
    return None     

# From skeleton (same as backtracking_search in lecture notes)
def backtracking(board):
    """Takes a board and returns solved board."""
    '''
    Implement backtracking search using the minimum remaining value heuristic. 
    Pick your own order of values to try for each variable, and apply forward 
    checking to reduce variables domains.
    '''
    #print(board)
    
    # change from curr_val_dict to board
    dependency_dict = create_dict_dependencies(board)
    #print("dependency dict: " + str(dependency_dict))
    
    # create a dictionary with domains for the tiles that are constrained based on preset values
    domain_dict = initialize_domain_dict(board, dependency_dict)
    #print("domain dict" + str(domain_dict))
    
    # change from curr_val_dict to board
    # backtracking_helper same as backtrack(assingment, csp) in lecture notes                
    found_board = backtracking_helper(board, domain_dict, dependency_dict)
    
    if found_board == None:
        #print("not solvable")
        solved_board = board # could not find solution
    else:
        #print("solved")
        solved_board = found_board.copy()
    
    return solved_board

def create_dict_dependencies(curr_val_dict):
    dependency_dict = {}
    for tile in curr_val_dict.keys():
        dependency_dict[tile] = []
        grid_found = False
        grid = []
        
        while(grid_found == False):
            for i in range(len(tile_grids)):
                for j in range(len(tile_grids[i])):
                    if tile_grids[i][j] == tile:
                        grid_found = True
                        grid = tile_grids[i]
                        break
        
        for other_tile in curr_val_dict.keys():
            if(other_tile != tile):
                # if other_tile in same row as tile
                if other_tile[0] == tile[0]:
                    dependency_dict[tile].append(other_tile)
                 # if other_tile in same col as tile
                elif other_tile[1] == tile[1]:
                    dependency_dict[tile].append(other_tile)
                 # if other_tile in same grid as tile
                elif other_tile in grid:
                    dependency_dict[tile].append(other_tile)
    
    return dependency_dict

if __name__ == '__main__':    
    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    
    line = sys.argv[1]

    # Parse boards to dict representation, scanning board L to R, Up to Down
    board = { ROW[r] + COL[c]: int(line[9*r+c])
              for r in range(9) for c in range(9)}

    # Print starting board. TODO: Comment this out when timing runs.
    print_board(board)

    # Solve with backtracking
    solved_board = backtracking(board)

    # Print solved board. TODO: Comment this out when timing runs.
    print_board(solved_board)

    # Write board to file
    outfile.write(board_to_string(solved_board))
    outfile.write('\n')
    outfile.close()