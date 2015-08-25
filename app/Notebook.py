import json
import os


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

    def read_py(self, path_to_file):
        current_cell = None
        execution_count = 1
        skip_one_line = False
        outputcells = []
        source = []

        def close_cell():
            if current_cell in ['markdown', 'code']:
                if len(source) > 1:
                    del source[-1:]
                source[-1] = source[-1].rstrip('\n')
                cell['source'] = source
                outputcells.append(cell)

        def close_last_cell():
            if current_cell in ['markdown', 'code']:
                source[-1] = source[-1].rstrip('\n')
                cell['source'] = source
                outputcells.append(cell)

        def open_cell(_line, _execution_count):
            if '<markdowncell>' in _line:
                _cell = {'cell_type': 'markdown', 'metadata': {}}
                _source = []
                _current_cell = 'markdown'
            else:
                _cell = {'cell_type': 'code',
                         'execution_count': _execution_count,
                         'metadata': {'collapsed': False},
                         'outputs': []}
                _source = []
                _current_cell = 'code'
            return _cell, _source, _current_cell

        def append_line_to_source(row):
            if current_cell == 'markdown':
                source.append(row.lstrip("# "))
            elif current_cell == 'code':
                source.append(row)

        with open(path_to_file, 'r') as lines:
            self.add_descriptive_data(lines.readlines())
            lines.seek(0)
            for line in lines:
                if skip_one_line:
                    skip_one_line = False
                elif self.is_first_line_of_cell(line):
                    close_cell()
                    if current_cell == 'code':
                        execution_count += 1
                    cell, source, current_cell = open_cell(line, execution_count)
                    skip_one_line = True
                elif current_cell in ('markdown', 'code'):
                    append_line_to_source(line)

            close_last_cell()

            for cell in outputcells:
                self.cells.append(Cell(cell))

    @staticmethod
    def is_first_line_of_cell(line):
        if line == '# <markdowncell>\n' or line == '# <codecell>\n':
            return True
        return False

    def add_descriptive_data(self, lines):
        self.metadata = self.create_metadata()
        self.notebook_format = self.read_nb_format_from_py(lines)
        self.nbformat_minor = 0

    @staticmethod
    def create_metadata():
        kernelspec = {'display_name': 'Python 2',
                      'language': 'python',
                      'name': 'python2'}
        language_info = {'codemirror_mode': {'name': 'ipython', 'version': 2},
                         'file_extension': '.py',
                         'mimetype': 'text/x-python',
                         'name': 'python',
                         'nbconvert_exporter': 'python',
                         'pygments_lexer': 'ipython2',
                         'version': '2.7.10'}
        metadata = {'kernelspec': kernelspec,
                    'language_info': language_info}
        return metadata

    @staticmethod
    def read_nb_format_from_py(lines):
        if '<nbformat>' in lines[1]:
            nbformat = lines[1].split('>')[1].split('<')[0]
            if "." in nbformat:
                nbformat = float(nbformat)
            else:
                nbformat = int(nbformat)
            return nbformat
        else:
            raise IOError("No or not suitable ( line[1]: "+lines[1]+") nbformat in supported lines")

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
        self.cell_type = cell['cell_type']
        self.source = cell["source"]

    def generate_field_output(self):
        output = '\n# <' + self.cell_type + 'cell' + '>\n\n'
        for item in self.source:
            if self.cell_type == "code":
                output += item
            else:
                output += "# " + item
        return output + "\n"

    def to_dict(self):
        return {'cell_type': self.cell_type, 'source': self.source}
