import unittest
from CakeValuation import DiscreteCakeValuation
from CakeCutting import core

class TestDiscreteCakeValuation(unittest.TestCase):
    
    def test_divide_cake_equally(self):
        values = [2, 3, 1, 4, 5, 1, 1, 0, 2, 1]
        cake = DiscreteCakeValuation(values, 0)
        cuts = cake.divideCakeEqually(4)
        expected = [2, 4, 5]
        self.assertEqual(cuts, expected)

        cuts.insert(0, 0)
        cuts.insert(len(cuts), len(values))
        for i in range(1, len(cuts)):
            cakeValue = cake.evalCakePiece(cuts[i-1], cuts[i])
            print(cuts[i-1], " to ", cuts[i], " value: ", cakeValue)
            self.assertEqual(cakeValue, 5)

    def test_divide_cake_equally_different_values(self):
        values = [1, 1, 1, 1, 1, 1]
        cake = DiscreteCakeValuation(values, 0)
        result = cake.divideCakeEqually(3)
        expected = [2, 4]
        self.assertEqual(result, expected)

    def test_divide_cake_equally_more_people(self):
        values = [10, 20, 30, 40]
        cake = DiscreteCakeValuation(values, 0)
        result = cake.divideCakeEqually(2)
        expected = []
        self.assertEqual(result, expected)

    def test_divide_cake_equally_single_person(self):
        values = [5, 10, 15]
        cake = DiscreteCakeValuation(values, 0)
        result = cake.divideCakeEqually(1)
        expected = []
        self.assertEqual(result, expected)

    def test_divide_cake_equally_no_values(self):
        values = []
        cake = DiscreteCakeValuation(values, 0)
        result = cake.divideCakeEqually(3)
        expected = []
        self.assertEqual(result, expected)

    def test_trim_piece_to_value(self):
        values = [2, 3, 1, 4, 5, 1, 1, 0, 2, 1]
        cake = DiscreteCakeValuation(values, 0)

        result = cake.trimPieceToValue(0, 5, 9)
        expected = 3
        self.assertEqual(result, expected)

        result = cake.trimPieceToValue(0, 2, 5)
        expected = 0
        self.assertEqual(result, expected)

        result = cake.trimPieceToValue(2, 7, 2)
        expected = 5
        self.assertEqual(result, expected)

        result = cake.trimPieceToValue(0, 5, 0)
        expected = 5
        self.assertEqual(result, expected)

class TestSubcore(unittest.TestCase):
    def test_five_player(self):
        agents = [
            DiscreteCakeValuation([1,1,1,1,1,1,2,2,2,3,3,6,6], 0),
            DiscreteCakeValuation([4,4,2,1,1,6,1,1,0,0,0,8,0], 1),
            DiscreteCakeValuation([1,1,2,1,0,1,1,1,3,0,0,4,0], 2),
            DiscreteCakeValuation([1,1,1,4,2,2,4,2,6,2,4,8,0], 3),
            DiscreteCakeValuation([1,1,1,1,5,1,1,0,0,0,3,3,12], 4)
        ]

        cake = (0, 13)
        allocation = core(0, agents, cake)

        # Check that each agent got a piece that they valued the highest
        for piece, agent in allocation.items():
            if (agent == -1):
                continue
            print(piece, " -> ", agent)
            pieceValue = agents[agent].evalCakePiece(piece[0], piece[1])
            for otherPiece, otherAgent in allocation.items():
                if (otherAgent != -1 and agent != otherAgent):
                    print("Comparing agent ", agents[agent].getId(),"'s piece ", piece, " to agent ", agents[otherAgent].getId(), "'s piece ", otherPiece)
                    self.assertGreaterEqual(pieceValue, agents[agent].evalCakePiece(otherPiece[0], otherPiece[1]))

        


if __name__ == '__main__':
    unittest.main()