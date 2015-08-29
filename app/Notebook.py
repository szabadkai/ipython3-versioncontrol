import json
import os
from ReadPy import ReadPy


class Notebook(object):
    notebook_format = None
    cells = []
    metadata = None
    nbformat_minor = None

    def read(self, path_to_file):
        input_headless, ext = os.path.splitext(path_to_file)
        if ext == ".ipynb":
            self.read_notebook(path_to_file)
        elif ext == ".py":
            self.read_py(path_to_file)

    def read_notebook(self, path_to_file):
        with open(path_to_file, 'r') as notebook:
            notebook_data = json.load(notebook)
        self.notebook_format = notebook_data["nbformat"]
        assert "cells" in notebook_data.keys(), "Nbformat is " + str(notebook_data['nbformat']) \
                                                + ", try the old converter script."
        for cell in notebook_data["cells"]:
            self.cells.append(Cell(cell))

    @staticmethod
    def read_py(path_to_file):
        reader = ReadPy()
        reader.read(path_to_file)

    def to_dict(self):
        cells = {'metadata': self.metadata,
                 'nbformat': self.notebook_format,
                 'nbformat_minor': self.nbformat_minor,
                 'cells': []}
        for cell in self.cells:
            cells['cells'].append(cell.to_dict())
        return cells


class Cell(object):
    def __init__(self, cell):
        self.type = cell['cell_type']
        self.source = cell["source"]

    def generate_field_output(self):
        output = '\n# <' + self.type + 'cell' + '>\n\n'
        for item in self.source:
            if self.type == "code":
                output += item
            else:
                output += "# " + item
        return output + "\n"

    def to_dict(self):
        return {'cell_type': self.type, 'source': self.source}
