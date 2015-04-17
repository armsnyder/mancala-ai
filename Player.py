# File: Player.py
# Author(s) names AND netid's: Michael Nowakowski (mjn912), Adam Snyder (ars123) and Steven Vorbrich (slv398)
# Date: 17 April 2015
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        print "Alpha Beta Move not yet implemented"
        #returns the score adn the associated moved
        return (-1,1)
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType, ply=0,
                 hueristicWeights=(1000, 1000, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)):
        Player.__init__(self, playerNum, playerType, ply)
        self.hueristicWeights = hueristicWeights

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        print "Calling score in MancalaPlayer"
        metrics = [[], []]

        def addMetric(num, playerNum):
            """
            Adds metric to our list of metrics
            :param num: Value of metric
            :param playerNum: Number of player who is benefited
            """
            if playerNum == self.num:
                metrics[0].append(num)
            else:
                metrics[1].append(num)

        # [0] Has player 1 won the game?
        if board.hasWon(1):
            addMetric(1, 1)
        else:
            addMetric(0, 1)

        # [1] Has player 2 won the game?
        if board.hasWon(2):
            addMetric(1, 2)
        else:
            addMetric(0, 2)

        # [2] Number of pieces in player 1's mancala
        addMetric(board.scoreCups[0], 1)

        # [3] Number of pieces in player 2's mancala
        addMetric(board.scoreCups[1], 2)

        # [4] Number of empty holes on player 1's side
        addMetric(sum([1 for cup in board.P1Cups if cup == 0]), 1)

        # [5] Number of empty holes on player 2's side
        addMetric(sum([1 for cup in board.P2Cups if cup == 0]), 2)

        # [6] Number of capturable pieces on player 1's side
        addMetric(sum([board.P1Cups[board.NCUPS-i-1] for i in range(board.NCUPS) if board.P2Cups[i] == 0]), 2)

        # [7] Number of capturable pieces on player 2's side
        addMetric(sum([board.P2Cups[board.NCUPS-i-1] for i in range(board.NCUPS) if board.P1Cups[i] == 0]), 1)

        # [8] Number of holes on player 1's side that can finish on own side
        addMetric(sum([1 for i in range(board.NCUPS)
                       if board.P1Cups[i] != 0 and (board.P1Cups[i] < 6-i or board.P1Cups[i]+i >= 13)]), 1)

        # [9] Number of holes on player 2's side that can finish on own side
        addMetric(sum([1 for i in range(board.NCUPS)
                       if board.P2Cups[i] != 0 and (board.P2Cups[i] < 6-i or board.P2Cups[i]+i >= 13)]), 2)

        # [10] Number of stones on a side (player 1)
        addMetric(sum([board.P1Cups[i] for i in range(board.NCUPS)]), 1)

        # [11] Number of stones on a side (player 2)
        addMetric(sum([board.P2Cups[i] for i in range(board.NCUPS)]), 2)

        # [12] Number plays that would result in an extra turn for player 1
        addMetric(sum([1 for i in range(board.NCUPS) if board.P1Cups[i] == board.NCUPS-i]), 1)

        # [13] Number plays that would result in an extra turn for player 2
        addMetric(sum([1 for i in range(board.NCUPS) if board.P2Cups[i] == board.NCUPS-i]), 2)

        # [14] Max number of stones capturable in this turn for player 1
        possibilities = []
        for i in range(board.NCUPS):
            numPieces = board.P1Cups[i]
            extraPieces = (numPieces+i)/13
            landingPosition = (numPieces+i) % 13
            if (0 < numPieces < 14) and landingPosition < 6 and (board.P1Cups[landingPosition] == 0 or numPieces == 13):
                possibilities.append(1 + board.P2Cups[board.NCUPS-landingPosition-1] + extraPieces)
        addMetric(max(possibilities or [0, 0]), 1)

        # [15] Max number of stones capturable in this turn for player 2
        possibilities = []
        for i in range(board.NCUPS):
            numPieces = board.P2Cups[i]
            extraPieces = (numPieces+i)/13
            landingPosition = (numPieces+i) % 13
            if (0 < numPieces < 14) and landingPosition < 6 and (board.P2Cups[landingPosition] == 0 or numPieces == 13):
                possibilities.append(1 + board.P1Cups[board.NCUPS-landingPosition-1] + extraPieces)
        addMetric(max(possibilities or [0, 0]), 2)

        # Return the sum of the metrics multiplied by their respective weights
        return sum([metrics[0][i] * self.hueristicWeights[i] for i in range(len(metrics[0]))]) - \
            sum([metrics[1][i] * self.hueristicWeights[i+len(metrics[1])] for i in range(len(metrics[1]))])