import unittest
import backend

class Testbackend(unittest.TestCase):
    def test_mtod(self):
        self.debug(backend.run_model)
        