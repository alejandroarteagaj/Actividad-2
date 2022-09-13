import unittest
import backend

class Testbackend2(unittest.TestCase):
    def test_mtod(self):
        self.debug(backend.load_img_file)
        