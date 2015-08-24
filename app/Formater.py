import abc
import json
import os

class Formater():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def output(self, notebook, out_path, dry_run):
        """Outputs the notebook data in the desired form"""
        return

    @staticmethod
    @abc.abstractmethod
    def construct_output_path(input_path):
        return



class ToNotebook(Formater):
    def output(self, notebook, out_path, dry_run=False):
        output = notebook.to_dict()
        if not dry_run:
            self.write_py_data_to_notebook(output, out_path)
        print "Created Ipython Jupyter notebook file: {}".format(out_path)

    @staticmethod
    def construct_output_path(input_path):
        input_headless, ext = os.path.splitext(input_path)
        return input_headless + ".ipynb"

    @staticmethod
    def write_py_data_to_notebook(output, out_file_path):
        with open(out_file_path, 'w') as outfile:
            json.dump(output, outfile)


class ToPy(Formater):
    def output(self, notebook, out_path, dry_run):
        with open(out_path, 'w') as output:
            if not dry_run:
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
