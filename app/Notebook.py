import json


class Notebook(object):
    notebook_format = int()
    cells = []
    metadata = dict()
    nbformat_minor = int()

    def read_notebook(self, path_to_file):
        with open(path_to_file, 'r') as notebook:
            notebook_data = json.load(notebook)
        self.notebook_format = notebook_data["nbformat"]
        assert "cells" in notebook_data.keys(), "Nbformat is " + str(notebook_data['nbformat']) \
                                                + ", try the old converter script."
        for cell in notebook_data["cells"]:
            self.cells.append(Cell(cell))

    def create_initial_output(self, lines):
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
        nbformat_minor = 0

        if '<nbformat>' in lines[1]:
            nbformat = lines[1].split('>')[1].split('<')[0]
            try:
                nbformat = int(nbformat)
            except ValueError:
                nbformat = float(nbformat)
        else:
            raise IOError

        self.metadata = metadata
        self.notebook_format = nbformat
        self.nbformat_minor = nbformat_minor

    def read_py(self, path_to_file):
        def close_cell(current_cell):
            if current_cell in ['markdown', 'code']:
                if not last_cell and len(source) > 1:
                    del source[-1:]
                source[-1] = source[-1].rstrip('\n')
                cell['source'] = source
                outputcells.append(cell)
            return outputcells

        def open_cell(line, execution_count):
            if '<markdowncell>' in line:
                cell = {'cell_type': 'markdown',
                        'metadata': {}}
                source = []
                current_cell = 'markdown'
            elif '<codecell>' in line:
                cell = {'cell_type': 'code',
                       'execution_count': execution_count,
                        'metadata': {'collapsed': False},
                        'outputs': []}
                source = []
                current_cell = 'code'
            return cell, source, current_cell
        current_cell = 'unknown'
        execution_count = 1
        skip_one_line = False
        last_cell = False
        outputcells = []
        with open(path_to_file, 'r') as lines:
            self.create_initial_output(lines.readlines())
            lines.seek(0)
            for line in lines:
                if skip_one_line:
                    skip_one_line = False
                    continue

                if line=='# <markdowncell>\n' or line=='# <codecell>\n':
                    outputcells = close_cell(current_cell)
                    if current_cell=='code':
                        execution_count += 1
                    cell, source, current_cell = open_cell(line, execution_count)
                    skip_one_line = True
                    continue

                if current_cell=='markdown':
                    if len(line) > 1:
                        source.append(line[2:])
                    else:
                        source.append(line)
                elif current_cell=='code':
                    source.append(line)

            last_cell = True
            outputcells = close_cell(current_cell)
            for cell in outputcells:
                self.cells.append(Cell(cell))

    def to_dict(self):
        cells = {   'metadata': self.metadata,
                    'nbformat': self.nbformat,
                    'nbformat_minor': self.nbformat_minor,
                    'cells':[]}
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
                output += "#" + item
        return output + "\n"

    def to_dict(self):
        return {'cell_type':self.cell_type, 'source': self.source}