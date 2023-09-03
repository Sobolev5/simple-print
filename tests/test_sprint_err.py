import unittest
import logging
from unittest.mock import patch
from unittest.mock import MagicMock
from simple_print import SprintErr


class TestSprintErr(unittest.TestCase):
    # pytest test/test_sprint_err.py -rP

    @patch('logging.info', MagicMock(side_effect=[Exception("Something went wrong")]))
    def test_sprint_err(self):
        with SprintErr():
            logging.info("")
