# -*- coding: utf-8 -*-
from threading import Thread
import time
import sys


class Spinner(Thread):
    """Waiting indicator."""
    def __init__(self, max_play=0, min_play=1, time_step=0.5):
        """

        :param max_play:
        :param min_play:
        :param time_step:
        """
        super().__init__()

        self.animation = ["|o_o|", "|o_-|", "|o_o|", "|-_o|", "|o_o|", "|-_-|", "|^_^|", "|-_-|",
                          "|o_o|", "|O_o|", "|o_o|", "|o_O|", "|o_o|", "|O_O|", "|0_0|", "|O_O|", ]
        self._output = sys.stdout
        self._state = True
        self._max_play = max_play
        self._min_play = min_play
        self._time_step = time_step
        self._count = 0

        self.daemon = True

    def play_animation(self):
        """

        :return:
        """
        idx = 0
        print()
        while self._state:
            string = f"Please wait, I'm crawling... {self.animation[idx % len(self.animation)]} \r"
            idx += 1
            self._output.write(string)
            self._output.flush()
            time.sleep(self._time_step)

    def run(self):
        """

        :return:
        """
        self.play_animation()

    def stop(self):
        """

        :return:
        """
        self._state = False
        self.join()
