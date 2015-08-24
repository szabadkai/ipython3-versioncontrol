import unittest
from app.NotebookConverter import NotebookToPy


class NotebookToPyTests(unittest.TestCase):
    def test_object_generation(self):
        nb2py = NotebookToPy()
        self.assertIsInstance(nb2py, NotebookToPy)


if __name__ == '__main__':
    unittest.main()
