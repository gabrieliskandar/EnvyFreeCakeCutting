import unittest
from DiscreteCakeValuation import DiscreteCakeValuation

class TestDiscreteCakeValuation(unittest.TestCase):
    
    def test_divide_cake_equally(self):
        values = [2, 3, 1, 4, 5, 1, 1, 0, 2, 1]
        cake = DiscreteCakeValuation(values)
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
        cake = DiscreteCakeValuation(values)
        result = cake.divideCakeEqually(3)
        expected = [2, 4]
        self.assertEqual(result, expected)

    def test_divide_cake_equally_more_people(self):
        values = [10, 20, 30, 40]
        cake = DiscreteCakeValuation(values)
        result = cake.divideCakeEqually(2)
        expected = []
        self.assertEqual(result, expected)

    def test_divide_cake_equally_single_person(self):
        values = [5, 10, 15]
        cake = DiscreteCakeValuation(values)
        result = cake.divideCakeEqually(1)
        expected = []
        self.assertEqual(result, expected)

    def test_divide_cake_equally_no_values(self):
        values = []
        cake = DiscreteCakeValuation(values)
        result = cake.divideCakeEqually(3)
        expected = []
        self.assertEqual(result, expected)

    def test_trim_piece_to_value(self):
        values = [2, 3, 1, 4, 5, 1, 1, 0, 2, 1]
        cake = DiscreteCakeValuation(values)

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

if __name__ == '__main__':
    unittest.main()