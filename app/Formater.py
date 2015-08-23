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
        output =
        output['cells'] = notebook.cells_to_dict()
        if not dry_run:
            self.write_py_data_to_notebook(output, out_path)
        print "Created Ipython Jupyter notebook file: {}".format(out_path)

    @staticmethod
    def write_py_data_to_notebook(output, out_file_path):
        with open(out_file_path, 'w') as outfile:
            json.dump(output, outfile)

    @staticmethod
    def create_initial_output(notebook):
        assert isinstance(notebook, Notebook)
        return {'metadata': notebook.metadata,
                  'nbformat': notebook.nbformat,
                  'nbformat_minor': notebook.nbformat_minor}


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