import chess
from math import inf


PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

PAWN_SCORE = 100
KNIGHT_SCORE = 300
BISHOP_SCORE = 300
ROOK_SCORE = 500
QUEEN_SCORE = 1000
KING_SCORE = 400

OPPONENT = True
ME = False

INF = float("inf")

class AlphaBetaAI():
    def __init__(self, depth):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        minimax_scores = []

        for m in moves:
            board.push(m)
            score = self.minimax(board, 1, -INF, INF)
            board.pop()
            minimax_scores.append((score, m))
        best_move = max(minimax_scores, key=lambda x: x[0])[1]

        return best_move

    def minimax(self, board, depth, alpha, beta):
        if self.depth == depth or board.is_game_over():
            value = self.evaluation(board)
            return value
        moves = list(board.legal_moves)

        # OPPONENT
        if depth % 2 == 0:
            best_value = INF
            for m in moves:
                board.push(m)
                value = self.minimax(board, depth + 1, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                board.pop()
                if beta <= alpha:
                    break
            return best_value

        # ME
        else:
            best_value = -INF
            for m in moves:
                board.push(m)
                value = self.minimax(board, depth + 1, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                board.pop()
                if beta <= alpha:
                    break
            return best_value

    ### Total Eval Function
    def evaluation(self, board):
        total_eval = self.primary_evaluation_function(board) + self.table_evaluation_function(board)
        return total_eval

    ### First evaluation method
    def primary_evaluation_function(self, board):
        pawn_score = self.calculate_score(board, PAWN_SCORE, PAWN)
        knight_score = self.calculate_score(board, KNIGHT_SCORE, KNIGHT)
        bishop_score = self.calculate_score(board, BISHOP_SCORE, BISHOP)
        rook_score = self.calculate_score(board, ROOK_SCORE, ROOK)
        queen_score = self.calculate_score(board, QUEEN_SCORE, QUEEN)

        sum_evaluate = pawn_score + knight_score + bishop_score + rook_score + queen_score
        return sum_evaluate

    def piece_count(self, board, piece, side):
        return len(list(board.pieces(piece, side)))

    def calculate_score(self, board, piece_score, piece_type):
        return piece_score * (
                    self.piece_count(board, piece_type, ME) - self.piece_count(board, piece_type, OPPONENT))

    ### Second evaluation method
    def table_score(self, board, piece_table, piece_type, side):
        pieces = list(board.pieces(piece_type, side))
        if side:
            piece_table.reverse()
            sum_score = sum([piece_table[x] for x in pieces])
            piece_table.reverse()
        else:
            sum_score = sum([piece_table[x] for x in pieces])
        return sum_score

    def table_evaluation_function(self, board):
        pawn_score = self.table_score(board, PAWN_TABLE, PAWN, OPPONENT)
        knight_score = self.table_score(board, KNIGHT_TABLE, KNIGHT, OPPONENT)
        bishop_score = self.table_score(board, BISHOP_TABLE, BISHOP, OPPONENT)
        rook_score = self.table_score(board, ROOK_TABLE, ROOK, OPPONENT)
        queen_score = self.table_score(board, QUEEN_TABLE, QUEEN, OPPONENT)
        king_score = self.table_score(board, KING_TABLE, KING, OPPONENT)

        sum_evaluate = pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score
        return sum_evaluate

PAWN_TABLE = [0, 0, 0, 0, 0, 0, 0, 0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5, 5, 10, 25, 25, 10, 5, 5,
              0, 0, 0, 20, 20, 0, 0, 0,
              5, -5, -10, 0, 0, -10, -5, 5,
              5, 10, 10, -20, -20, 10, 10, 5,
              0, 0, 0, 0, 0, 0, 0, 0]

KNIGHT_TABLE = [-50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50]

BISHOP_TABLE = [-20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20]

ROOK_TABLE = [0, 0, 0, 0, 0, 0, 0, 0,
              5, 10, 10, 10, 10, 10, 10, 5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              0, 0, 0, 5, 5, 0, 0, 0]

QUEEN_TABLE = [-20, -10, -10, -5, -5, -10, -10, -20,
               -10, 0, 0, 0, 0, 0, 0, -10,
               -10, 0, 5, 5, 5, 5, 0, -10,
               -5, 0, 5, 5, 5, 5, 0, -5,
               0, 0, 5, 5, 5, 5, 0, -5,
               -10, 5, 5, 5, 5, 5, 0, -10,
               -10, 0, 5, 0, 0, 0, 0, -10,
               -20, -10, -10, -5, -5, -10, -10, -20]

KING_TABLE = [-30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -20, -30, -30, -40, -40, -30, -30, -20,
              -10, -20, -20, -20, -20, -20, -20, -10,
              20, 20, 0, 0, 0, 0, 20, 20,
              20, 30, 10, 0, 0, 10, 30, 20]

