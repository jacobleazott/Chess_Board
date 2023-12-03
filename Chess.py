from Settings import *
import random
import chess
import chess.pgn
import time
import board
import neopixel


def convert_to_int(self):
    epd_string = self.epd()
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


def get_game(pgn_file_io, num):
    for x in range(1, num):
        chess.pgn.skip_game(pgn_file_io)
    return chess.pgn.read_game(pgn_file_io)


def get_random_game():
    data = PGN_DIR[random.randrange(0, len(PGN_DIR))]
    pgn_fileio = open(data[0])
    return get_game(pgn_fileio, random.randrange(0, data[1]))


def get_rgb_piece_value(piece):
    square_rgb = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    if piece != 0:
        square_rgb[0:2] = COLOR_PROFILE[piece < 0]
        # If Not King
        if piece != 6:
            square_rgb[2] = COLOR_PROFILE[abs(piece) + 1]
    return square_rgb


def set_pixel_square(square, rgb_piece_value):
    index = INT_BOARD_TO_LED_MATRIX[square] * 3
    pixels[index] = rgb_piece_value[0] if square % 2 else rgb_piece_value[2]
    pixels[index+1] = rgb_piece_value[1]
    pixels[index+2] = rgb_piece_value[2] if square % 2 else rgb_piece_value[0]


def upload_board_to_leds(board):
    int_board = convert_to_int(board)
    for square, int_piece in enumerate(int_board):
        set_pixel_square(square, get_rgb_piece_value(int_piece))
    pixels.show()


def run_game(game):
    game_board = game.board()
    for move in game.mainline_moves():
        game_board.push(move)
        upload_board_to_leds(game_board)
        time.sleep(0.5)


def run():
    random.seed()
    while True:
        run_game(get_random_game())


pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER)
run()
