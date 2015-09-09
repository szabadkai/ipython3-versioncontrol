from app.Notebook import Cell


class ReadPy(object):
    current_cell = None
    execution_count = 1
    _outputcells = []

    def read(self, path_to_file):
        skip_one_line = False
        with open(path_to_file, 'r') as lines:
            self.add_descriptive_data(lines.readlines())
            lines.seek(0)
            for line in lines:
                if skip_one_line:
                    skip_one_line = False
                elif self.is_first_line_of_cell(line):
                    self.close_cell()
                    if self.current_cell == 'code':
                        self.execution_count += 1
                    self.open_cell(line, self.execution_count)
                    skip_one_line = True
                elif self.current_cell.type in ('markdown', 'code'):
                    self.append_line_to_source(line)
            self.close_last_cell()
            return self._outputcells

    def close_cell(self):
        if self.current_cell.type in ('markdown', 'code'):
            if len(self.current_cell.source) > 1:
                del self.current_cell.source[-1:]
            self.current_cell.source[-1] = self.current_cell.source[-1].rstrip('\n')
            self._outputcells.append(self.current_cell)

    def close_last_cell(self):
        if self.current_cell.type in ['markdown', 'code']:
            self.current_cell.source[-1] = self.current_cell.source[-1].rstrip('\n')
            self._outputcells.append(self.current_cell)

    def open_cell(self, line, execution_count):
        if '<markdowncell>' in line:
            self.current_cell = Cell({'cell_type': 'markdown', 'metadata': {}, 'source':[]})
        else:
            self.current_cell = Cell({'cell_type': 'code',
                                      'execution_count': execution_count,
                                      'metadata': {'collapsed': False},
                                      'outputs': []})

    def append_line_to_source(self, row):
        if self.current_cell.type == 'markdown':
            self.current_cell.source.append(row.lstrip("# "))
        elif self.current_cell.type == 'code':
            self.current_cell.source.append(row)

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