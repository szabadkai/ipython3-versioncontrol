import abc
import json
from Notebook import Notebook,Cell


class Formater():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def output(self, notebook, out_path):
        """Outputs the notebook data in the desired form"""
        return


class ToNotebook(Formater):
    def output(self, notebook, out_path, dry_run=False):
        output = self.create_initial_output(notebook)
        output['cells'] = self.build_notebook_cells(notebook)
        if not dry_run:
            self.write_py_data_to_notebook(output, out_path)
        print "Created Ipython Jupyter notebook file: {}".format(out_path)

    @staticmethod
    def build_notebook_cells(notebook):
        cells = []
        for cell in notebook.cells:
            cells.append({"cell_type":cell.cell_type, "source":cell.source})
        return cells

    @staticmethod
    def write_py_data_to_notebook(output, out_file_path):
        with open(out_file_path, 'w') as outfile:
            json.dump(output, outfile)

    @staticmethod
    def create_initial_output(notebook):
        assert isinstance(notebook, Notebook)
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
        nbformat = notebook.notebook_format
        return {'metadata': metadata,
                  'nbformat': nbformat,
                  'nbformat_minor': nbformat_minor}


class ToPy(Formater):
    def output(self, notebook, out_path):
        with open(out_path, 'w') as output:
            self.add_header(output, str(notebook.notebook_format))
            for cell in notebook.cells:
                output.write(cell.generate_field_output())

    @staticmethod
    def add_header(output, notebook_format):
        assert isinstance(output, file)
        assert isinstance(notebook_format, str)
        output.write('# -*- coding: utf-8 -*-\n')
        output.write('# <nbformat>' + notebook_format + '</nbformat>\n')