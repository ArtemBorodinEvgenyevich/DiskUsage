import unittest
from threading import Thread
from DiscUsage_Console.DUCore.DUSpinner import Spinner


class TestWaitingSpinner(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.spinner = Spinner(time_step=0.9)

    def test_check_class_attributes(self):
        self.assertEqual(self.spinner._max_play, 0)
        self.assertEqual(self.spinner._min_play, 1)
        self.assertEqual(self.spinner._time_step, 0.9)
        self.assertTrue(self.spinner.daemon, True)

    def test_check_spinnner_instance(self):
        self.assertIsInstance(self.spinner, Thread)

    def test_stop(self):
        self.spinner.start()
        self.spinner.stop()
        self.assertEqual(self.spinner._state, False)


if __name__ == '__main__':
    unittest.main()
