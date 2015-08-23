import unittest
from app.NotebookToPy import PyGenerator
from app.Notebook import Cell, Notebook


class NotebookToPyTests(unittest.TestCase):
    def test_cell_object(self):
        self.assertRaises(TypeError, Cell, "")

    def test_cell_object_init_source(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        self.assertListEqual(cell.source, ['a', 'b'])

    def test_cell_object_init_cell_type(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        self.assertEquals(cell.cell_type, 'code')

    def test_cell_object_init_missing_celltype(self):
        self.assertRaises(KeyError, Cell, {'source': ['a', 'b']})

    def test_cell_object_init_missing_source(self):
        self.assertRaises(KeyError, Cell, {'cell_type': 'code'})

    def test_cell_object_to_dict_method(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        self.assertDictEqual(cell.to_dict(), {'cell_type': 'code', 'source': ['a', 'b']})

    def test_cell_object_to_generate_output_method(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        assert 'codecell' in cell.generate_field_output()
        # TODO: Maybe it needs a better test more about it when reread is implemented

    def test_notebook_object(self):
        nb = Notebook()
        self.assertIsInstance(nb, Notebook)

    def test_notebook_read_ipynb_file(self):
        nb = Notebook()
        nb.read_notebook("test.ipynb")
        self.assertNotEqual(nb.notebook_format, None)

    def test_notebook_read_ipynb_file_without_cells(self):
        nb = Notebook()
        self.assertRaises(ValueError, nb.read_notebook, "test2.ipynb")

    def test_notebook_read_ipynb_file_cell_loading(self):
        nb = Notebook()
        nb.read_notebook("test.ipynb")
        self.assertGreater(len(nb.cells), 0)

    def test_notebook_read_ipynb_file_cell_type(self):
        nb = Notebook()
        nb.read_notebook("test.ipynb")
        self.assertIsInstance( nb.cells[0], Cell)

    def test_notebook_create_initial_output_no_nbformat(self):
        nb = Notebook()
        self.assertRaises(IOError, nb.create_initial_output, ['', "if '<nmat>' in lines[1]:"])

    def test_notebook_read_ipynb_file_nbformat(self):
        nb = Notebook()
        nb.create_initial_output(open("test.py", 'r').readlines())
        self.assertEquals(nb.notebook_format, 4)


if __name__ == '__main__':
    unittest.main()