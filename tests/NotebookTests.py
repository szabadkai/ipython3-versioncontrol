import unittest
from app.Notebook import Cell, Notebook


class NotebookTests(unittest.TestCase):
    def test_cell_object(self):
        self.assertRaises(TypeError, Cell, "")

    def test_cell_object_init_source(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        self.assertListEqual(cell.source, ['a', 'b'])

    def test_cell_object_init_cell_type(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        self.assertEquals(cell.type, 'code')

    def test_cell_object_init_missing_celltype(self):
        self.assertRaises(KeyError, Cell, {'source': ['a', 'b']})

    def test_cell_object_init_missing_source(self):
        self.assertRaises(KeyError, Cell, {'cell_type': 'code'})

    def test_cell_object_to_dict_method(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        self.assertDictEqual(cell.to_dict(), {'cell_type': 'code', 'source': ['a', 'b']})

    def test_cell_object_to_generate_output_method(self):
        cell = Cell({'cell_type': 'code', 'source': ['a', 'b']})
        print cell.generate_field_output()
        self.assertEquals('\n# <codecell>\n\nab\n', cell.generate_field_output())

    def test_notebook_object(self):
        nb = Notebook()
        self.assertIsInstance(nb, Notebook)

    def test_notebook_read_ipynb_file(self):
        nb = Notebook()
        nb.read_notebook("tests/test.ipynb")
        self.assertNotEqual(nb.notebook_format, None)

    def test_notebook_read_ipynb_file_without_cells(self):
        nb = Notebook()
        self.assertRaises(ValueError, nb.read_notebook, "tests/test2.ipynb")

    def test_notebook_read_ipynb_file_cell_loading(self):
        nb = Notebook()
        nb.read_notebook("tests/test.ipynb")
        self.assertGreater(len(nb.cells), 0)

    def test_notebook_read_py_file_cell_loading(self):
        nb = Notebook()
        nb.read_py("tests/test.py")
        self.assertGreater(len(nb.cells), 0)

    def test_notebook_read_ipynb_file_cell_type(self):
        nb = Notebook()
        nb.read_notebook("tests/test.ipynb")
        self.assertIsInstance( nb.cells[0], Cell)

    def test_notebook_read_py_as_notebook_error(self):
        nb = Notebook()
        self.assertRaises(ValueError,  nb.read_notebook, "tests/test.py")

    def test_notebook_add_descriptive_data_no_nbformat(self):
        nb = Notebook()
        self.assertRaises(IOError, nb.add_descriptive_data, ['', "if '<nmat>' in lines[1]:"])

    def test_notebook_read_ipynb_file_nbformat(self):
        nb = Notebook()
        nb.add_descriptive_data(open("tests/test.py", 'r').readlines())
        self.assertEquals(nb.notebook_format, 4)

    def test_notebook_to_dict_method(self):
        nb = Notebook()
        nb.add_descriptive_data(['', "# <nbformat>4</nbformat>"])
        self.assertEquals(nb.to_dict()["nbformat"], 4)

    def test_if_notebooks_are_the_same_from_different_input_types(self):
        nb = Notebook()
        nb.read_notebook("tests/test.ipynb")
        nb2 = Notebook()
        nb2.read_py("tests/test.py")
        assert nb.to_dict() == nb.to_dict()

if __name__ == '__main__':
    unittest.main()