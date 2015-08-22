import unittest
from app.NotebookToPy import PyGenerator, Cell, Notebook


class NotebookToPyTests(unittest.TestCase):
    pyGenerator = PyGenerator()
    nb = Notebook()

    def test_read_notebook_method(self):
        self.nb.read_notebook("test.ipynb")
        assert len(self.nb.cells) > 0

    def test_unavailable_file_loading(self):
        self.assertRaises(IOError, self.nb.read_notebook, "")

    def test_file_path_construction(self):
        output_path = self.pyGenerator.construct_output_path("test.ipynb");
        assert output_path == "test.py"

    def test_cell_object(self):
        test_dict = {"cell_type":"code", "source":"lkjashdkjahfslkdjlhfas"}
        cell = Cell(test_dict)
        assert cell.cell_type == "code" and cell.source == "lkjashdkjahfslkdjlhfas"

    def test_empty_cel(self):
        test_dict = {}
        self.assertRaises(KeyError, Cell, test_dict)

    def test_read_py(self):
        self.nb = Notebook()
        with open("test.py", 'r') as input:
            self.nb.read_cells_from_py(input)
        test_nb = Notebook()
        test_nb.read_notebook("test.ipynb")
        assert len(self.nb.cells) == len(test_nb.cells)
        for i in range(len(self.nb.cells)):
            assert self.nb.cells[i].cell_type == test_nb.cells[i].cell_type



if __name__ == '__main__':
    unittest.main()
