import abc
import json
import os


class Formater():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def output(self, notebook, out_path):
        """Outputs the notebook data in the desired form"""
        return

    @staticmethod
    @abc.abstractmethod
    def construct_output_path(input_path):
        return


class ToNotebook(Formater):
    dry_run = None
    overwrite = None

    def __init__(self, overwrite=False, dry_run=False):
        self.overwrite = overwrite
        self.dry_run = dry_run

    def output(self, notebook, out_path):
        output = notebook.to_dict()
        self.write_py_data_to_notebook(output, out_path)

    @staticmethod
    def construct_output_path(input_path):
        input_headless, ext = os.path.splitext(input_path)
        return input_headless + ".ipynb"

    @staticmethod
    def write_py_data_to_notebook(output, out_file_path):
        with open(out_file_path, 'w') as outfile:
            json.dump(output, outfile)


class ToPy(Formater):
    def __init__(self, overwrite=False, dry_run=False,):
        self.overwrite = overwrite
        self.dry_run = dry_run

    def output(self, notebook, out_path):
        with open(out_path, 'w') as output:
            self.add_header(output, str(notebook.notebook_format))
            for cell in notebook.cells:
                output.write(cell.generate_field_output())

    @staticmethod
    def construct_output_path(input_path):
        input_headless, ext = os.path.splitext(input_path)
        return input_headless + ".py"

    @staticmethod
    def add_header(output, notebook_format):
        assert isinstance(output, file)
        assert isinstance(notebook_format, str)
        output.write('# -*- coding: utf-8 -*-\n')
        output.write('# <nbformat>' + notebook_format + '</nbformat>\n')
