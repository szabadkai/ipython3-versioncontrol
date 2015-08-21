import unittest
import os
from app.NotebookToPy import PyGenerator, Cell


class NotebookToPyTests(unittest.TestCase):
    pyGenerator = PyGenerator()

    def test_read_notebook_method(self):
        notebook = self.pyGenerator.read_notebook("test.ipynb")
        assert len(notebook)>0

    def test_unavailable_file_loading(self):
        self.assertRaises(IOError, self.pyGenerator.read_notebook, "")

    def test_file_path_construction(self):
        output_path = self.pyGenerator.construct_output_path("test.ipynb");
        assert output_path == "test.py"

    def test_cell_object(self):
        test_dict = {"cell_type":"code", "source":"lkjashdkjahfslkdjlhfas"}
        cell = Cell(test_dict)
        assert cell.cell_type == "code"

    def test_empty_cel(self):
        test_dict = {}
        self.assertRaises(KeyError, Cell, test_dict

    def test_write_header(self):
        with open("testfile", 'w') as output:
            PyGenerator.add_header(output, str(4))
        assert os.path.exists("testfile")


if __name__ == '__main__':
    unittest.main()
