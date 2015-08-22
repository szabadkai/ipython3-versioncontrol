import json


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

    def read_cells_from_py(self, file_handle):
        for line in file_handle:
            if line == '# <markdowncell>\n' or line == '# <codecell>\n':
                cell_type = "markdown" if line == '# <markdowncell>\n' else 'code'
                cell = Cell({"cell_type": cell_type, "source": []})
                while not (line == '# <markdowncell>\n' or line == '# <codecell>\n'):
                    line = file_handle.readline()
                    if cell.cell_type == "markdown":
                        source_line = line[2:] if len(line) > 2 else line
                        cell.source.append(source_line)
                    elif cell.cell_type == "code":
                        cell.source.append(line)
                else:
                    self.cells.append(cell)
                    file_handle.seek(file_handle.tell() - 1)
            else:
                print(line)

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
