import os
import fnmatch
from Notebook import Notebook


class NotebookConverter(object):
    def convert_all(self, directory, formater, dry_run=False, overwrite=False):
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.ipynb'):
                filename = os.path.abspath(os.path.join(root, filename))
                self.convert(filename, formater, dry_run, overwrite)

    @staticmethod
    def convert(input_file_path, formater, dry_run=False, overwrite=False):
        output_file_path = formater.construct_output_path(input_file_path)
        if not os.path.exists(output_file_path) or overwrite:
            nb = Notebook()
            nb.read(input_file_path)
            formater.output(nb, output_file_path, dry_run)
