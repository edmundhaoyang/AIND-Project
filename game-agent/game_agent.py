"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    center = game.width/2

    own_position = game.get_player_location(player)
    opp_position = game.get_player_location(game.get_opponent(player))

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_dist_x = abs(center - own_position[0])
    own_dist_y = abs(center - own_position[1])

    opp_dist_x = abs(center - opp_position[0])
    opp_dist_y = abs(center - opp_position[1])

    return float(10 * (own_moves - opp_moves) +
                 (own_dist_x + own_dist_y) - (opp_dist_x + opp_dist_y))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
 
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    # We have moves to play. How many more than our opponent?
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - opp_moves)



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    # We have moves to play. How many more than our opponent?
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if own_moves != opp_moves:
        return float(own_moves - opp_moves)

    else:
        center_y_pos, center_x_pos = int(game.height / 2), int(game.width / 2)
        player_y_pos, player_x_pos = game.get_player_location(player)
        opponent_y_pos, opponent_x_pos = game.get_player_location(game.get_opponent(player))
        player_distance = abs(player_y_pos - center_y_pos) + abs(player_x_pos - center_x_pos)
        opponent_distance = abs(opponent_y_pos - center_y_pos) + abs(opponent_x_pos - center_x_pos)
        
        return float(opponent_distance - player_distance) / 10.


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_search_function(self):
        search_function = self.minimax
        if self.method == 'alphabeta':
            search_function = self.alphabeta
        if self.method == 'negamax':
            search_function = self.negamax
        return search_function

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        best_move = (-1, -1)

        if len(legal_moves) == 0:
            return best_move

        search_function = self.get_search_function()

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if not self.iterative:
                bset_val, best_move = search_function(game, depth=self.search_depth)
            else:
                bset_val, d = 0, 0
                while True:
                    # abs(v) != float("Inf") ok but we can use all the time
                    bset_val, best_move = search_function(game, depth=d)
                    d = d + 1

        except Timeout:
            # Handle any actions required at timeout, if necessary
            if (best_move == (-1, -1)):
                best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        current_depth : int
            current_depth is an integer representing the number of plies

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        bestMove = (-1, -1)

        if maximizing_player == 1:
            player_to_maximize = game.active_player
        else:
            player_to_maximize = game.inactive_player

        if (depth == 0):
            return self.score(game, player_to_maximize), bestMove

        if game.utility(player_to_maximize) != 0.0:
            return game.utility(player_to_maximize), bestMove

        legalMoves = game.get_legal_moves(game.active_player)
        bestMove = legalMoves[0]

        if maximizing_player:
            bestValue = float("-Inf")

            for m in legalMoves:
                v, _ = self.minimax(game.forecast_move(m), depth - 1, False)
                if v > bestValue:
                    bestValue = v
                    bestMove = m
            return bestValue, bestMove

        else:
            bestValue = float("Inf")

            for m in legalMoves:
                v, _ = self.minimax(game.forecast_move(m), depth - 1, True)
                if v < bestValue:
                    bestValue = v
                    bestMove = m
            return bestValue, bestMove

    def alphabeta(self, game, depth, alpha=float("-inf"),
                  beta=float("inf"), maximizing_player=True):

        if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

        bestMove = (-1, -1)

        if maximizing_player == 1:
            player_to_maximize = game.active_player
        else:
            player_to_maximize = game.inactive_player

        if (depth == 0):
            return self.score(game, player_to_maximize), bestMove

        if game.utility(player_to_maximize) != 0.0:
            return game.utility(player_to_maximize), bestMove

        legal_moves = game.get_legal_moves(game.active_player)
        bestMove = legal_moves[0]

        if maximizing_player:
            v = float("-Inf")

            for m in legal_moves:
                newv, _ = self.alphabeta(game.forecast_move(m),
                                         depth - 1, alpha, beta, False)
                if newv > v:
                    v = newv
                    bestMove = m
                if v > alpha:
                    alpha = v
                    bestMove = m
                if beta <= alpha:
                    break  # beta cut-off
            return v, bestMove

        else:
            v = float("Inf")
            for m in legal_moves:
                newv, _ = self.alphabeta(game.forecast_move(m),
                                         depth - 1, alpha, beta, True)
                if newv < v:
                    v = newv
                    bestMove = m
                if v < beta:
                    beta = v
                    bestMove = m
                if beta <= alpha:
                    break  # beta cut-off
            return v, bestMove

   