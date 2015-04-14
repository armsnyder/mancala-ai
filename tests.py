import unittest

import Player


class TestExample(unittest.TestCase):

    def testExample(self):
        player = Player.Player(1, Player.Player.HUMAN)
        self.assertEqual(Player.Player.HUMAN, player.type)