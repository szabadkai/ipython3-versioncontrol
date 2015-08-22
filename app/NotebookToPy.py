import json
import os
import fnmatch


class PyGenerator(object):
    def convert_all_notebook_to_py(self, directory, overwrite=False):
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.ipynb'):
                filename = os.path.abspath(os.path.join(root, filename))
                self.convert_notebook_to_py(filename, overwrite)

    def convert_notebook_to_py(self, input_file_path, overwrite=False):
        output_file_path = self.construct_output_path(input_file_path)
        if not os.path.exists(output_file_path) or overwrite:
            nb = Notebook()
            nb.read_notebook(input_file_path)
            self.write_notebook_to_py(nb, output_file_path)

    def write_notebook_to_py(self, notebook, out_file_path):
        assert isinstance(notebook, Notebook)
        with open(out_file_path, 'w') as output:
            self.add_header(output, str(notebook.notebook_format))
            for cell in notebook.cells:
                output.write(cell.generate_field_output())

    @staticmethod
    def add_header(output, notebook_format):
        assert isinstance(output, file)
        assert isinstance(notebook_format, str)
        output.write('# -*- coding: utf-8 -*-\n')
        output.write('# <nbformat>' + notebook_format + '</nbformat>\n')

    @staticmethod
    def construct_output_path(input_path):
        input_headless, ext = os.path.splitext(input_path)
        return input_headless + ".py"


class Notebook(object):
    notebook_format = int()
    cells = []

    def read_notebook(self, path_to_file):
        with open(path_to_file, 'r') as notebook:
            notebook_data = json.load(notebook)
        self.notebook_format = notebook_data["nbformat"]
        assert "cells" in notebook_data.keys(), "Nbformat is " + str(notebook_data['nbformat']) \
                                                + ", try the old converter script."
        for cell in notebook_data["cells"]:
            self.cells.append(Cell(cell))


class Cell(object):
    def __init__(self, cell):
        self.cell_type = cell['cell_type']
        self.source = cell["source"]

    def generate_field_output(self):
        output = '\n# <' + self.cell_type + 'cell' + '>\n\n'
        for item in self.source:
            if self.cell_type == "code":
                output += item
            else:
                output += "#" + item
        return output + "\n"


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                             '(This will overwrite default.)')
    args = parser.parse_args()
    pg = PyGenerator()

    if args.file is not None:
        pg.convert_notebook_to_py(args.file, overwrite=args.overwrite)
    else:
        pg.convert_all_notebook_to_py(directory='.', overwrite=args.overwrite)