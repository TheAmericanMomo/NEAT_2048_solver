import pygame
import random
import math
class Board:

    """
    listNums is a short[4][4] where the first number is the row index and the
     * second is the col index [0][0] [0][1] [0][2] [0][3] [1][0] [1][1] [1][2]
     * [1][3] [2][0] [2][1] [2][2] [2][3] [3][0] [3][1] [3][2] [3][3]
     * 
     * this array can also be represented as indexes { 0, 1, 2, 3, 4, 5, 6, 7,
     * 8, 9, 10, 11, 12, 13, 14, 15 } row idx = x//4 col idx = x % 4
    """
    BOARDER_SIZE = 5
    def __init__(self, listNums, window_width, window_height, header_size, score):
        self.listNums = listNums
        self.score = score
        self.unchangedScore = score
        self.window_width = window_width
        self.window_height = window_height

        self.zeros_in_bottom_row = False

        self.box_WIDTH = window_width // 4 
        self.box_HEIGHT = window_height // 4

        self.NUMBER_FONT = pygame.font.SysFont("arial", 20)

        self.header_size = header_size


    def draw(self, window):
        for x in range(4):
            for y in range(4):
                if(self.listNums[y][x] != 0):
                    width = x*self.box_WIDTH
                    height = y*self.box_HEIGHT + self.header_size
                    pygame.draw.rect(
                        window, (255, 255, 255), (width + self.BOARDER_SIZE, height + self.BOARDER_SIZE, 
                            self.box_WIDTH - 2* self.BOARDER_SIZE, self.box_HEIGHT - 2* self.BOARDER_SIZE))

                    text = self.NUMBER_FONT.render(str(self.listNums[y][x]), True, (0, 0, 0))

                    halfWidth = - text.get_width()//2
                    window.blit(text, (width + self.BOARDER_SIZE + self.box_WIDTH//2 - halfWidth, height + self.BOARDER_SIZE + self.box_HEIGHT//2 - halfWidth))

    """
    the following move functions perform the moves on the board
    """
    def move_left(self):
        change_performed = False

        for row in range(4):
            idx = 0
            for col in range(4):
                board_val = self.listNums[row][col]
                val_at_idx = self.listNums[row][idx]

                if board_val != 0:
                    if val_at_idx == 0:
                        self.listNums[row][idx] = board_val
                        self.listNums[row][col] = 0
                        change_performed = True

                    elif val_at_idx == board_val:
                        if idx != col:
                            self.listNums[row][idx] *= 2
                            self.score += self.listNums[row][idx]
                            self.unchangedScore += self.listNums[row][idx]
                            self.listNums[row][col] = 0
                            change_performed = True
                            idx += 1

                    elif val_at_idx != board_val:
                        idx += 1
                        if idx != col:
                            self.listNums[row][idx] = board_val
                            self.listNums[row][col] = 0
                            change_performed = True
            
        return change_performed

    def move_right(self):
        change_performed = False

        for row in range(4):
            idx = 3
            for col in range(3,-1,-1):
                board_val = self.listNums[row][col]
                val_at_idx = self.listNums[row][idx]

                if board_val != 0:
                    if val_at_idx == 0:
                        self.listNums[row][idx] = board_val
                        self.listNums[row][col] = 0
                        change_performed = True

                    elif val_at_idx == board_val:
                        if idx != col:
                            self.listNums[row][idx] *= 2
                            self.score += self.listNums[row][idx]
                            self.unchangedScore += self.listNums[row][idx]
                            self.listNums[row][col] = 0
                            change_performed = True
                            idx -= 1

                    elif val_at_idx != board_val:
                        idx -= 1
                        if idx != col:
                            self.listNums[row][idx] = board_val
                            self.listNums[row][col] = 0
                            change_performed = True
            
        return change_performed

    def move_up(self):
        change_performed = False

        for col in range(4):
            idx = 0
            for row in range(4):
                board_val = self.listNums[row][col]
                val_at_idx = self.listNums[idx][col]

                if board_val != 0:
                    if val_at_idx == 0:
                        self.listNums[idx][col] = board_val
                        self.listNums[row][col] = 0
                        change_performed = True

                    elif val_at_idx == board_val:
                        if idx != row:
                            self.listNums[idx][col] *= 2
                            self.score += self.listNums[idx][col]
                            self.unchangedScore += self.listNums[idx][col]
                            self.listNums[row][col] = 0
                            change_performed = True
                            idx += 1

                    elif val_at_idx != board_val:
                        idx += 1
                        if idx != row:
                            self.listNums[idx][col] = board_val
                            self.listNums[row][col] = 0
                            change_performed = True
            
        return change_performed


    def move_down(self):
        change_performed = False

        for col in range(4):
            idx = 3
            for row in range(3, -1, -1):
                board_val = self.listNums[row][col]
                val_at_idx = self.listNums[idx][col]

                if board_val != 0:
                    if val_at_idx == 0:
                        self.listNums[idx][col] = board_val
                        self.listNums[row][col] = 0
                        change_performed = True

                    elif val_at_idx == board_val:
                        if idx != row:
                            self.listNums[idx][col] *= 2
                            self.score += self.listNums[idx][col]
                            self.unchangedScore += self.listNums[idx][col]
                            self.listNums[row][col] = 0
                            change_performed = True
                            idx -= 1

                    elif val_at_idx != board_val:
                        idx -= 1
                        if idx != row:
                            self.listNums[idx][col] = board_val
                            self.listNums[row][col] = 0
                            change_performed = True
            
        return change_performed

    def findEmptyIdxs(self):
        idxs = []
        for i in range(16):
            if self.listNums[i // 4][i % 4] == 0:
                idxs.append(i)
        return idxs

    """
    Spawns a new number on the board folowing the game's probability distribution

    2 is spawned with a 90% probability and 4 with a 10% proba
    
    """
    def spawn_new_number(self):
        emptyIdxs = self.findEmptyIdxs()

        if len(emptyIdxs) == 0:
         #   print("err: spawn_new_number called on a full board")
            return False
        
        randomIdx = emptyIdxs[random.randrange(len(emptyIdxs))]
        fourIfZero = random.randrange(10)

        if fourIfZero == 0:
            self.listNums[randomIdx // 4][randomIdx %4] = 4
        else:
            self.listNums[randomIdx // 4][randomIdx % 4] = 2

        return True

    def generate_initial_board(self):
        randomIdx = random.randrange(16)
        fourIfZero = random.randrange(10)

        if fourIfZero == 0:
            self.listNums[randomIdx // 4][randomIdx %4] = 4
        else:
            self.listNums[randomIdx // 4][randomIdx % 4] = 2

        secondIdx = randomIdx
        fourIfZero = random.randrange(10)
        while secondIdx == randomIdx:
            secondIdx = random.randrange(16)
        
        if fourIfZero == 0:
            self.listNums[secondIdx // 4][secondIdx %4] = 4
        else:
            self.listNums[secondIdx // 4][secondIdx % 4] = 2



    def reset(self):
        self.listNums = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.generate_initial_board()
        self.score = 0
        self.unchangedScore = 0

    """
    The four following functions return whether or not a board move is possible in that direction

    This is used as an input for the NN
    """
    def can_t_go_left(self):
        identicalNeighbors = False
        thereIsAZeroToTheLeft = False

        row = 0
        while row < 4 and (not identicalNeighbors) and not thereIsAZeroToTheLeft:
            identicalNeighbors = identicalNeighbors or (self.listNums[row][0] != 0 and (self.listNums[row][0] == self.listNums[row][1]))  or (self.listNums[row][1] != 0 and (self.listNums[row][1] == self.listNums[row][2])) or (self.listNums[row][2] != 0 and (self.listNums[row][2] == self.listNums[row][3]))

            zeroFound = False
            idx = 0
            while (not zeroFound) and idx < 4:
                zeroFound = (self.listNums[row][idx] == 0)
                idx += 1
            
            while idx < 4 and not thereIsAZeroToTheLeft:
                thereIsAZeroToTheLeft = (self.listNums[row][idx] != 0)
                idx += 1
            
            row += 1
        
        return not(identicalNeighbors or thereIsAZeroToTheLeft)
        
    def can_t_go_right(self):
        identicalNeighbors = False
        thereIsAZeroToTheRight = False

        row = 0
        while row < 4 and not identicalNeighbors and not thereIsAZeroToTheRight:
            identicalNeighbors = identicalNeighbors or (self.listNums[row][0] != 0 and (self.listNums[row][0] == self.listNums[row][1]))  or (self.listNums[row][1] != 0 and (self.listNums[row][1] == self.listNums[row][2])) or (self.listNums[row][2] != 0 and (self.listNums[row][2] == self.listNums[row][3]))
            zeroFound = False
            idx = 3
            while (not zeroFound) and idx > -1:
                zeroFound = (self.listNums[row][idx] == 0)
                idx -= 1
            
            while idx > -1 and not thereIsAZeroToTheRight:
                thereIsAZeroToTheRight = (self.listNums[row][idx] != 0)
                idx -= 1
            
            row += 1
        
        return not(identicalNeighbors or thereIsAZeroToTheRight)

    def can_t_go_up(self):
        identicalNeighbors = False
        thereIsAZeroToTheTop = False

        col = 0
        while col < 4 and (not identicalNeighbors) and not thereIsAZeroToTheTop:
            identicalNeighbors = identicalNeighbors or (self.listNums[0][col] != 0 and (self.listNums[0][col] == self.listNums[1][col]))  or (self.listNums[1][col] != 0 and (self.listNums[1][col] == self.listNums[2][col])) or (self.listNums[2][col] != 0 and (self.listNums[2][col] == self.listNums[3][col]))
            zeroFound = False
            idx = 0
            while (not zeroFound) and idx < 4:
                zeroFound = (self.listNums[idx][col] == 0)
                idx += 1
            
            while idx < 4 and not thereIsAZeroToTheTop:
                thereIsAZeroToTheTop = (self.listNums[idx][col] != 0)
                idx += 1
            col += 1
        
        return not(identicalNeighbors or thereIsAZeroToTheTop)

    def can_t_go_down(self):
        identicalNeighbors = False
        thereIsAZeroToTheBottom = False

        col = 0
        while col < 4 and (not identicalNeighbors) and not thereIsAZeroToTheBottom:
            identicalNeighbors = identicalNeighbors or (self.listNums[0][col] != 0 and (self.listNums[0][col] == self.listNums[1][col]))  or (self.listNums[1][col] != 0 and (self.listNums[1][col] == self.listNums[2][col])) or (self.listNums[2][col] != 0 and (self.listNums[2][col] == self.listNums[3][col]))
            zeroFound = False
            idx = 3
            while (not zeroFound) and idx > -1:
                zeroFound = (self.listNums[idx][col] == 0)
                idx -= 1
            
            while idx > -1 and not thereIsAZeroToTheBottom:
                thereIsAZeroToTheBottom = (self.listNums[idx][col] != 0)
                idx -= 1
            col += 1
        
        return not(identicalNeighbors or thereIsAZeroToTheBottom)

    """
    The following four functions are used for heuristics

    We want the AI to follow the basic strategy of puting the higher numbers near one corner

    From there, we want the mutation to discover new strategies.
    """
    #don't care about penalizing for the top row and the right most column

    #may not be good to penalize monotonicity of higher rows, because the ai might not want to shift to join
    def penalize_non_monotonicity(self):
        acc = 0
    #    row1IsMono = self.listNums[1][0] >= self.listNums[1][1] and self.listNums[1][1] >= self.listNums[1][2] and self.listNums[1][2] >= self.listNums[1][3]
    #    row2IsMono = self.listNums[2][0] >= self.listNums[2][1] and self.listNums[2][1] >= self.listNums[2][2] and self.listNums[2][2] >= self.listNums[2][3]
        row3IsMono = self.listNums[3][0] >= self.listNums[3][1] and self.listNums[3][1] >= self.listNums[3][2] and self.listNums[3][2] >= self.listNums[3][3]

        col0IsMono = self.listNums[0][0] <= self.listNums[1][0] and self.listNums[1][0] <= self.listNums[2][0] and self.listNums[2][0] <= self.listNums[3][0]
        col1IsMono = self.listNums[0][1] <= self.listNums[1][1] and self.listNums[1][1] <= self.listNums[2][1] and self.listNums[2][1] <= self.listNums[3][1]
        col2IsMono = self.listNums[0][2] <= self.listNums[1][2] and self.listNums[1][2] <= self.listNums[2][2] and self.listNums[2][2] <= self.listNums[3][2]
        col3IsMono = self.listNums[0][3] <= self.listNums[1][3] and self.listNums[1][3] <= self.listNums[2][3] and self.listNums[2][3] <= self.listNums[3][3]

        if(not row3IsMono):
            acc += 0.2
        
    #    if(not row2IsMono):
    #        acc += 0.01

    #    if(not row1IsMono):
    #        acc += 0.005
        
        if(not col0IsMono):
            acc += 0.01
        
        if(not col1IsMono):
            acc += 0.01
        
        if not col2IsMono:
            acc += 0.01
        
        if not col3IsMono:
            acc += 0.01

        self.score -= abs(self.score) * acc


    ##penalizes iff there are zeros twice in a row!!! Thus, the ai doesn't lose points for merging 
    #the bottom row
    def penalize_zeros_in_bottom_row(self):
        if self.zeros_in_bottom_row and (self.listNums[3][0] == 0 or self.listNums[3][1] == 0 or self.listNums[3][2] == 0 or self.listNums[3][3] == 0):
            self.score -= abs(self.score) * 0.05
        
        elif self.zeros_in_bottom_row:
            self.zeros_in_bottom_row = False

        elif (self.listNums[3][0] == 0 or self.listNums[3][1] == 0 or self.listNums[3][2] == 0 or self.listNums[3][3] == 0):
            self.zeros_in_bottom_row = True

    def penalize_invalid_move(self):
        self.score /= 4
        #self.score = 0

    def give_points_for_few_empty_spaces(self):
        num = 0
        for i in range(16):
            if self.listNums[i // 4][i % 4] == 0:
                num += 1
        
        self.score *= (1+0.001*num)

    """
    This helper function returns the board tiles as their log so that the NN doesn't 
    get overwhelmed by the higher values
    
    """
    def get_log_list(self):
        list = []
        for i in range(4):
            list.append([])
            for j in range(4):
                if self.listNums[i][j] == 0:
                    list[i].append(-1)
                else:
                    list[i].append(math.log2(self.listNums[i][j]))
        return list


