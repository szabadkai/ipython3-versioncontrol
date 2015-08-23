import os
import fnmatch
from Notebook import Notebook
from Formater import ToPy


class NotebookToPy(object):
    def convert_all_notebook_to_py(self, directory, overwrite=False):
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.ipynb'):
                filename = os.path.abspath(os.path.join(root, filename))
                self.convert_notebook_to_py(filename, overwrite)

    def convert_notebook_to_py(self, input_file_path, overwrite=False):
        output_file_path = self.construct_output_path_for_py(input_file_path)
        if not os.path.exists(output_file_path) or overwrite:
            nb = Notebook()
            nb.read_notebook(input_file_path)
            fm = ToPy()
            fm.output(nb, output_file_path)

    @staticmethod
    def construct_output_path_for_py(input_path):
        input_headless, ext = os.path.splitext(input_path)
        return input_headless + ".py"


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                             '(This will overwrite default.)')
    args = parser.parse_args()
    pg = NotebookToPy()

    if args.file is not None:
        pg.convert_notebook_to_py(args.file, overwrite=args.overwrite)
    else:
        pg.convert_all_notebook_to_py(directory='.', overwrite=args.overwrite)
