# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                            ╠══╣
# ║  ║    CHESS BOARD SIMULATOR                   CREATED: 2023-11-11          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                            ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ═══════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# This script randomly selects a chess game from the available PGN's in the PGN/ dir. It replays the game and updates
#   the board according to the color profile selected. 
#
# Future improvements: BRO-15
#   Additional color profiles that swap between games
#   OLED display to show players, elo, location, etc...
#   Screen wipes/ animations between games
#   Visual indicators of moves like check/ checkmate and stockfish evaluations like brilliant moves or blunders
# ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
from Settings import *
import random
import chess
import chess.pgn
import time
import board
import neopixel

pixels = None

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Converts a given game board (which uses characters for pieces) to an integer list
INPUT: game - chess.pgn game
OUTPUT: list of the current board state as integers
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def convert_to_int(game):
    epd_string = game.epd()
    list_int = []
    for i in epd_string:
        if i == " ":
            return list_int
        elif i != "/":
            if i in STRING_TO_INT_PIECE_MAP:
                list_int.append(STRING_TO_INT_PIECE_MAP[i])
            else:
                for counter in range(0, int(i)):
                    list_int.append(0)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Helper function to go and grab 'num' game from a specific pgn file
INPUT: pgn_file_io - file object for the pgn file
       num - game number to pull from the file
OUTPUT: 
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_game(pgn_file_io, num):
    for x in range(1, num):
        chess.pgn.skip_game(pgn_file_io)
    return chess.pgn.read_game(pgn_file_io)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Pulls a random game from one of the available PGN files
INPUT: NA
OUTPUT: chess.pgn object of the random game
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_random_game():
    data = PGN_DIR[random.randrange(0, len(PGN_DIR))]
    pgn_fileio = open(data[0])
    return get_game(pgn_fileio, random.randrange(0, data[1]))


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: For the current piece (different for white and black) return the rgb value from the color profile
INPUT: piece - (str) defined in Settings.py STRING_TO_INT_PIECE_MAP
OUTPUT: rgb value (list) [r, g, b]
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_rgb_piece_value(piece):
    square_rgb = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    if piece != 0:
        base_color = COLOR_PROFILE[piece < 0]
        square_rgb[0] = base_color
        square_rgb[1] = base_color
        square_rgb[2] = base_color if abs(piece) == 6 else COLOR_PROFILE[abs(piece) + 1]
    return square_rgb


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Helper function to set the pixels for a specific square on the board
INPUT: square - given square on the board (0-63)
       rgb_piece_value - list of [r, g, b] values for the given piece
OUTPUT: NA
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def set_pixel_square(square, rgb_piece_value):
    index = INT_BOARD_TO_LED_MATRIX[square] * 3
    pixels[index] = rgb_piece_value[0] if square % 2 == 0 else rgb_piece_value[2]
    pixels[index+1] = rgb_piece_value[1]
    pixels[index+2] = rgb_piece_value[2] if square % 2 == 0 else rgb_piece_value[0]


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Updates the LED board with the given game position
INPUT: board - chess game board of the current position
OUTPUT: NA
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def upload_board_to_leds(board):
    int_board = convert_to_int(board)
    for square, int_piece in enumerate(int_board):
        set_pixel_square(square, get_rgb_piece_value(int_piece))
    pixels.show()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Runs the provided game by incrementing moves, updating the board, and delaying 0.5s between moves
INPUT: game - a chess.pgn object that we will now replay
OUTPUT: NA
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def run_game(game):
    game_board = game.board()
    for move in game.mainline_moves():
        game_board.push(move)
        upload_board_to_leds(game_board)
        time.sleep(0.5)


def main():
    global pixels
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER)
    
    random.seed()
    while True:
        run_game(get_random_game())


if __name__ == "__main__":
    main()

# FIN ════════════════════════════════════════════════════════════════════════════════════════════════════════════════
