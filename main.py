# DRIVER

# relevant files imported
import pygame, sys
from board import *
from moves import *

# initialize pygame
pygame.init()  # essential for pygame

# define and display surface (with caption)
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption('GHOST CHESS')
# define and display the dock icon
icon = pygame.image.load("./icon/game/icon1_32px.png")
pygame.display.set_icon(icon)
# display chessboard
bg = pygame.image.load("background/game/background3.png")

player = "Player"  # 'AI' for the computer player
depth = 5 # minimax algo depth for search
gameover = False
win = 0

# # board matrix, create instance of board class from ./board.py
board = Board(1)

# allows us to keep track of sprites/game objects
all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]
all_sprites_list.add(sprites)

# draw the sprites onto the screen
all_sprites_list.draw(screen)

# necessary for capping the game at 60FPS
clock = pygame.time.Clock()


def welcome():
    '''
    Introduction Page
    '''
    global player, depth, board, all_sprites_list, sprites

    intro = True
    while intro:
        # make background grey
        screen.fill((50, 50, 50))
        # add image and messages
        screen.blit(pygame.image.load("./icon/intro/chess1.png"), (180, 100))
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("GHOST CHESS", True, (106, 127, 232), (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (240, 240 + 20)
        screen.blit(text, textRect)
        # Press 1 - Higher Difficulty
        font1 = pygame.font.Font("freesansbold.ttf", 20)
        text1 = font1.render("Press 1 - Go toe to toe with Agent Smith", True, (106, 127, 232), (50, 50, 50))
        textRect1 = text1.get_rect()
        textRect1.center = (240, 240 + 70)
        screen.blit(text1, textRect1)
        font1_1 = pygame.font.Font("freesansbold.ttf", 14)
        text1_1 = font1_1.render("          Pick only if you think you are the ONE", True, (106, 127, 232), (50, 50, 50))
        textRect1_1 = text1_1.get_rect()
        textRect1_1.center = (240, 240 + 90)
        screen.blit(text1_1, textRect1_1)
        # Press 2 - Lower Difficulty
        font2 = pygame.font.Font("freesansbold.ttf", 20)
        text2 = font2.render("Press 2 - Fight Morpheus in the Simulator", True, (106, 127, 232), (50, 50, 50))
        textRect2 = text2.get_rect()
        textRect2.center = (240, 240 + 120)
        screen.blit(text2, textRect2)
        # Press Q - QUIT
        font3 = pygame.font.Font("freesansbold.ttf", 20)
        text3 = font3.render("Press Q - Quit", True, (106, 127, 232), (50, 50, 50))
        textRect3 = text3.get_rect()
        textRect3.center = (240, 240 + 150)
        screen.blit(text3, textRect3)
        # makers
        font4 = pygame.font.Font("freesansbold.ttf", 11)
        text4 = font4.render("-- Mind Concinnity", True, (106, 127, 232), (50, 50, 50))
        textRect4 = text4.get_rect()
        textRect4.center = (240 + 150, 240 + 210)
        screen.blit(text4, textRect4)

        # keyboard press event for option selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_1:
                    intro = False
                    depth = 5
                    print("depth = 5")
                elif event.key == pygame.K_2:
                    intro = False
                    depth = 3
                    print("depth = 3")
                choose_color = True
        pygame.display.flip()

    while choose_color:
        # re-fill background
        screen.fill((50, 50, 50))
        # Choose color
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Choose Color:", True, (106, 127, 232), (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (240, 240 + 20)
        screen.blit(text, textRect)
        # Press 1 - White
        font1 = pygame.font.Font("freesansbold.ttf", 20)
        text1 = font1.render("Press 1 - White", True, (106, 127, 232), (50, 50, 50))
        textRect1 = text1.get_rect()
        textRect1.center = (240, 240 + 70)
        screen.blit(text1, textRect1)
        player = "Player"
        # Press 2 - Black
        font1 = pygame.font.Font("freesansbold.ttf", 20)
        text1 = font1.render("Press 2 - Black", True, (106, 127, 232), (50, 50, 50))
        textRect1 = text1.get_rect()
        textRect1.center = (240, 240 + 100)
        screen.blit(text1, textRect1)
        player = "AI"


        # keyboard press event for option selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_1:
                    choose_color = False
                    player = "Player"
                    print("You are white (not being a racist)")
                    board = Board(1)
                    all_sprites_list = pygame.sprite.Group()
                    sprites = [piece for row in board.array for piece in row if piece]
                    all_sprites_list.add(sprites)
                    all_sprites_list.draw(screen)
                elif event.key == pygame.K_2:
                    choose_color = False
                    player = "AI"
                    print("You are black (not being a racist)")
                    board = Board(1)
                    all_sprites_list = pygame.sprite.Group()
                    sprites = [piece for row in board.array for piece in row if piece]
                    all_sprites_list.add(sprites)
                    all_sprites_list.draw(screen)

        pygame.display.flip()


def select_piece(color):
    '''
    Select piece on board
    Returns iff valid piece was selected based on the color
    '''
    # get mouse pointer coordinates
    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    # only highlight, and return if its the player's piece
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]


def select_square():
    '''
    Returns board coordinates of where the mouse selected.
    '''
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return (y, x)


def run_game():
    '''
    Game loop
    '''
    global player, gameover, win

    gameover = False # indicates whether game is over
    selected = False  # indicates whether a piece is selected yet
    trans_table = dict()  # holds previously computed minimax values
    checkWhite = False

    while not gameover:

        # Human player's turn
        if player == "Player":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        sys.exit()

                # select a piece to move
                elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                    piece = select_piece("w")

                    # a white piece was selected, generate pseudo-legal moves
                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        selected = True

                # piece is selected, now move it somewhere
                elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                    square = select_square()
                    special_moves = special_move_gen(board, "w")

                    # square selected is a pseudo-legal move
                    if square in player_moves:
                        oldx = piece.x  # preserve, in case we have to reverse the move
                        oldy = piece.y
                        # preserve the piece we're potentially capturing
                        dest = board.array[square[0]][square[1]]

                        # attempt to move the piece
                        # if a pawn promotion occurs, return the pieces that
                        # we need to update in the sprites list
                        pawn_promotion = board.move_piece(
                            piece, square[0], square[1])

                        # remove the pawn sprite, add the queen sprite
                        if pawn_promotion:  
                            all_sprites_list.add(pawn_promotion[0])
                            sprites.append(pawn_promotion[0])
                            all_sprites_list.remove(pawn_promotion[1])
                            sprites.remove(pawn_promotion[1])

                        # this is needed for proper castling
                        if type(piece) == King or type(piece) == Rook:
                            piece.moved = True
                        # remove the sprite of the piece that was captured
                        if dest:  
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)

                        # Now we have to see if move puts you in check
                        # generate a set of the attacked squared
                        attacked = move_gen(board, "b", True)
                        # move not in check, we're good
                        if (board.white_king.y, board.white_king.x) not in attacked:
                            selected = False
                            player = "AI"
                            # update the 'score' of the board
                            if dest:
                                board.score -= board.pvalue_dict[type(dest)]
                        # move is in check, we have to reverse it
                        else:  
                            board.move_piece(piece, oldy, oldx)
                            if type(piece) == King or type(piece) == Rook:
                                piece.moved = False
                            board.array[square[0]][square[1]] = dest
                            if dest:  # if dest not None
                                all_sprites_list.add(dest)
                                sprites.append(dest)
                            if pawn_promotion:
                                all_sprites_list.add(pawn_promotion[1])
                                sprites.append(pawn_promotion[1])
                            piece.highlight()

                            # different sidemenus depend on whether or not you're
                            # currently in check
                            if checkWhite:
                                pygame.display.update()
                                pygame.time.wait(1000)
                            else:
                                pygame.display.update()
                                pygame.time.wait(1000)

                    # cancel the move, you've selected the same square
                    elif (piece.y, piece.x) == square:
                        piece.unhighlight()
                        selected = False

                    # square selected is a potential special move
                    elif special_moves and square in special_moves:
                        special = special_moves[square]
                        # special move is castling, perform it
                        if (special == "CR" or special == "CL") and type(piece) == King:
                            board.move_piece(
                                piece, square[0], square[1], special)
                            selected = False
                            player = "AI"


        # Computer player's turn
        elif player == "AI":

            # get a move from the minimax/alphabeta algorithm, at a search depth of 3
            value, move = minimax(board, depth, float("-inf"), float("inf"), True, trans_table)

            # this indicates an AI in checkmate; it has no possible moves
            if value == float("-inf") and move == 0:
                print(value)
                print(move)
                gameover = True
                player = "Player"
                win = 1
            # perform the AI's move
            else:
                start = move[0]
                end = move[1]
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]

                # deal with a possible pawn promotion, the same way it is dealt
                # above for the player
                pawn_promotion = board.move_piece(piece, end[0], end[1])
                if pawn_promotion:
                    all_sprites_list.add(pawn_promotion[0])
                    sprites.append(pawn_promotion[0])
                    all_sprites_list.remove(pawn_promotion[1])
                    sprites.remove(pawn_promotion[1])

                if dest:
                    all_sprites_list.remove(dest)
                    sprites.remove(dest)
                    board.score += board.pvalue_dict[type(dest)]

                player = "Player"
                # check to see if the player is now in check, as a result of the
                # AI's move
                attacked = move_gen(board, "b", True)
                if (board.white_king.y, board.white_king.x) in attacked:
                    checkWhite = True
                else:
                    checkWhite = False

            if value == float("inf"):
                print("Player checkmate")
                gameover = True
                player = "AI"
                win = 2

        # update the screen and the sprites after the move has been performed
        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)

def game_over():
    '''
    Game over page
    '''
    global depth, win
    while gameover:
        # see if/how the game is over
        for i in range(0, 100000):
            i = i + 1
        # make background grey
        screen.fill((50, 50, 50))
        # add image and messages
        screen.blit(pygame.image.load("./icon/gameover/monarchy.png"), (180, 130))
        if win == 1:
            # Player WON
            font1 = pygame.font.Font("freesansbold.ttf", 20)
            text1 = font1.render("Welcome to Zion Neo.", True, (179, 102, 255), (50, 50, 50))
            textRect1 = text1.get_rect()
            textRect1.center = (240, 240 + 70)
            screen.blit(text1, textRect1)
        elif win == 2:
            # AI WON
            font2 = pygame.font.Font("freesansbold.ttf", 20)
            text2 = font2.render("And I thought you were Mr. Anderson...", True, (179, 102, 255), (50, 50, 50))
            textRect2 = text2.get_rect()
            textRect2.center = (240, 240 + 100)
            screen.blit(text2, textRect2)
        else:
            # stalemate
            font3 = pygame.font.Font("freesansbold.ttf", 20)
            text3 = font3.render("You are good. Just not the one.", True, (179, 102, 255), (50, 50, 50))
            textRect3 = text3.get_rect()
            textRect3.center = (240, 240 + 100)
            screen.blit(text3, textRect3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    sys.exit()
        pygame.display.flip()

    import os
    board.print_to_terminal()
    crown = pygame.image.load("assets/crown.png").convert_alpha()
    crown = pygame.transform.scale(crown, (80, 60))
    screen.blit(crown, (520, 20))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.event.clear()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == pygame.QUIT:
                import sys
                sys.exit()

if __name__ == "__main__":
    welcome()
    run_game()
    game_over()
