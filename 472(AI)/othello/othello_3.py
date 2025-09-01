from collections import namedtuple

import numpy as np


GameState = namedtuple('GameState', 'to_move, utility, board, moves')


#Game Class from AIMA
class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        num_players = len(players)
        skipped_turns = 0  # Add a counter for skipped turns

        while True:
            for i, player in enumerate(players):
                move = player(self, state)
                if move is not None:
                    state = self.result(state, move)
                    skipped_turns = 0  # Reset skipped turns counter
                else:
                    skipped_turns += 1  # Increment skipped turns counter

                if self.terminal_test(state) or skipped_turns == num_players:
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))
                    

#Child class for Othello. Using Game class from the AIMA
class Othello(Game):
    def __init__(self, h=8, v=8):
        self.board = self.initial_board()
        initial_state = GameState(to_move=1, utility=0, board=self.board, moves=[])
        valid_moves = self.actions(initial_state)
        self.initial = initial_state._replace(moves=valid_moves)


    #Set inital othello board. 4 componenmt set. 
    #Board dimension 8x8
    # 0=nothing, 1=player1, 2=player2
    def initial_board(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return board


    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        actions = []
        for y in range(8):
            for x in range(8):
                if self.possible_check(y, x, state.to_move, 3-state.to_move, state.board):
                    actions.append((y, x))
        return actions
        
    #Return boolean.
    def possible_check(self, y, x, player, opponent, board):
        if board[y][x] != 0:
            return False
        
        #check all direction
        check = False
        directions = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy != 0 or dx != 0]
        for dy, dx in directions:
            temp_y, temp_x = y + dy, x + dx
            if 0 <= temp_y < 8 and 0 <= temp_x < 8 and board[temp_y][temp_x] == opponent:
                while 0 <= temp_y < 8 and 0 <= temp_x < 8:
                    if board[temp_y][temp_x] == opponent:
                        temp_y += dy
                        temp_x += dx
                    elif board[temp_y][temp_x] == player:
                        check = True
                        break
                    else:
                        break
        return check
    
    
    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        y, x = move
        new_board = [row.copy() for row in state.board]
        current_player = state.to_move
        self.apply_move(y, x, current_player, new_board)

        next_player = 3 - current_player
        next_moves = self.actions(GameState(to_move=next_player, utility=0, board=new_board, moves=[]))

        return GameState(to_move=next_player, utility=0, board=new_board, moves=next_moves)


    def apply_move(self, y, x, player, board):
        opponent = 3 - player
        board[y][x] = player

        for dy, dx in [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy != 0 or dx != 0]:
            temp_y, temp_x = y + dy, x + dx
            if 0 <= temp_y < 8 and 0 <= temp_x < 8 and board[temp_y][temp_x] == opponent:
                while 0 <= temp_y < 8 and 0 <= temp_x < 8:
                    if board[temp_y][temp_x] == opponent:
                        temp_y += dy
                        temp_x += dx
                    elif board[temp_y][temp_x] == player:
                        while (temp_y != y or temp_x != x):
                            temp_y -= dy
                            temp_x -= dx
                            board[temp_y][temp_x] = player
                        break
                    else:
                        break




    def utility(self, state, player):
         """Return the score difference"""
         board = state.board
         player1, player2 = self.score(board)
         if player == 1:
            return player1 - player2
         else:
            return player2 - player1

    #Return the score. Count number of 1s and 2s
    def score(self, board):
        player1_score = 0
        player2_score = 0

        for row in board:
            for cell in row:
                if cell == 1:
                    player1_score += 1
                elif cell == 2:
                    player2_score += 1

        return player1_score, player2_score
    
    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        if len(state.moves) == 0:
            next_player = 3 - state.to_move
            next_moves = self.actions(GameState(to_move=next_player, utility=0, board=state.board, moves=[]))
            if len(next_moves) == 0:
                return True
        return False
        
    #display the given board.
    #Transfer 0, 1 and 2 into symbols
    #Make grid a~h and 1~8
    def display(self, state):
        print("+========= player 1: ○ || player 2: ● =========+")
        print("  1  2  3  4  5  6  7  8")
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, row in enumerate(state.board):
            row_string = letters[i] + " "
            for cell in row:
                if cell == 0:
                    row_string += ".  "
                elif cell == 1:
                    row_string += "○  "
                elif cell == 2:
                    row_string += "●  "
                else:
                    print("X")
            print(row_string)
        print("##Score## ○: {} || ●: {} ".format(*self.score(state.board)))

#Function to convert alphabet to the number
def convert(coor):
    if coor == 'a':
        return 0
    elif coor == 'b':
        return 1
    elif coor == 'c':
        return 2
    elif coor == 'd':
        return 3 
    elif coor == 'e':
        return 4
    elif coor == 'f':
        return 5
    elif coor == 'g':
        return 6
    elif coor == 'h':
        return 7
    else:
        print("Invalid alphabet coordinate. Range:[a-h]")   

#Function to convert number to alphabet
def inverse_convert(coor):
    if coor == 0:
        return 'a'
    elif coor == 1:
        return 'b'
    elif coor == 2:
        return 'c'
    elif coor == 3:
        return 'd'
    elif coor == 4:
        return 'e'
    elif coor == 5:
        return 'f'
    elif coor == 6:
        return 'g'
    elif coor == 7:
        return 'h'
    else:
        print("##inverse_convert function error##")   

#Function to play as a human. Recieves the input from the user.
def human_player(game, state):
    game.display(state)
    legal_moves = game.actions(state)
    move = None
    while move not in legal_moves:
        try:
            user_input = input("Enter move without space [alphabet num] (ex: a3): ").lower()
            garo, sero = user_input[0], int(user_input[1]) - 1
            garo = convert(garo)
            move = (garo, sero)
            if move not in legal_moves:
                print("Invalid move.")
        except (ValueError, IndexError):
            print("Invalid format (ex: c5)")

    return move

#Function to make cpu as a player. Uses alpha-beta cutoff function.
def ai_player(game, state):
    game.display(state)
    legal_moves = game.actions(state)
    best_move = alpha_beta_cutoff_search(state, game)
    
    if best_move in legal_moves:
        state = game.result(state, best_move)  
        print(f"CPU input: {inverse_convert(best_move[0])}{best_move[1] + 1}")
        return best_move
    else:
        print("CPU invalid move.")
        if legal_moves:
            return legal_moves[0]
        else:
            print("No valid movement")
            return None

#Function to use alpha-beta cutoff with deeper depth.
def better_ai_player(game, state):
    game.display(state)
    legal_moves = game.actions(state)
    best_move = alpha_beta_cutoff_search_ver(state, game)
    
    if best_move in legal_moves:
        state = game.result(state, best_move)  
        print(f"CPU input: {inverse_convert(best_move[0])}{best_move[1] + 1}")
        return best_move
    else:
        print("CPU invalid move.")
        if legal_moves:
            return legal_moves[0]
        else:
            print("No valid movement")
            return None
        
#Function to use weight as a evaluation function.
def weight_ai_player(game, state):
    game.display(state)
    legal_moves = game.actions(state)
    best_move = alpha_beta_cutoff_search(state, game, eval_fn=weight_heuristic)
    
    if best_move in legal_moves:
        state = game.result(state, best_move)  
        print(f"CPU input: {inverse_convert(best_move[0])}{best_move[1] + 1}")
        return best_move
    else:
        print("CPU invalid move.")
        if legal_moves:
            return legal_moves[0]
        else:
            print("No valid movement")
            return None

#Function to use movement left as a evaluation function.
def movement_ai_player(game, state):
    game.display(state)
    legal_moves = game.actions(state)
    best_move = alpha_beta_cutoff_search(state, game, eval_fn=lambda state: movement_heuristic(game, state))
    
    if best_move in legal_moves:
        state = game.result(state, best_move)  
        print(f"CPU input: {inverse_convert(best_move[0])}{best_move[1] + 1}")
        return best_move
    else:
        print("CPU invalid move.")
        if legal_moves:
            return legal_moves[0]
        else:
            print("No valid movement")
            return None

#-------------------------------------------------------------------------------------#
# Alpha-beta cut off from AIMA 
def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in state.moves:
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in state.moves:
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in state.moves:
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

#-------------------------------------------------------------------------------------#


#Modified Aima alpha-beta cut off with deeper depth. 
def alpha_beta_cutoff_search_ver(state, game, d=8, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in state.moves:
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in state.moves:
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in state.moves:
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


#Setting weight on the graph. Corner gets the highest value.
def weight_heuristic(state):
    board = state.board
    player = state.to_move
    opponent = 3 - player

    weights = [
        [20, 1, 5, 4, 4, 5, 1, 20],
        [1, -10, -1, -1, -1, -1, -10, 1],
        [5, -1, 0, 0, 0, 0, -1, 5],
        [4, -1, 0, 0, 0, 0, -1, 4],
        [4, -1, 0, 0, 0, 0, -1, 4],
        [5, -1, 0, 0, 0, 0, -1, 5],
        [1, -10, -1, -1, -1, -1, -10, 1],
        [20, 1, 5, 4, 4, 5, 1, 20]
    ]

    weight = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == player:
                weight += weights[y][x]
            elif board[y][x] == opponent:
                weight -= weights[y][x]

    return weight


#Function to count number of the movements.
def movement_heuristic(game, state):
    player_moves = len(game.actions(state))
    
    actions = game.actions(state)
    if actions:
        # Assume the opponent is the next player after applying any legal move
        opponent_state = game.result(state, actions[0])
        opponent_moves = len(game.actions(opponent_state))
    else:
        # Handle the case when there are no available actions
        opponent_moves = 0

    return player_moves - opponent_moves


#Main function to run
def main():
    game = Othello()


    '''
    Comment out to choose different style of players
    '''

    '''
    Player 1
    '''
    #Choose player 1 method
    player1 = human_player              #Played by the uswer
    #player1 = ai_player                  #Played by the alpha-beta original
 


    '''
    Player 2
    '''
    #Choose player 2 method
    player2 = ai_player                  #Played by original alpha-beta by cpu
    #player2 = human_player               #Played by the user 
    #player2 = better_ai_player            #Played by the better alpha-beta by cpu. Increased depth to 8
    #player2 = weight_ai_player           #Played by the 2nd eval function (weight)
    #player2 = movement_ai_player         #Played by the 3rd eval function (number of possible movement)
    



    result = game.play_game(player1, player2)

    print("Result: ", result)
    if result > 0:
        print("Player 1 win")
    elif result == 0:
        print("draw")
    else:
        print("CPU (player 2) win")


print("--------------------------------------------------")
main()


