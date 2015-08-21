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
            notebook_data = self.read_notebook(input_file_path)
            self.write_notebook_data_to_py(notebook_data, output_file_path)

    def write_notebook_data_to_py(self, notebook_data, out_file_path):
        assert isinstance(notebook_data, dict)
        with open(out_file_path, 'w') as output:
            if "cells" in notebook_data.keys():
                self.add_header(output, str(notebook_data['nbformat']))
                cells = notebook_data['cells']
                for cell in cells:
                    temp = Cell(cell)
                    output.write(temp.generate_field_output())
            else:
                print "Nbformat is " + str(notebook_data['nbformat']) + ", try the old converter script."
                return

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

    @staticmethod
    def read_notebook(path_to_file):
        with open(path_to_file, 'r') as notebook:
            notebook_data = json.load(notebook)
        return notebook_data


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

