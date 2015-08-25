import unittest
from app.NotebookConverter import NotebookConverter


class NotebookToPyTests(unittest.TestCase):
    def test_object_generation(self):
        nbconverter = NotebookConverter()
        self.assertIsInstance(nbconverter, NotebookConverter)

if __name__ == '__main__':
    unittest.main()
