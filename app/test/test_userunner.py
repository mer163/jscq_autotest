# encoding = utf-8

import random
import unittest

class TestsqeuenceFunctions(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)

    def tearDown(self):
        pass

    @unittest.skip("skipping")
    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)


    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq , 20)
        for element in random.sample(self.seq,5):
            self.assertTrue(element in self.seq)


if __name__ == '__main__':
    # run with main
    # unittest.main

    # 2.run with runner
    # testcase1 = unittest.TestLoader.loadTestsFromTestCase(TestsqeuenceFunctions)
    # suit = unittest.TestSuite(testcase1)
    # unittest.TextTestRunner(verbosity=2).run(suit)

    # 3. order by
    suit = unittest.TestSuite()
    suit.addTest(TestsqeuenceFunctions("test_choice"))
    suit.addTest(TestsqeuenceFunctions("test_sample"))
    runner= unittest.TextTestRunner(verbosity=2)
    runner.run(suit)