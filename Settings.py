import board
import neopixel
from Color_Profile import *

COLOR_PROFILE = COLOR_PROFILE_1
BRIGHTNESS = 0.2
NUM_LEDS = 192
PIXEL_PIN = board.D18
ORDER = neopixel.GRB

INT_BOARD_TO_LED_MATRIX = [7, 8, 23, 24, 39, 40, 55, 56,
                           6, 9, 22, 25, 38, 41, 54, 57,
                           5, 10, 21, 26, 37, 42, 53, 58,
                           4, 11, 20, 27, 36, 43, 52, 59,
                           3, 12, 19, 28, 35, 44, 51, 60,
                           2, 13, 18, 29, 34, 45, 50, 61,
                           1, 14, 17, 30, 33, 46, 49, 62,
                           0, 15, 16, 31, 32, 47, 48, 63]

PGN_DIR = [["PGN/Capablanca.pgn", 597],
           ["PGN/Carlsen.pgn", 5000],
           ["PGN/Caruana.pgn", 4114],
           ["PGN/Nakamura.pgn", 6603],
           ["PGN/Frank.pgn", 1622]]

STRING_TO_INT_PIECE_MAP = {
    'P': 1,  # White Pawn
    'p': -1,  # Black Pawn
    'N': 2,  # White Knight
    'n': -2,  # Black Knight
    'B': 3,  # White Bishop
    'b': -3,  # Black Bishop
    'R': 4,  # White Rook
    'r': -4,  # Black Rook
    'Q': 5,  # White Queen
    'q': -5,  # Black Queen
    'K': 6,  # White King
    'k': -6  # Black King
}