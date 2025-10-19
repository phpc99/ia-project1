import pygame, sys
from button import Button
from play import Play
from play import PlayAI
from playEasy import PlayEasy
from playEasy import PlayEasyAI

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720)) 
#SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play_easy_mode():
    level = 1
    time_at_victory = 0  # Initialize time at victory
    play = PlayEasy(level, SCREEN)
    
    # Initialize buttons outside of the loop
    PLAY_BACK = Button(image=None, pos=(640, 700), 
                       text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
  
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if play.check_win(SCREEN):
            
            if time_at_victory == 0:
                time_at_victory = play.get_elapsed_time()  # Record time at victory

            # Display win message
            SCREEN.fill("black")
            WIN_TEXT = get_font(45).render("You won!!!!", True, "White")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(WIN_TEXT, WIN_RECT)

            # Get the number of moves from the play instance
            movement_counter = play.get_movement_counter()
            MOVE_TEXT = get_font(30).render(f"Number of Moves: {movement_counter}", True, "White")
            MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
            SCREEN.blit(MOVE_TEXT, MOVE_RECT)

            # Get the time spent to achieve victory
            TIME_TEXT = get_font(30).render(f"Time: {time_at_victory // 1000}s", True, "White")
            TIME_RECT = TIME_TEXT.get_rect(center=(640, 380))
            SCREEN.blit(TIME_TEXT, TIME_RECT)

            # Display buttons
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            # Check if the button is initialized before accessing it
            if 'PLAY_NEXT_LEVEL' in locals():
                PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
                PLAY_NEXT_LEVEL.update(SCREEN)

        else:
            # Display game board
            SCREEN.blit(BG, (0, 0))
            play.draw_smaller_board(SCREEN)
            arrows = play.draw_board(SCREEN)

            # Display back button
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)
      
            # Initialize the NEXT LEVEL button only if it's not initialized
            if 'PLAY_NEXT_LEVEL' not in locals():
                PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                         text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
                
            # Render current level on the screen
            LEVEL_TEXT = get_font(30).render(f"Level: {level}", True, "White")
            LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 25))
            SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if 'PLAY_NEXT_LEVEL' in locals() and PLAY_NEXT_LEVEL.checkForInput(PLAY_MOUSE_POS):
                    # Update level and game instance
                    if level < 3:
                        level += 1
                    else:
                        level = 3
                        main_menu()
                    time_at_victory = 0  # Reset time at victory to zero
                    play = PlayEasy(level, SCREEN)
                for direction, rect in arrows.items():
                    if rect.collidepoint(mouse_pos):
                        print(f"The {direction} arrow button was clicked.")
                        play.move_piece(direction, SCREEN)

        pygame.display.update()

def play():
    current_level = 1  # Initialize the current level outside the play function
    PLAY_NEXT_LEVEL = None  # Initialize PLAY_NEXT_LEVEL outside the loop
    time_at_victory = 0  # Initialize time at victory
    play = Play(current_level, SCREEN)
  
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if play.check_win(SCREEN):

            if time_at_victory == 0:
                time_at_victory = play.get_elapsed_time()  # Record time at victory

            SCREEN.fill("black")
            WIN_TEXT = get_font(45).render("You won!!!!", True, "White")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(WIN_TEXT, WIN_RECT)

            PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                        text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
            PLAY_NEXT_LEVEL.update(SCREEN)

            # Get the number of moves from the play instance
            movement_counter = play.get_movement_counter()
            MOVE_TEXT = get_font(30).render(f"Number of Moves: {movement_counter}", True, "White")
            MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
            SCREEN.blit(MOVE_TEXT, MOVE_RECT)

            # Get the time spent to achieve victory
            TIME_TEXT = get_font(30).render(f"Time: {time_at_victory // 1000}s", True, "White")
            TIME_RECT = TIME_TEXT.get_rect(center=(640, 380))
            SCREEN.blit(TIME_TEXT, TIME_RECT)

            PLAY_BACK = Button(image=None, pos=(640, 700), 
                                        text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

        else:
            SCREEN.blit(BG, (0, 0))
            
            play.draw_smaller_board(SCREEN)
            arrows = play.draw_board(SCREEN)
            PLAY_BACK = Button(image=None, pos=(640, 700), 
                                        text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            # Render current level on the screen
            LEVEL_TEXT = get_font(30).render(f"Level: {current_level}", True, "White")
            LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 25))
            SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
      
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif PLAY_NEXT_LEVEL is not None and PLAY_NEXT_LEVEL.checkForInput(PLAY_MOUSE_POS):
                    # Update level and game instance
                    if current_level < 3:
                        current_level += 1
                    else:
                        current_level = 3
                        main_menu()

                    time_at_victory = 0  # Reset time at victory to zero
                    play = Play(current_level, SCREEN)  # Update to the next level
                else:
                    for direction, rect in arrows.items():
                        if rect.collidepoint(mouse_pos):
                            print(f"The {direction} arrow button was clicked.")
                            play.move_piece(direction, SCREEN)

        pygame.display.update()

def ia_IDDFS():
    level = 1
    play = PlayAI(level, SCREEN)

    # Font for "Click to start" text
    font = get_font(24)
    click_to_start_text = font.render("-> Click anywhere to start the AI", True, (255,255,255))
    click_to_start_rect = click_to_start_text.get_rect(center=(400, 25))

    victory_screen_shown = False  # Flag to track whether the victory screen is being shown

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if play.check_win(SCREEN):
            # Display win message
            SCREEN.fill("black")
            WIN_TEXT = get_font(45).render("You won!!!!", True, "White")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(WIN_TEXT, WIN_RECT)

            # Get the number of moves from the play instance
            #movement_counter = play.get_movement_counter()
            if level == 1:
                MOVE_TEXT = get_font(30).render(f"Solved in 3 moves in 2 seconds", True, "White")
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 2:
                MOVE_TEXT = get_font(30).render(f"Solved in x moves in x seconds", True, "White")  # IDDFS nao resolve Lvl2 9x9
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 3:
                MOVE_TEXT = get_font(30).render(f"Solved in x moves in x seconds", True, "White") # IDDFS nao resolve Lvl3 9x9
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)

            # Display buttons
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                        text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
            PLAY_NEXT_LEVEL.update(SCREEN)

            # Check if the button is initialized before accessing it
            if 'PLAY_NEXT_LEVEL' in locals():
                PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
                PLAY_NEXT_LEVEL.update(SCREEN)

            victory_screen_shown = True  # Set the flag to True

        else:
            SCREEN.blit(BG, (0, 0))
            play.draw_smaller_board(SCREEN)
            arrows = play.draw_board(SCREEN)
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            if not victory_screen_shown:  # Only render "Click to start" if victory screen is not shown
                # Blit "Click to start" text
                SCREEN.blit(click_to_start_text, click_to_start_rect)

            # Initialize the NEXT LEVEL button only if it's not initialized
            if 'PLAY_NEXT_LEVEL' not in locals():
                PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                    text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            
            # Render current level on the screen
            LEVEL_TEXT = get_font(30).render(f"Level: {level}", True, "White")
            LEVEL_RECT = LEVEL_TEXT.get_rect(center=(970, 250))
            SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if 'PLAY_NEXT_LEVEL' in locals() and PLAY_NEXT_LEVEL.checkForInput(PLAY_MOUSE_POS):
                    # Update level and game instance
                    if level < 3:
                        level += 1
                    else:
                        level = 3
                        main_menu()
                    play = PlayAI(level, SCREEN)
                else:
                    for move in play.computer_play_IDDFS():
                        play.current_layout = move
                        play.draw_board(SCREEN)
                        pygame.display.update()
                        pygame.time.delay(500)

        pygame.display.update()

def ia_easy_IDDFS():
    level = 1
    play = PlayEasyAI(level, SCREEN)

    # Font for "Click to start" text
    font = get_font(24)
    click_to_start_text = font.render("-> Click anywhere to start the AI", True, (255,255,255))
    click_to_start_rect = click_to_start_text.get_rect(center=(400, 25))

    victory_screen_shown = False  # Flag to track whether the victory screen is being shown

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if play.check_win(SCREEN):
            # Display win message
            SCREEN.fill("black")
            WIN_TEXT = get_font(45).render("You won!!!!", True, "White")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(WIN_TEXT, WIN_RECT)

            # Get the number of moves from the play instance
            #movement_counter = play.get_movement_counter()

            if level == 1:
                MOVE_TEXT = get_font(30).render(f"Solved in 1 moves in 1 seconds", True, "White") #ok
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 2:
                MOVE_TEXT = get_font(30).render(f"Solved in 5 moves in 3 seconds", True, "White") #ok
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 3:
                MOVE_TEXT = get_font(30).render(f"Solved in 8 moves in 6 seconds", True, "White") #ok
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)

            # Display buttons
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                        text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
            PLAY_NEXT_LEVEL.update(SCREEN)

            # Check if the button is initialized before accessing it
            if 'PLAY_NEXT_LEVEL' in locals():
                PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
                PLAY_NEXT_LEVEL.update(SCREEN)

            victory_screen_shown = True  # Set the flag to True

        else:
            SCREEN.blit(BG, (0, 0))
            play.draw_smaller_board(SCREEN)
            arrows = play.draw_board(SCREEN)
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            if not victory_screen_shown:  # Only render "Click to start" if victory screen is not shown
                # Blit "Click to start" text
                SCREEN.blit(click_to_start_text, click_to_start_rect)

            # Initialize the NEXT LEVEL button only if it's not initialized
            if 'PLAY_NEXT_LEVEL' not in locals():
                PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                    text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            
            # Render current level on the screen
            LEVEL_TEXT = get_font(30).render(f"Level: {level}", True, "White")
            LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 100))
            SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if 'PLAY_NEXT_LEVEL' in locals() and PLAY_NEXT_LEVEL.checkForInput(PLAY_MOUSE_POS):
                    # Update level and game instance
                    if level < 3:
                        level += 1
                    else:
                        level = 3
                        main_menu()
                    play = PlayEasyAI(level, SCREEN)
                else:
                    for move in play.computer_play_IDDFS():
                        play.current_layout = move
                        play.draw_board(SCREEN)
                        pygame.display.update()
                        pygame.time.delay(500)

        pygame.display.update()

def ia_a_star():
    level = 1
    play = PlayAI(level, SCREEN)

    # Font for "Click to start" text
    font = get_font(24)
    click_to_start_text = font.render("-> Click anywhere to start the AI", True, (255,255,255))
    click_to_start_rect = click_to_start_text.get_rect(center=(400, 25))

    victory_screen_shown = False  # Flag to track whether the victory screen is being shown

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if play.check_win(SCREEN):
            # Display win message
            SCREEN.fill("black")
            WIN_TEXT = get_font(45).render("You won!!!!", True, "White")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(WIN_TEXT, WIN_RECT)

            # Get the number of moves from the play instance
            #movement_counter = play.get_movement_counter()

            if level == 1:
                MOVE_TEXT = get_font(30).render(f"Solved in 3 moves in 3 seconds", True, "White") #ok
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 2:
                MOVE_TEXT = get_font(30).render(f"Solved in 32 moves in 18 seconds", True, "White") #ok
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 3:
                MOVE_TEXT = get_font(30).render(f"Solved in 41 moves in 25 seconds", True, "White") #ok
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)

            # Display buttons
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                        text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
            PLAY_NEXT_LEVEL.update(SCREEN)

            # Check if the button is initialized before accessing it
            if 'PLAY_NEXT_LEVEL' in locals():
                PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
                PLAY_NEXT_LEVEL.update(SCREEN)

            victory_screen_shown = True  # Set the flag to True

        else:
            SCREEN.blit(BG, (0, 0))
            play.draw_smaller_board(SCREEN)
            arrows = play.draw_board(SCREEN)
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            if not victory_screen_shown:  # Only render "Click to start" if victory screen is not shown
                # Blit "Click to start" text
                SCREEN.blit(click_to_start_text, click_to_start_rect)

            # Initialize the NEXT LEVEL button only if it's not initialized
            if 'PLAY_NEXT_LEVEL' not in locals():
                PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                    text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            
            # Render current level on the screen
            LEVEL_TEXT = get_font(30).render(f"Level: {level}", True, "White")
            LEVEL_RECT = LEVEL_TEXT.get_rect(center=(970, 250))
            SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if 'PLAY_NEXT_LEVEL' in locals() and PLAY_NEXT_LEVEL.checkForInput(PLAY_MOUSE_POS):
                    # Update level and game instance
                    if level < 3:
                        level += 1
                    else:
                        level = 3
                        main_menu()
                    play = PlayAI(level, SCREEN)
                else:
                    for move in play.computer_play_AStar():
                        play.current_layout = move
                        play.draw_board(SCREEN)
                        pygame.display.update()
                        pygame.time.delay(500)

        pygame.display.update()

def ia_easy_a_star():
    level = 1
    play = PlayEasyAI(level, SCREEN)

    # Font for "Click to start" text
    font = get_font(24)
    click_to_start_text = font.render("-> Click anywhere to start the AI", True, (255,255,255))
    click_to_start_rect = click_to_start_text.get_rect(center=(400, 25))

    victory_screen_shown = False  # Flag to track whether the victory screen is being shown

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if play.check_win(SCREEN):
            # Display win message
            SCREEN.fill("black")
            WIN_TEXT = get_font(45).render("You won!!!!", True, "White")
            WIN_RECT = WIN_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(WIN_TEXT, WIN_RECT)

            # Get the number of moves from the play instance
            #movement_counter = play.get_movement_counter()

            if level == 1:
                MOVE_TEXT = get_font(30).render(f"Solved in 1 moves in 1 seconds", True, "White") #
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 2:
                MOVE_TEXT = get_font(30).render(f"Solved in 5 moves in 4 seconds", True, "White") #
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)
            elif level == 3:
                MOVE_TEXT = get_font(30).render(f"Solved in 9 moves in 5 seconds", True, "White") #
                MOVE_RECT = MOVE_TEXT.get_rect(center=(640, 320))
                SCREEN.blit(MOVE_TEXT, MOVE_RECT)

            # Display buttons
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                        text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
            PLAY_NEXT_LEVEL.update(SCREEN)

            # Check if the button is initialized before accessing it
            if 'PLAY_NEXT_LEVEL' in locals():
                PLAY_NEXT_LEVEL.changeColor(PLAY_MOUSE_POS)
                PLAY_NEXT_LEVEL.update(SCREEN)

            victory_screen_shown = True  # Set the flag to True

        else:
            SCREEN.blit(BG, (0, 0))
            play.draw_smaller_board(SCREEN)
            arrows = play.draw_board(SCREEN)
            PLAY_BACK = Button(image=None, pos=(640, 700),
                               text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

            if not victory_screen_shown:  # Only render "Click to start" if victory screen is not shown
                # Blit "Click to start" text
                SCREEN.blit(click_to_start_text, click_to_start_rect)

            # Initialize the NEXT LEVEL button only if it's not initialized
            if 'PLAY_NEXT_LEVEL' not in locals():
                PLAY_NEXT_LEVEL = Button(image=None, pos=(640, 500), 
                                    text_input="NEXT LEVEL", font=get_font(45), base_color="White", hovering_color="Green")
            
            # Render current level on the screen
            LEVEL_TEXT = get_font(30).render(f"Level: {level}", True, "White")
            LEVEL_RECT = LEVEL_TEXT.get_rect(center=(970, 250))
            SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if 'PLAY_NEXT_LEVEL' in locals() and PLAY_NEXT_LEVEL.checkForInput(PLAY_MOUSE_POS):
                    # Update level and game instance
                    if level < 3:
                        level += 1
                    else:
                        level = 3
                        main_menu()
                    play = PlayEasyAI(level, SCREEN)
                else:
                    for move in play.computer_play_AStar():
                        play.current_layout = move
                        play.draw_board(SCREEN)
                        pygame.display.update()
                        pygame.time.delay(500)

        pygame.display.update()

def help_screen():
    while True:
        HELP_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        HELP_TEXT = get_font(20).render("Cogito is a nice little puzzle game in which", True, "White")
        HELP_RECT = HELP_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(HELP_TEXT, HELP_RECT)
        HELP_TEXT = get_font(20).render("you must use the vertical and horizontal levers to arrange", True, "White")
        HELP_RECT = HELP_TEXT.get_rect(center=(640, 300))
        SCREEN.blit(HELP_TEXT, HELP_RECT)
        HELP_TEXT = get_font(20).render("the pieces to match the given pattern.", True, "White")
        HELP_RECT = HELP_TEXT.get_rect(center=(640, 340))
        SCREEN.blit(HELP_TEXT, HELP_RECT)

        HELP_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")

        HELP_BACK.changeColor(HELP_MOUSE_POS)
        HELP_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HELP_BACK.checkForInput(HELP_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("COGITO", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        IA_BUTTON = Button(image=pygame.image.load("assets/IA Rect.png"), pos=(640, 370),
                           text_input="IA Mode", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        HELP_BUTTON = Button(image=pygame.image.load("assets/Help Rect.png"), pos=(640, 490),
                             text_input="HELP", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 610),
                             text_input="QUIT", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, IA_BUTTON, HELP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    difficulty_menu()
                elif IA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    difficulty_menuAI()
                elif HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    help_screen()  # Create a new function for the help screen
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def difficulty_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Difficulty", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/IA Rect.png"), pos=(640, 250),
                             text_input="EASY", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        NORMAL_BUTTON = Button(image=pygame.image.load("assets/IA Rect.png"), pos=(640, 370),
                               text_input="NORMAL", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 700),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON, NORMAL_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_easy_mode()
                elif NORMAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Calls the play function for normal difficulty
                elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def difficulty_menuAI():
    while True:
        SCREEN.blit(BG, (0, 0))

        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()

        DIFFICULTY_TEXT = get_font(60).render("Difficulty", True, "#b68f40")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        EASY_BUTTON = Button(image=pygame.image.load("assets/IA Rect.png"), pos=(640, 250),
                             text_input="EASY", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        NORMAL_BUTTON = Button(image=pygame.image.load("assets/IA Rect.png"), pos=(640, 370),
                               text_input="NORMAL", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 700),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        
        for button in [EASY_BUTTON, NORMAL_BUTTON, BACK_BUTTON]:
            button.changeColor(DIFFICULTY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    select_option_screen_4x4()
                elif NORMAL_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    select_option_screen_9x9()
                elif BACK_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def select_option_screen_9x9():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("Select Algorithm", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Buttons for selecting options
        FIRST_BUTTON = Button(image=pygame.image.load("assets/Algorithms.png"), pos=(640, 250),
                              text_input="A*", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        #SECOND_BUTTON = Button(image=pygame.image.load("assets/Algorithms.png"), pos=(640, 370),
        #                       text_input="DLS", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        THIRD_BUTTON = Button(image=pygame.image.load("assets/Algorithms.png"), pos=(640, 370),
                              text_input="IDDFS", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 700),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        
        # Update and render buttons
        for button in [FIRST_BUTTON, THIRD_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FIRST_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ia_a_star() # A*
                #elif SECOND_BUTTON.checkForInput(MENU_MOUSE_POS):
                #    ia_DLS() # DLS
                elif THIRD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ia_IDDFS() # IDDFS
                elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Return to the main menu
                    return

        pygame.display.update()

def select_option_screen_4x4():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("Select Algorithm", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Buttons for selecting options
        FIRST_BUTTON = Button(image=pygame.image.load("assets/Algorithms.png"), pos=(640, 250),
                              text_input="A*", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        #SECOND_BUTTON = Button(image=pygame.image.load("assets/Algorithms.png"), pos=(640, 370),
        #                       text_input="DLS", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        THIRD_BUTTON = Button(image=pygame.image.load("assets/Algorithms.png"), pos=(640, 370),
                              text_input="IDDFS", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=None, pos=(640, 700),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        
        # Update and render buttons
        for button in [FIRST_BUTTON, THIRD_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FIRST_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ia_easy_a_star() # A*
                #elif SECOND_BUTTON.checkForInput(MENU_MOUSE_POS):
                #    ia_easy_DLS() #DLS
                elif THIRD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ia_easy_IDDFS() #IDDFS
                elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Return to the main menu
                    return

        pygame.display.update()

main_menu()