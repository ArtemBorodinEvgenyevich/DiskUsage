# -*- coding: utf-8 -*-
""" A module containing a thread class to create a new thread for waiting animation."""
from threading import Thread
import time
import sys


class Spinner(Thread):
    """Class for enabling a new thread with waiting indicator animation.

    .. note::
         Works as a daemon.
    """
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

    def play_animation(self) -> None:
        """Start playing animation until ```self._state``` changed."""
        idx = 0
        print()
        while self._state:
            string = f"Please wait, I'm crawling... {self.animation[idx % len(self.animation)]} \r"
            idx += 1
            self._output.write(string)
            self._output.flush()
            time.sleep(self._time_step)

    def run(self) -> None:
        """Start new thread and repeatedly flush stdout to show animation frames."""
        self.play_animation()

    def stop(self) -> None:
        """Stop and join thread to main and change animation state."""
        self._state = False
        self.join()
