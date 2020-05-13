import time
import math
import numpy as np
from BaseAI import BaseAI

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class IntelligentAgent(BaseAI):
    def __init__(self):
        self.time_lim = 0.15
        self.max_depth = 2
    
    def getMove(self, grid):
        depth_lim = 0
        start_time = time.process_time()
        (foundMove, foundUtility) = self.maximize(grid, depth_lim, (-1*math.inf), math.inf, start_time)
        return foundMove

    def maximize(self, grid, depth_lim, alpha, beta, start_time):
        
        # get children of the node (get available moves for the player)
        moveset = grid.getAvailableMoves()
        
        if (time.process_time() - start_time > 0.15):
            return (None, self.evaluate(grid))
        elif depth_lim >= self.max_depth:
            return (None, self.evaluate(grid))
        elif not moveset:
            return (None, self.evaluate(grid))
        '''
        (maxChild, maxUtility) = (Null, -infinity)
        '''        
        (maxMove, maxUtility) = (None, (-1*math.inf))
        
        '''
        for child in state.children():
            (__, utility) = chance(grid, depth, alpha, beta)
            
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return (maxChild, maxUtility)
                
        '''
        for move,child_grid in moveset:
            child_clone = child_grid.clone()
            # determine utility (using clone of child_grid which is the moved board)
            utility = self.chance(child_clone, depth_lim, alpha, beta, start_time)
            
            if utility > maxUtility:
                (maxMove, maxUtility) = (move, utility)
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        
        return (maxMove, maxUtility)
    
    def chance(self, grid, depth_lim, alpha, beta, start_time):
        
        (two_tile, two_utility) = self.minimize(grid, depth_lim, alpha, beta, 2, start_time)
        (four_tile, four_utility) = self.minimize (grid, depth_lim, alpha, beta, 4, start_time)
        
        return .9 * two_utility + .1 * four_utility
    
    def minimize(self, grid, depth_lim, alpha, beta, tile_val, start_time):
        if (time.process_time() - start_time > 0.15):
            return (None, self.evaluate(grid))
        
        '''
        (minChild, minUtility) = (null, infinity)
        '''
        (minTile, minUtility) = (None, math.inf)
        
        open_tiles = grid.getAvailableCells()
        
        '''
        for child in state.children():
            (__, utility) = maximize(child, alpha, beta)
            
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility
        '''
        for tile in open_tiles:
            # insert tile (from computer) with value in tile_val
            grid_clone = grid.clone()
            grid_clone.insertTile(tile, tile_val)
            
            # determine utility
            (currTile, utility) = self.maximize(grid_clone, depth_lim+1, alpha, beta, start_time)
            if utility < minUtility:
                (minTile, minUtility) = (tile, utility)
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility

        '''
        return (minChild, minUtility)
        '''
        return (minTile, minUtility)
    
    def available_cell_count(self, grid):
        # return the number of available cells 
        return len(grid.getAvailableCells())
 
    def snake_shape_weight_matrices(self, grid):
        snake_matrix = np.array([[4**15, 4**14, 4**13, 4**12],
                        [4**8, 4**9, 4**10, 4**11],
                        [4**7, 4**6, 4**5, 4**4], 
                        [4**0, 4**1, 4**2, 4**3]], np.int32)
    
        grid_map = np.array(grid.map)
        
        return np.sum(np.dot(snake_matrix, grid_map))
    
    def max_tile(self, grid):
        return grid.getMaxTile()
    
    def sum_of_tiles(self, grid):
        total = 0
        for x in range(grid.size):
            for y in range(grid.size):
                # If Current Cell is Filled
                if grid.map[x][y]:
                    total += grid.getCellValue((x,y))
        return total

    def max_tile_in_corner(self, grid):
        max_tile_location = (0,0)
        max_tile_val = 0
        for x in range(grid.size):
            for y in range(grid.size):
                curr_val = grid.getCellValue((x,y))
                if curr_val > max_tile_val:
                   max_tile_val = curr_val
                   max_tile_location = (x,y)
        if (max_tile_location == (0,0) or max_tile_location == (0,3) or max_tile_location == (3,0) or max_tile_location == (3,3)):
            return 10
        return 0
    
    # Num of potential merges           
    def smoothness(self, grid, dirs=vecIndex):
        # Init Moves to be Checked        
        checkingMoves = set(dirs)
        
        count = 0

        # move through grid map
        for x in range(grid.size):
            for y in range(grid.size):

                # If Current Cell is Filled
                if grid.map[x][y]:

                    # Look Ajacent Cell Value
                    for i in checkingMoves:
                        move = directionVectors[i]

                        adjCellValue = grid.getCellValue((x + move[0], y + move[1]))

                        # If Value of the Adjacent Cell is the Same
                        if adjCellValue == grid.map[x][y]:
                            count+=1
        return count        
        
    
    def evaluate(self, grid):
        return (2**14)*self.smoothness(grid) + self.snake_shape_weight_matrices(grid) + (2**14)*self.available_cell_count(grid)
