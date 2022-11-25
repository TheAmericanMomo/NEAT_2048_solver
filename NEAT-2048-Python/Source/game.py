from .board import Board
import pygame
import random
pygame.init()


class GameInformation:
    def __init__(self, score):
        self.score = score


class Game:
    """
    To use this class simply initialize and instance and call the .loop() method
    inside of a pygame event loop (i.e while loop). Inside of your event loop
    you can call the .draw() and .move_paddle() methods according to your use case.
    Use the information returned from .loop() to determine when to end the game by calling
    .reset().
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self, listNums, window, window_width, window_height, header_size):
        self.window_width = window_width
        self.window_height = window_height
        self.box_width = window_width // 4
        self.box_height = window_height // 4
        self.header_size = header_size

        self.board = Board(
            listNums, window_width, window_height, header_size, 0)

        self.window = window

    def _draw_score(self):
        score_text = self.SCORE_FONT.render(
            f"{self.board.score}", 1, self.RED)
        
        self.window.blit(score_text, (self.window_width //
                                           2 - score_text.get_width()//2, 20))

    def draw(self):
        self.window.fill(self.BLACK)

        self._draw_score()
        self.board.draw(self.window)

    def move(self, move, can_t_go_left, can_t_go_up, can_t_go_right, can_t_go_down):
        """
        Move the board to the left, right, bottom or top.

        move is an integer between 0 and 3, [0:Left,1:Right,2:Up,3:Down]

        :returns: boolean indicating if movement is valid. 
                  Movement is invalid if it is impossible to move
                  in that direction
        """
        exists_a_valid_move = (not can_t_go_left) or (not can_t_go_right) or (not can_t_go_down) or (not can_t_go_up)

        if move == 0:
            if can_t_go_left and exists_a_valid_move:
                self.board.penalize_invalid_move()
            return self.board.move_left()
        elif move == 1:
            if can_t_go_down and exists_a_valid_move:
                self.board.penalize_invalid_move()
            return self.board.move_down()
        elif move == 2:
            if can_t_go_right and exists_a_valid_move:
                self.board.penalize_invalid_move()
            return self.board.move_right()
        else:
            if can_t_go_up and exists_a_valid_move:
                self.board.penalize_invalid_move()
            return self.board.move_up()

    def loop(self): 
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        # if the move was valid, i.e. it resulted in a change, 
        # i.e. the board has at least one empty space

        self.board.penalize_non_monotonicity()
        self.board.penalize_zeros_in_bottom_row()
        self.board.give_points_for_few_empty_spaces()

        self.board.spawn_new_number()
        
        game_info = GameInformation(self.board.score)

        return game_info

    def reset(self):
        """Resets the entire game."""
        self.board.reset()

