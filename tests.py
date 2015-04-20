import unittest
import time

import slv398
import MancalaBoard


class TestExample(unittest.TestCase):

    def testExample(self):
        player = slv398.Player(1, slv398.Player.HUMAN)
        self.assertEqual(slv398.Player.HUMAN, player.type)


class TestScoring(unittest.TestCase):

    def setUp(self):
        self.board = MancalaBoard.MancalaBoard()
        self.player1 = slv398.slv398(1, slv398.Player.CUSTOM)
        self.player2 = slv398.slv398(2, slv398.Player.CUSTOM)

    def testScoreMancalas(self):
        self.player1.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1]
        self.assertEqual(0, self.player1.score(self.board))
        self.assertEqual(0, self.player2.score(self.board))
        self.board.scoreCups[0] = 1
        self.assertEqual(1, self.player1.score(self.board))
        self.assertEqual(-2, self.player2.score(self.board))
        self.board.scoreCups[1] = 10
        self.assertEqual(-9, self.player1.score(self.board))
        self.assertEqual(18, self.player2.score(self.board))

    def testScoreEmptyCups(self):
        self.board.P1Cups = [0] * self.board.NCUPS
        self.board.P2Cups = [0] * self.board.NCUPS
        self.board.P1Cups = [1] * self.board.NCUPS
        self.player1.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(0, self.player2.score(self.board))
        self.assertEqual(0, self.player1.score(self.board))
        self.board.P1Cups = [2] * self.board.NCUPS
        self.assertEqual(1, self.player2.score(self.board))
        self.assertEqual(-1, self.player1.score(self.board))
        self.board.P1Cups = [0, 1, 0, 1, 0, 1]
        self.assertEqual(-1, self.player2.score(self.board))

    def testSumore(self):
        self.board.P1Cups = [0, 3, 0, 1, 0, 2]
        self.board.P2Cups = [0, 4, 0, 3, 2, 8]
        self.board.scoreCups = [4, 2]
        self.player1.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(3, self.player1.score(self.board))
        self.assertEqual(-3, self.player2.score(self.board))

    def testBigPlays(self):
        self.board.P1Cups = [0, 0, 14, 3, 8, 10]
        self.board.P2Cups = [1, 13, 4, 0, 12, 0]
        self.board.scoreCups = [4, 9]
        self.player1.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(-19, self.player1.score(self.board))
        self.assertEqual(19, self.player2.score(self.board))

    def testOne(self):
        self.board.P1Cups = [0, 0, 0, 0, 0, 0]
        self.board.P2Cups = [0, 0, 0, 0, 0, 0]
        self.board.scoreCups = [46, 2]
        self.player1.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(slv398.WINNING_SCORE, self.player1.score(self.board))
        self.assertEqual(-44, self.player2.score(self.board))


class TestAlphaBeta(unittest.TestCase):

    def setUp(self):
        self.board = MancalaBoard.MancalaBoard()
        self.player1 = slv398.slv398(1, slv398.Player.MINIMAX, 3)
        self.player2 = slv398.slv398(2, slv398.Player.ABPRUNE, 3)

    def testFirstMove(self):
        self.board.reset()
        player1_score, player1_move = self.player1.minimaxMove(self.board, 1)
        self.board.reset()
        player2_score, player2_move = self.player2.alphaBetaMove(self.board, 1)
        self.assertEqual(player1_move, player2_move)
        self.assertEqual(player1_score, player2_score)

    def testSecondMove(self):
        self.board.reset()
        player1_score, player1_move = self.player1.minimaxMove(self.board, 2)
        self.board.reset()
        player2_score, player2_move = self.player2.alphaBetaMove(self.board, 2)
        self.assertEqual(player1_move, player2_move)
        self.assertEqual(player1_score, player2_score)

    def testThirdMove(self):
        self.board.reset()
        player1_score, player1_move = self.player1.minimaxMove(self.board, 3)
        self.board.reset()
        player2_score, player2_move = self.player2.alphaBetaMove(self.board, 3)
        self.assertEqual(player1_move, player2_move)
        self.assertEqual(player1_score, player2_score)

    def testWins(self):
        self.board.P1Cups = [0, 0, 1, 0, 0, 0]
        self.board.P2Cups = [5, 4, 0, 2, 1, 0]
        self.board.scoreCups = [15, 5]
        self.player1 = slv398.slv398(1, slv398.Player.CUSTOM)
        self.player2 = slv398.slv398(2, slv398.Player.CUSTOM)
        self.player1.hueristicWeights = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        self.player2.hueristicWeights = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        self.assertEqual(-1, self.player1.searchTree(self.board, 6, time.time())[0])
        self.assertEqual(slv398.WINNING_SCORE, self.player2.searchTree(self.board, 6, time.time())[0])