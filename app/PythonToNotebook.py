import os
import fnmatch
from Notebook import Notebook
from Formater import ToNotebook


class NbGenerator(object):
    def convert_all_py_to_notebook(self, directory, overwrite=False, dry_run=False):
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.py'):
                filename = os.path.abspath(os.path.join(root, filename))
                self.convert_py_to_notebook(filename, overwrite,dry_run)

    def convert_py_to_notebook(self, input_file_path, overwrite=False, dry_run=False):
        output_file_path = self.construct_output_path_for_py(input_file_path)
        if not os.path.exists(output_file_path) or overwrite:
            nb = Notebook()
            nb.read_py(input_file_path)
            fm = ToNotebook()
            fm.output(nb, output_file_path, dry_run)

    @staticmethod
    def construct_output_path_for_py(input_path):
        input_headless, ext = os.path.splitext(input_path)
        return input_headless + ".ipynb"


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                       '(This will overwrite default.)')
    parser.add_argument('--dry-run', action='store_true', help='Only prints what would happen', default=False)
    args = parser.parse_args()
    ng = NbGenerator()

    if args.file is not None:
        ng.convert_py_to_notebook(args.file, overwrite=args.overwrite, dry_run=args.dry_run)
    else:
        ng.convert_all_py_to_notebook(directory='.', overwrite=args.overwrite, dry_run=args.dry_run)
