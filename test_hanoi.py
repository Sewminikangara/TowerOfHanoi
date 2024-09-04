import unittest
from hanoi import hanoi

class TestHanoi(unittest.TestCase):
    def test_hanoi_3_disks(self):
        result = hanoi(3, 'A', 'C', 'B')
        expected = [
                    ('A', 'C'), 
                    ('A', 'B'),
                    ('C', 'B'), 
                    ('A', 'C'),
                    ('B', 'A'),
                    ('B', 'C'),
                    ('A', 'C')
                    ]
        self.assertEqual(result, expected)

    def test_hanoi_1_disk(self):
        result = hanoi(1, 'A', 'C', 'B')
        expected = [('A', 'C')]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
