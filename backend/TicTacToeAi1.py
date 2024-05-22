# Bai Thieu: x

from enum import Enum

class Direction(Enum):
    VERTICAL = ((-1, 0), (1, 0))
    HORIZONTAL = ((0, -1), (0, 1))
    MAIN_DIAG = ((-1, -1), (1, 1))
    ANTI_DIAG = ((-1, 1), (1, -1))
    TRAVERSE_VERTICALLY = (1, 0)
    TRAVERSE_HORIZONTALY = (0, 1)
    TRAVERSE_MAIN_DIAG = (1, 1)
    TRAVERSE_ANTI_DIAG = (1, -1)
    DIR = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1))


DV = Direction.VERTICAL
DH = Direction.HORIZONTAL
DM = Direction.MAIN_DIAG
DA = Direction.ANTI_DIAG
dV = Direction.TRAVERSE_VERTICALLY
dH = Direction.TRAVERSE_HORIZONTALY
dM = Direction.TRAVERSE_MAIN_DIAG
dA = Direction.TRAVERSE_ANTI_DIAG
dirs = Direction.DIR
STREAK_LEN = 5
win_situation_score = 1000
lose_situation_score = 900


def is_empty(board):
    return board == [[' '] * len(board)] * len(board)

def validate(size, r, c):
        return r >= 0 and r < size and c >= 0 and c < size

def win_situation(statistics_score):
        if statistics_score[STREAK_LEN]:
            return 5
        else:
            # Two 4 streaks with different directions can win
            if len(statistics_score[4]) >= 2:
                return 4
            elif len(statistics_score[4]) == 1:
                # In one direction if has two 4 streaks, it can win
                dir_4 = list(statistics_score[4].keys())[0]
                if statistics_score[4][dir_4] >= 2:
                    return 4
                else:
                    # If a diretion has a 4 streaks and another direction has a 3 streaks that not be blocked, it can win
                    for dir_3 in statistics_score[3]:
                        if statistics_score[3][dir_3] >= 2 and dir_3 != dir_4:
                            return 4
            else:
                # If two directions has 3 streaks that not be blocked, it can win
                score_3 = sorted(statistics_score[3].values(), reverse=True)
                if len(score_3) >= 2 and score_3[0] >= score_3[1] >= 2:
                    return 3
        return 0

def synthesize_score(statistics_score):
        '''
        Parameters:
            statistics_score: the statistics score of the four directions
        Returns:
            the synthesize score 
        '''  
        synthesized_scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
        for score in statistics_score:
            if score == STREAK_LEN:
                synthesized_scores[score] = 1 if statistics_score[score] else 0
            else:
                synthesized_scores[score] = sum(statistics_score[score].values())
        return synthesized_scores    


def statistics_score(score_dir):
        '''
        Parameters:
            score_dir: a dictionary of the scores of the four directions
        Returns:
            the statistics score of the four directions
        '''
        statistics_score = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
        for dir in score_dir:
            direction = Direction[dir].value[1]
            for score in score_dir[dir]:
                if direction in statistics_score[score]:
                    statistics_score[score][direction] += 1
                else:
                    statistics_score[score][direction] = 1
        return statistics_score    

def score_series(board, start_coord, direction, end_coord, piece):
        '''
        Parameters:
            start_coord: the starting coordinate of the series
            direction: the direction of the series
            end_coord: the ending coordinate of the series
            piece: the piece to score

        Returns:
            a list of the scores of the series
        '''
        def get_series(board, start_coord, end_coord, direction):
            '''
            Parameters:
                board: the board
                start_coord: the starting coordinate of the series
                direction: the direction of the series
                end_coord: the ending coordinate of the series
            Returns:
                a list of the series
            '''
            start_row, start_col = start_coord
            dir_row, dir_col = direction
            end_row, end_col = end_coord

            series = []
            while start_row != end_row + dir_row or start_col != end_col + dir_col:
                series.append(board[start_row][start_col])
                start_row += dir_row
                start_col += dir_col
            return series
        
        series = get_series(board, start_coord, end_coord, direction)
        series_scores = []

        def score_of_five_cell(cell_list, piece):
            '''
            Parameters:
                cell_list: a list of five continuous cells
                piece: the piece to score
            Returns:
                the score of the five continuous cells
            '''
            blank = cell_list.count(' ')
            filled = cell_list.count(piece)

            if blank + filled < 5:
                return -1
            else:
                return filled
        
        for start in range(len(series) - 4):
            score = score_of_five_cell(series[start:start + 5], piece)
            series_scores.append(score)

        return series_scores

def score_cell(board, size, piece, coord):
        '''
        Parameters:
            coord: the coordinate of the cell
            piece: the piece in the cell
        Returns:
            a dictionary of the scores of the four directions
        '''
        r, c = coord
        score_dir = {DV.name: [], DH.name: [], DM.name: [], DA.name: []}

        score_dir[DV.name].extend(score_series(board, march(board, size, coord, DV.value[0], STREAK_LEN - 1), dV.value, 
                                                     march(board, size, coord, DV.value[1], STREAK_LEN - 1), piece))
        
        score_dir[DH.name].extend(score_series(board, march(board, size, coord, DH.value[0], STREAK_LEN - 1), dH.value, 
                                                     march(board, size, coord, DH.value[1], STREAK_LEN - 1), piece))
        
        score_dir[DM.name].extend(score_series(board, march(board, size, coord, DM.value[0], STREAK_LEN - 1), dM.value, 
                                                     march(board, size, coord, DM.value[1], STREAK_LEN - 1), piece))
        
        score_dir[DA.name].extend(score_series(board, march(board, size, coord, DA.value[0], STREAK_LEN - 1), dA.value, 
                                                     march(board, size, coord, DA.value[1], STREAK_LEN - 1), piece))
        
        return statistics_score(score_dir)    

def march(board, size, coord, direction, len):
        '''
        Parameters:
            coord: the starting coordinate
            direction: the direction of the march
            len: the length of the march
        Returns:
            the ending coordinate of the march
        '''
        start_row, start_col = coord
        dir_row, dir_col = direction
        end_row = start_row + dir_row * len
        end_col = start_col + dir_col * len

        while not validate(size, end_row, end_col):
            end_row -= dir_row
            end_col -= dir_col
        
        return end_row, end_col    

def possible_moves(board, size):
        taken = []
        for row in range(size):
            for col in range(size):
                if board[row][col] != ' ':
                    taken.append((row, col))
        
        possible_moves = []
        for dir in dirs.value:
            for coord in taken:
                for length in range(1, STREAK_LEN):
                    move = march(board, size, coord, dir, length)
                    if move not in taken and move not in possible_moves:
                        possible_moves.append(move)
        
        return possible_moves


def heuristic(board, size, move):
        res = dis = adv = 0
        r, c = move
        ally = "x"
        enemy = "o"
        
        # Advantage of ally if ally makes the move
        board[r][c] = ally
        statistics_score = score_cell(board, size, ally, move)
        win_situationx = win_situation(statistics_score)
        attack_score = synthesize_score(statistics_score)
        adv += (win_situationx * win_situation_score + attack_score[-1] + attack_score[1] + 4 * attack_score[2] 
                + 9 * attack_score[3] + 16 * attack_score[4])
        
        # Disadvantage of ally if enemy makes the move
        board[r][c] = enemy
        statistics_score = score_cell(board, size, enemy, move)
        lose_situation = win_situation(statistics_score)
        defend_score = synthesize_score(statistics_score)
        dis += (lose_situation * lose_situation_score + defend_score[-1] + defend_score[1] + 4 * defend_score[2]
                + 9 * defend_score[3] + 16 * defend_score[4])
        
        res = adv + dis

        board[r][c] = ' '
        return res

def get_move1(board, size):
        best_move = (0, 0)
        if is_empty(board):
            best_move = size // 2, size // 2
        else:
            moves = possible_moves(board, size)
            best_score = float('-inf')
            print(len(moves))
            for move in moves:
                score = heuristic(board, size, move)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move
    
    # def _minimax_alpha_beta(self, depth, alpha, beta, is_maximizing=True):
    #     if depth == 0 or self.win():
    #         return self._heuristic(self._last_move), self._last_move
        
    #     if is_maximizing:
    #         max_eval = float('-inf')
    #         for move in self._possible_moves():
    #             self._board.board()[move[0]][move[1]] = self._player.cur_player().value
    #             self._player.turn()
    #             tmp = self._last_move
    #             self._last_move = move
    #             eval = self._minimax_alpha_beta(depth - 1, alpha, beta, False)
    #             self._board.board()[move[0]][move[1]] = '_'
    #             self._player.turn()
    #             self._last_move = tmp
    #             # max_eval = max(max_eval, eval)
    #             if eval > max_eval:
    #                 max_eval = eval
    #                 best_move = move
    #             alpha = max(alpha, eval)
    #             if beta <= alpha:
    #                 break
    #         return max_eval, best_move
    #     else:
    #         min_eval = float('inf')
    #         for move in self._possible_moves():
    #             self._board.board()[move[0]][move[1]] = self._player.next_player().value
    #             self._player.turn()
    #             eval = self._minimax_alpha_beta(depth - 1, alpha, beta, True)
    #             self._board.board()[move[0]][move[1]] = '_'
    #             self._player.turn()
    #             # min_eval = min(min_eval, eval)
    #             if eval < min_eval:
    #                 min_eval = eval
    #                 best_move = move
    #             beta = min(beta, eval)
    #             if beta <= alpha:
    #                 break
    #         return min_eval, best_move
        
    # def best_move(self):
    #     return self._minimax_alpha_beta(2, float('-inf'), float('inf'))[1]
        