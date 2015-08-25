"""
   This script converts a .py file to Ipython v4 notebook format. The .py file
   must be a result of an Ipython -> .py conversion using the notebook_v4_to_py.py
   script or the automatic post-hook save in Ipyhon 3 based on that script.
   In this way the version controlled .py files can be converted back to Ipython
   notebook format.

   Call this script with argument "-f" to create an .ipynb file from a .py file:

   python py_to_notebook_v4.py -f filename.py

   Call the script with argument "--overwrite" to overwrite existing .ipynb files.

   Call the script with argument "--dry-run" to simulate (print) what would happen.

   Date: 07. August 2015.
   #############################################################################

   This script is released under the MIT License

   Copyright (c) 2015 Balabit SA

   Permission is hereby granted, free of charge, to any person obtaining a copy of
   this software and associated documentation files (the "Software"), to deal in
   the Software without restriction, including without limitation the rights to use,
   copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
   Software, and to permit persons to whom the Software is furnished to do so,
   subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
   PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
   HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
   WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from app.NotebookConverter import NotebookConverter
from app.Formater import ToNotebook

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                             '(This will overwrite default.)')
    parser.add_argument('--dry-run', action='store_true', help='Only prints what would happen', default=False)
    args = parser.parse_args()
    py2nb = NotebookConverter()
    fm = ToNotebook()

    if args.file is not None:
        py2nb.convert(args.file, ToNotebook(overwrite=args.overwrite, dry_run=args.dry_run))
    else:
        py2nb.convert_all('.', ToNotebook(overwrite=args.overwrite, dry_run=args.dry_run))
