import unittest
from lib import psystem


class TestCases(unittest.TestCase):
    def test_same_type(self):
        self.assertFalse(psystem.same_type(None))
        self.assertFalse(psystem.same_type([]))
        self.assertFalse(psystem.same_type({}))
        self.assertFalse(psystem.same_type(''))
        self.assertFalse(psystem.same_type(set()))
        self.assertFalse(psystem.same_type(()))
        self.assertTrue(psystem.same_type((1,2,3)))
        self.assertTrue(psystem.same_type([1.1,2.2,3.3]))
        self.assertTrue(psystem.same_type(("A","""B""", 'C')))
        self.assertTrue(psystem.same_type({True, False}))
        self.assertTrue(psystem.same_type({None, None}))
        self.assertFalse(psystem.same_type({1, 2, None}))
        self.assertFalse(psystem.same_type({1, 2.2, 3}))
        self.assertFalse(psystem.same_type({"1", 2, 3}))


if __name__ == '__main__':
    unittest.main()
