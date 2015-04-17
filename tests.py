import unittest

import Player
import MancalaBoard


class TestExample(unittest.TestCase):

    def testExample(self):
        player = Player.Player(1, Player.Player.HUMAN)
        self.assertEqual(Player.Player.HUMAN, player.type)


class TestScoring(unittest.TestCase):

    def setUp(self):
        self.board = MancalaBoard.MancalaBoard()
        self.player1 = Player.MancalaPlayer(1, Player.Player.CUSTOM)
        self.player2 = Player.MancalaPlayer(2, Player.Player.CUSTOM)

    def testScoreBasic(self):
        self.assertEqual(0, self.player1.score(self.board))

    def testScoreMancalas(self):
        self.assertEqual(0, self.player1.score(self.board))
        self.assertEqual(0, self.player2.score(self.board))
        self.player1.hueristicWeights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(0, self.player1.score(self.board))
        self.assertEqual(0, self.player2.score(self.board))
        self.board.scoreCups[0] = 1
        self.assertEqual(1, self.player1.score(self.board))
        self.assertEqual(-2, self.player2.score(self.board))
        self.board.scoreCups[1] = 10
        self.assertEqual(-9, self.player1.score(self.board))
        self.assertEqual(18, self.player2.score(self.board))

    def testScoreEmptyCups(self):
        self.assertEqual(0, self.player2.score(self.board))
        self.board.P1Cups = [0] * self.board.NCUPS
        self.board.P2Cups = [0] * self.board.NCUPS
        self.assertEqual(0, self.player2.score(self.board))
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
        self.player1.hueristicWeights = [100, 100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.player2.hueristicWeights = [100, 100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(144, self.player1.score(self.board))
        self.assertEqual(-144, self.player2.score(self.board))