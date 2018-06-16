
import unittest
from set_solver import Game


class SetSolverTests(unittest.TestCase):

    def test_cards_generated(self):
        g = Game(card_count=81)
        assert len(g.find_sets(3)) == 1080

    def test_cards_provided(self):
        data = 'red 1 diamond stripe, red 1 oval stripe, red 2 squiggle outline, red 2 diamond stripe, purple 1 oval stripe, purple 1 squiggle solid, green 2 oval outline, green 3 squiggle stripe, red 2 squiggle stripe, red 2 squiggle solid, red 2 oval solid, green 3 oval outline'
        g = Game(cards_input=data)
        assert g.find_sets(cards_per_set=3) == [[2, 3, 10], [2, 5, 7], [2, 8, 9], [3, 4, 7], [3, 5, 11], [4, 10, 11]]

    def test_extra_dimension(self):
        g = Game(cards_input='0 0 0 0 0, 1 1 1 1 1, 2 2 2 2 0')
        assert len(g.find_sets(cards_per_set=3)) == 0
        g = Game(cards_input='0 0 0 0 0, 1 1 1 1 1, 2 2 2 2 2')
        assert len(g.find_sets(cards_per_set=3)) == 1

    def test_n_cards_per_set(self):
        for n in range(2, 7):
            card_input = ','.join([(str(i) + ' ') * 5 for i in range(n)])
            g = Game(cards_input=card_input)
            assert len(g.find_sets(cards_per_set=n)) == 1

    def test_invalid_cards_differ_dimension_count(self):
        with self.assertRaises(Exception):
            data= '0 1, 0'
            Game(card_count=3, cards_input=data)

    def test_invalid_duplicate(self):
        with self.assertRaises(Exception):
            data = '0 0 0, 0 0 0'
            Game(card_count=3, cards_input=data)
            g.find_sets(2)
