#!/usr/bin/env python3
import unittest

from day4_part2 import length_is_not_six, has_adjacent_digits, has_decreasing_digits, has_adjacent_digit_group

class TestDay4InputPatterns(unittest.TestCase):

    def test_length_is_not_six(self):
        self.assertTrue(length_is_not_six(12345))
        self.assertFalse(length_is_not_six(123456))
        self.assertTrue(length_is_not_six(1234567))

    def test_has_adjacent_digits(self):
        self.assertTrue(has_adjacent_digits(111111))
        self.assertFalse(has_adjacent_digits(123789))

    def test_has_decreasing_digits(self):
        self.assertFalse(has_decreasing_digits(111111))
        self.assertTrue(has_decreasing_digits(223450))

    def test_has_adjacent_digit_group(self):
        self.assertFalse(has_adjacent_digit_group(112233))
        self.assertTrue(has_adjacent_digit_group(123444))
        self.assertFalse(has_adjacent_digit_group(111122))


if __name__ == '__main__':
    unittest.main()
