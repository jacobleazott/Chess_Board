
import chess.pgn
import chess

mapped = {
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


def convert_to_int(self):
    epd_string = self.epd()
    list_int = []
    for i in epd_string:
        if i == " ":
            return list_int
        elif i != "/":
            if i in mapped:
                list_int.append(mapped[i])
            else:
                for counter in range(0, int(i)):
                    list_int.append(0)


def print_board(game_board):
    int_board = convert_to_int(game_board)
    count = 0
    for x in range(0, 8):
        print(int_board[x*8:(x*8 + 7)])


def test():
    first_game = chess.pgn.read_game(pgn)
    chess.pgn.skip_game(pgn)
    second_game = chess.pgn.read_game(pgn)
    third_game = chess.pgn.read_game(pgn)
    board = first_game.board()
    for move in first_game.mainline_moves():
        board.push(move)
        print_board(board)
        print()

    board = second_game.board()
    for move in second_game.mainline_moves():
        board.push(move)
        print_board(board)
        print()


def get_game(pgn_file_io, num):
    for x in range(1, num):
        chess.pgn.skip_game(pgn_file_io)
    return chess.pgn.read_game(pgn_file_io)


pgn = open("PGN/Frank.pgn")

print(get_game(pgn, 1622))

