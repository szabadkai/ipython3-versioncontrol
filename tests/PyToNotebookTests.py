import unittest
from app.PyToNotebook import PyToNotebook


class NotebookToPyTests(unittest.TestCase):
    def test_object_generation(self):
        py2nb = PyToNotebook()
        self.assertIsInstance(py2nb, PyToNotebook)


if __name__ == '__main__':
    unittest.main()
