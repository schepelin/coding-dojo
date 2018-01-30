#
import unittest

from solution import Life


class SolutionTestCase(unittest.TestCase):

    def test_grid_initialization(self):
        input = [
            '***#*',
            '*#*#*',
            '*#*#*',
            '*###*',
            '#*##*',
        ]

        new_life = Life(input)
        self.assertEqual(input, new_life.state)

    def test_get_neighbours_on_edge_cell(self):
        input = [
            '#*',
            '**'
        ]
        life = Life(input)
        neighbours_count = life.get_alive_neighbours_count(0, 0)
        self.assertEqual(neighbours_count, 0)
        neighbours_count = life.get_alive_neighbours_count(0, 1)
        self.assertEqual(neighbours_count, 1)

    def test_get_neighbours_on_inner_cell(self):
        input = [
            '#*#',
            '***',
            '***',
        ]
        life = Life(input)
        neighbours_count = life.get_alive_neighbours_count(1, 1)
        self.assertEqual(neighbours_count, 2)

    def test_first_rule_survive(self):
        input = [
            '#*#',
            '***',
            '***',
        ]
        life = Life(input)
        actual = life.will_cell_survive_after_first_rule(0, 1)
        self.assertTrue(actual)

    def test_first_rule_dies(self):
        input = [
            '#*#',
            '***',
            '***',
        ]
        life = Life(input)
        actual = life.will_cell_survive_after_first_rule(0, 0)
        self.assertFalse(actual)
        self.assertIsNotNone(actual)

    def test_second_rule(self):
        input = [
            '###',
            '###',
            '#**',
        ]
        life = Life(input)
        actual = life.will_cell_die_after_second_rule(0, 1)
        self.assertTrue(actual)
        actual = life.will_cell_die_after_second_rule(2, 0)
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()

# инициализировать сетку игры
# применить правила 1-4
# вернуть новое состояние

