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
        self.player1.hueristicWeights[2] = 1
        self.player1.hueristicWeights[3] = 1
        self.player2.hueristicWeights[2] = 2
        self.player2.hueristicWeights[3] = 2
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
        self.player1.hueristicWeights[4] = 1
        self.player1.hueristicWeights[5] = 1
        self.player1.hueristicWeights[6] = 1
        self.player1.hueristicWeights[7] = 1
        self.player2.hueristicWeights[4] = 1
        self.player2.hueristicWeights[5] = 1
        self.player2.hueristicWeights[6] = 1
        self.player2.hueristicWeights[7] = 1
        self.assertEqual(0, self.player2.score(self.board))
        self.assertEqual(0, self.player1.score(self.board))
        self.board.P1Cups = [2] * self.board.NCUPS
        self.assertEqual(1, self.player2.score(self.board))
        self.assertEqual(-1, self.player1.score(self.board))
        self.board.P1Cups = [0, 1, 0, 1, 0, 1]
        self.assertEqual(0, self.player2.score(self.board))

    def testSumore(self):
        pass

    def testPlayerOne(self):
        self.board.P1Cups = [0, 3, 0, 1, 0, 2]
        self.board.P2Cups = [0, 4, 0, 3, 2, 8]