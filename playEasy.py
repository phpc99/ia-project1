# Here is the play logic for the game such as the board state, board movement, etc...
import pygame
import numpy as np
from ia import *

def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

class PlayEasy():

    def __init__(self, level, SCREEN):
        self.current_level = level
        self.board_size = 4
        self.board_color = (233, 236, 239)  # Light square color
        self.piece_color = (255, 2, 2)  # Red square
        self.square_size = 60
        self.start_x = 100
        self.static_smaller_board = np.array([
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ], dtype=int)
        self.start_y = (SCREEN.get_height() - (self.board_size * self.square_size)) // 2
        if (level == 1):
            self.level_layout = np.array([ 
                        [0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 1, 0],
                        [0, 0, 1, 0],
            ])
            self.current_layout = self.level_layout
        elif (level == 2):
            self.level_layout = np.array([
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
            ])
            self.current_layout = self.level_layout
        elif (level == 3):
            self.level_layout = np.array([
                    [1, 0, 0, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 0, 0, 1],
            ])
            self.current_layout = self.level_layout
        self.start_time = pygame.time.get_ticks()  # Record the starting time in milliseconds
        self.timer_font = pygame.font.Font("assets/font.ttf", 18)  # Adjust the font size as needed
        self.movement_counter = 0  # Initialize the movement counter

    
    def draw_board(self, SCREEN):
       
        # Calculation of middle of the board
    
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Determine the square color
                if self.current_layout[row][col] == 1:
                    color = self.piece_color
                else:
                    color = self.board_color

                # Draw the square
                pygame.draw.rect(SCREEN, color, pygame.Rect(self.start_x + col * self.square_size, self.start_y + row * self.square_size, self.square_size, self.square_size))
    
        # Draw the grid lines after the squares
        for row in range(self.board_size+1):
            # Draw horizontal lines
            pygame.draw.line(SCREEN, (0,0,0), (self.start_x , self.start_y + row * self.square_size), (self.start_x + self.board_size * self.square_size, self.start_y + row * self.square_size))
        for col in range(self.board_size+1):
            # Draw vertical lines
            pygame.draw.line(SCREEN, (0,0,0), (self.start_x + col * self.square_size, self.start_y), (self.start_x + col * self.square_size, self.start_y + self.board_size * self.square_size))    

        # Define the arrow size and the number of arrows per side
        arrow_size = 30
        arrows_per_side = 4

        # Calculate the spacing between arrows
        #spacing = board_size * self.square_size / (arrows_per_side - 1)
        spacing = 60

        # Define the arrow buttons
        arrow_buttons = {}

        # Generate the positions for the left and right arrows
        for i in range(arrows_per_side):
            y = self.start_y+15 + i * spacing 
            arrow_buttons[f'right_{i}'] = pygame.Rect(self.start_x - arrow_size, y, arrow_size, arrow_size)
            arrow_buttons[f'left_{i}'] = pygame.Rect(self.start_x + self.board_size * self.square_size, y, arrow_size, arrow_size)

        # Generate the positions for the up and down arrows
        for i in range(arrows_per_side):
            x = self.start_x+15 + i * spacing
            arrow_buttons[f'down_{i}'] = pygame.Rect(x, self.start_y - arrow_size, arrow_size, arrow_size)
            arrow_buttons[f'up_{i}'] = pygame.Rect(x, self.start_y + self.board_size * self.square_size, arrow_size, arrow_size)

        # Draw the arrow buttons
        for direction, rect in arrow_buttons.items():
            pygame.draw.rect(SCREEN, (255, 255, 255), rect)

        elapsed_time = pygame.time.get_ticks() - self.start_time
        seconds = int(elapsed_time / 1000)  # Convert milliseconds to seconds
        timer_text = self.timer_font.render(f"Time: {seconds}s", True, (255, 255, 255))
        SCREEN.blit(timer_text, (900, 90))
        
        movement_text = self.timer_font.render(f"Moves: {self.movement_counter}", True, (255, 255, 255))
        SCREEN.blit(movement_text, (900, 140))

        # Load arrow image and resize it
        arrowPointDown_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointDown_image = pygame.transform.scale(pygame.image.load("assets/arrowPointDown.png"), (arrow_size, arrow_size))
        arrowPointUp_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointUp_image = pygame.transform.scale(pygame.image.load("assets/arrowPointUp.png"), (arrow_size, arrow_size))
        arrowPointRight_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointRight_image = pygame.transform.scale(pygame.image.load("assets/arrowPointRight.png"), (arrow_size, arrow_size))
        arrowPointLeft_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointLeft_image = pygame.transform.scale(pygame.image.load("assets/arrowPointLeft.png"), (arrow_size, arrow_size))

        # Draw a line of arrows at the top
        for col in range(self.board_size):
            row = 0
            rect = pygame.Rect(
                (self.start_x+15) + col * self.square_size,
                self.start_y - arrow_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointDown_image, rect)

        # Draw a line of arrows at the bottom
        for col in range(self.board_size):
            row = self.board_size - 1
            rect = pygame.Rect(
                (self.start_x+15) + col * self.square_size,
                self.start_y + self.board_size * self.square_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointUp_image, rect)

        # Draw a line of arrows on the left
        for row in range(self.board_size):
            col = 0
            rect = pygame.Rect(
                self.start_x - arrow_size,
                (self.start_y+15) + row * self.square_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointRight_image, rect)

        # Draw a line of arrows on the right
        for row in range(self.board_size):
            col = self.board_size - 1
            rect = pygame.Rect(
                self.start_x + self.board_size * self.square_size,
                (self.start_y+15) + row * self.square_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointLeft_image, rect)

        return arrow_buttons

    def check_win(self, SCREEN):
        if (np.array_equal(self.current_layout,self.static_smaller_board)):
            return True
        return False
    
    def draw_smaller_board(self, SCREEN):
        # Additional space to the right
        additional_space = 100

        # Offset to move the smaller board down
        offset_y = 250  # Adjust this value as needed

        # Calculate starting x-coordinate for the smaller board
        smaller_board_start_x = 850

        # Draw the static smaller board with a size reduction
        smaller_square_size = 30
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.static_smaller_board[row][col] == 1 and self.piece_color or self.board_color
                pygame.draw.rect(
                    SCREEN,
                    color,
                    pygame.Rect(
                        smaller_board_start_x + col * smaller_square_size,
                        self.start_y + row * smaller_square_size + offset_y,  # Move the smaller board down
                        smaller_square_size,
                        smaller_square_size,
                    ),
                )

        # Draw grid lines for the static smaller board
        for row in range(self.board_size + 1):
            pygame.draw.line(
                SCREEN,
                (0, 0, 0),
                (
                    smaller_board_start_x,
                    self.start_y + row * smaller_square_size + offset_y,  # Move the grid lines down
                ),
                (
                    smaller_board_start_x + self.board_size * smaller_square_size,
                    self.start_y + row * smaller_square_size + offset_y,  # Move the grid lines down
                ),
            )
        for col in range(self.board_size + 1):
            pygame.draw.line(
                SCREEN,
                (0, 0, 0),
                (
                    smaller_board_start_x + col * smaller_square_size,
                    self.start_y + offset_y,  # Move the grid lines down
                ),
                (
                    smaller_board_start_x + col * smaller_square_size,
                    self.start_y + self.board_size * smaller_square_size + offset_y,  # Move the grid lines down
                ),
            )

    def move_piece(self,arrow,SCREEN):
    
        # Extract the direction and index from the arrow pressed
        direction, index = arrow.split('_')
        index = int(index)
        print(direction)

        # Shift the specified row or column based on the direction
        if direction in ['left', 'right']:
            self.current_layout[index] = np.roll(self.current_layout[index], shift=1) if direction == 'right' else np.roll(self.current_layout[index], shift=-1)
        elif direction in ['up', 'down']:
            self.current_layout[:, index] = np.roll(self.current_layout[:, index], shift=-1) if direction == 'up' else np.roll(self.current_layout[:, index], shift=1)

        # Update the movement counter
        self.movement_counter += 1

        # Print the current layout
        print(self.current_layout)

    def get_movement_counter(self):
        return self.movement_counter

    def get_elapsed_time(self):
        return pygame.time.get_ticks() - self.start_time

    ####Algoritmo de busca para encontrar o próximo melhor movimento
    def evaluate_board(self, layout):
        #Contar o número de peças fora do lugar em relação ao estado objetivo
        return np.sum(layout != self.static_smaller_board)
    
    def search_next_move(self):
        best_move = None
        best_score = float('inf')  # Inicializa com infinito, buscando minimizar
        for direction in ['left', 'right', 'up', 'down']:
            for index in range(self.board_size):
                temp_layout = self.current_layout.copy()
                if direction in ['left', 'right']:
                    temp_layout[index] = np.roll(temp_layout[index], shift=1 if direction == 'right' else -1)
                elif direction in ['up', 'down']:
                    temp_layout[:, index] = np.roll(temp_layout[:, index], shift=-1 if direction == 'up' else 1)
                score = self.evaluate_board(temp_layout)
                if score < best_score:
                    best_score = score
                    best_move = direction + '_' + str(index)
        return best_move
    
    def get_hint(self):
        #algoritmo de busca para encontrar o próximo melhor movimento
        next_move = self.search_next_move()
        return next_move
    
    def computer_play_IDDFS(self):
        return IDDFS(self.current_layout, self.static_smaller_board, 10)
 
    def computer_play_AStar(self):
        return A_star(AI(self.current_layout, self.static_smaller_board))
    
    def computer_play_IDAStar(self):
        return IDA_star(AI(self.current_layout, self.static_smaller_board))
    
class PlayEasyAI():

    def __init__(self, level, SCREEN):
        self.current_level = level
        self.board_size = 4
        self.board_color = (233, 236, 239)  # Light square color
        self.piece_color = (255, 2, 2)  # Red square
        self.square_size = 60
        self.start_x = 100
        self.static_smaller_board = np.array([
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ], dtype=int)
        self.start_y = (SCREEN.get_height() - (self.board_size * self.square_size)) // 2
        if (level == 1):
            self.level_layout = np.array([ 
                        [0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 1, 0],
                        [0, 0, 1, 0],
            ])
            self.current_layout = self.level_layout
        elif (level == 2):
            self.level_layout = np.array([
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
            ])
            self.current_layout = self.level_layout
        elif (level == 3):
            self.level_layout = np.array([
                    [1, 0, 0, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 0, 0, 1],
            ])
            self.current_layout = self.level_layout
        self.timer_font = pygame.font.Font("assets/font.ttf", 18)  # Adjust the font size as needed
    
    def draw_board(self, SCREEN):
       
        # Calculation of middle of the board
    
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Determine the square color
                if self.current_layout[row][col] == 1:
                    color = self.piece_color
                else:
                    color = self.board_color

                # Draw the square
                pygame.draw.rect(SCREEN, color, pygame.Rect(self.start_x + col * self.square_size, self.start_y + row * self.square_size, self.square_size, self.square_size))
    
        # Draw the grid lines after the squares
        for row in range(self.board_size+1):
            # Draw horizontal lines
            pygame.draw.line(SCREEN, (0,0,0), (self.start_x , self.start_y + row * self.square_size), (self.start_x + self.board_size * self.square_size, self.start_y + row * self.square_size))
        for col in range(self.board_size+1):
            # Draw vertical lines
            pygame.draw.line(SCREEN, (0,0,0), (self.start_x + col * self.square_size, self.start_y), (self.start_x + col * self.square_size, self.start_y + self.board_size * self.square_size))    

        # Define the arrow size and the number of arrows per side
        arrow_size = 30
        arrows_per_side = 4

        # Calculate the spacing between arrows
        #spacing = board_size * self.square_size / (arrows_per_side - 1)
        spacing = 60

        # Define the arrow buttons
        arrow_buttons = {}

        # Generate the positions for the left and right arrows
        for i in range(arrows_per_side):
            y = self.start_y+15 + i * spacing 
            arrow_buttons[f'right_{i}'] = pygame.Rect(self.start_x - arrow_size, y, arrow_size, arrow_size)
            arrow_buttons[f'left_{i}'] = pygame.Rect(self.start_x + self.board_size * self.square_size, y, arrow_size, arrow_size)

        # Generate the positions for the up and down arrows
        for i in range(arrows_per_side):
            x = self.start_x+15 + i * spacing
            arrow_buttons[f'down_{i}'] = pygame.Rect(x, self.start_y - arrow_size, arrow_size, arrow_size)
            arrow_buttons[f'up_{i}'] = pygame.Rect(x, self.start_y + self.board_size * self.square_size, arrow_size, arrow_size)

        # Draw the arrow buttons
        for direction, rect in arrow_buttons.items():
            pygame.draw.rect(SCREEN, (255, 255, 255), rect)

        # Load arrow image and resize it
        arrowPointDown_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointDown_image = pygame.transform.scale(pygame.image.load("assets/arrowPointDown.png"), (arrow_size, arrow_size))
        arrowPointUp_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointUp_image = pygame.transform.scale(pygame.image.load("assets/arrowPointUp.png"), (arrow_size, arrow_size))
        arrowPointRight_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointRight_image = pygame.transform.scale(pygame.image.load("assets/arrowPointRight.png"), (arrow_size, arrow_size))
        arrowPointLeft_size = int(self.square_size * 0.5)  # Adjust the size as needed
        arrowPointLeft_image = pygame.transform.scale(pygame.image.load("assets/arrowPointLeft.png"), (arrow_size, arrow_size))

        # Draw a line of arrows at the top
        for col in range(self.board_size):
            row = 0
            rect = pygame.Rect(
                (self.start_x+15) + col * self.square_size,
                self.start_y - arrow_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointDown_image, rect)

        # Draw a line of arrows at the bottom
        for col in range(self.board_size):
            row = self.board_size - 1
            rect = pygame.Rect(
                (self.start_x+15) + col * self.square_size,
                self.start_y + self.board_size * self.square_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointUp_image, rect)

        # Draw a line of arrows on the left
        for row in range(self.board_size):
            col = 0
            rect = pygame.Rect(
                self.start_x - arrow_size,
                (self.start_y+15) + row * self.square_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointRight_image, rect)

        # Draw a line of arrows on the right
        for row in range(self.board_size):
            col = self.board_size - 1
            rect = pygame.Rect(
                self.start_x + self.board_size * self.square_size,
                (self.start_y+15) + row * self.square_size,
                arrow_size,
                arrow_size,
            )
            SCREEN.blit(arrowPointLeft_image, rect)

        return arrow_buttons

    def check_win(self, SCREEN):
        if (np.array_equal(self.current_layout,self.static_smaller_board)):
            return True
        return False
    
    def draw_smaller_board(self, SCREEN):
        # Additional space to the right
        additional_space = 100

        # Offset to move the smaller board down
        offset_y = 250  # Adjust this value as needed

        # Calculate starting x-coordinate for the smaller board
        smaller_board_start_x = 850

        # Draw the static smaller board with a size reduction
        smaller_square_size = 30
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.static_smaller_board[row][col] == 1 and self.piece_color or self.board_color
                pygame.draw.rect(
                    SCREEN,
                    color,
                    pygame.Rect(
                        smaller_board_start_x + col * smaller_square_size,
                        self.start_y + row * smaller_square_size + offset_y,  # Move the smaller board down
                        smaller_square_size,
                        smaller_square_size,
                    ),
                )

        # Draw grid lines for the static smaller board
        for row in range(self.board_size + 1):
            pygame.draw.line(
                SCREEN,
                (0, 0, 0),
                (
                    smaller_board_start_x,
                    self.start_y + row * smaller_square_size + offset_y,  # Move the grid lines down
                ),
                (
                    smaller_board_start_x + self.board_size * smaller_square_size,
                    self.start_y + row * smaller_square_size + offset_y,  # Move the grid lines down
                ),
            )
        for col in range(self.board_size + 1):
            pygame.draw.line(
                SCREEN,
                (0, 0, 0),
                (
                    smaller_board_start_x + col * smaller_square_size,
                    self.start_y + offset_y,  # Move the grid lines down
                ),
                (
                    smaller_board_start_x + col * smaller_square_size,
                    self.start_y + self.board_size * smaller_square_size + offset_y,  # Move the grid lines down
                ),
            )

    def move_piece(self,arrow,SCREEN):
    
        # Extract the direction and index from the arrow pressed
        direction, index = arrow.split('_')
        index = int(index)
        print(direction)

        # Shift the specified row or column based on the direction
        if direction in ['left', 'right']:
            self.current_layout[index] = np.roll(self.current_layout[index], shift=1) if direction == 'right' else np.roll(self.current_layout[index], shift=-1)
        elif direction in ['up', 'down']:
            self.current_layout[:, index] = np.roll(self.current_layout[:, index], shift=-1) if direction == 'up' else np.roll(self.current_layout[:, index], shift=1)

        # Print the current layout
        print(self.current_layout)

    ####Algoritmo de busca para encontrar o próximo melhor movimento
    def evaluate_board(self, layout):
        #Contar o número de peças fora do lugar em relação ao estado objetivo
        return np.sum(layout != self.static_smaller_board)
    
    def search_next_move(self):
        best_move = None
        best_score = float('inf')  # Inicializa com infinito, buscando minimizar
        for direction in ['left', 'right', 'up', 'down']:
            for index in range(self.board_size):
                temp_layout = self.current_layout.copy()
                if direction in ['left', 'right']:
                    temp_layout[index] = np.roll(temp_layout[index], shift=1 if direction == 'right' else -1)
                elif direction in ['up', 'down']:
                    temp_layout[:, index] = np.roll(temp_layout[:, index], shift=-1 if direction == 'up' else 1)
                score = self.evaluate_board(temp_layout)
                if score < best_score:
                    best_score = score
                    best_move = direction + '_' + str(index)
        return best_move
    
    def get_hint(self):
        #algoritmo de busca para encontrar o próximo melhor movimento
        next_move = self.search_next_move()
        return next_move
    
    def computer_play_IDDFS(self):
        return IDDFS(self.current_layout, self.static_smaller_board, 10)
 
    def computer_play_AStar(self):
        return A_star(AI(self.current_layout, self.static_smaller_board))
    
    def computer_play_IDAStar(self):
        return IDA_star(AI(self.current_layout, self.static_smaller_board))