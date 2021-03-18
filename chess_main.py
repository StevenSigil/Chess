"""
Main driver file. Responsible for handling user input and displaying the current GameState object
"""

import pygame as p

import chess_engine

WIDTH = HEIGHT = 512  # or 400
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # animation
IMAGES = {}


def load_images():
    """
    Initialize a global dictionary of images. Called exactly once in the main.
    """
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"assets/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    # NOTE: Access images by saying IMAGES['wP']


def main():
    """
    Main driver for our code. Will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    load_images()  # only do this once, before loop
    running = True
    sq_selected = ()  # No square selected initially, keep track of the last click of the user: (tuple:(row, col))
    player_clicks = []  # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) loc of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sq_selected == (row, col):  # the user clicked the same square twice
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear variable
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks

                if len(player_clicks) == 2:  # 2nd click
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)

                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = ()  # reset user player_clicks
                    player_clicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

    p.quit()


def drawGameState(screen, gs):
    """
    Responsible for all the graphics within a current game state.
    """
    draw_board(screen)  # draw squares on the board

    # Add piece highlights or move suggestions here
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares


def draw_board(screen):
    """
    Draws the white/gray squares
    """
    colors = [p.Color("white"), p.Color("light gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draws the pieces on the board using the current GameState.board (top-left always white)
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
