"""
   The script takes an .ipynb file (or all such files in the directory), and,
   if it doesn't already have a corresponding .py file, creates it from the
   .ipynb file. We do this because we don't want to version-control .ipynb files
   (which can contain images, matrices, data frames, etc), but we do want to
   save the content of the notebook cells.

   This is intented to be a replacement of the deprecated

   ipython notebook --script

   command for Ipython 2 notebooks that automatically saved notebooks as .py
   files that can be version controled.

   Optionally, the first three functions can be used for post-hook autosave in
   the ipython_notebook_config.py file.

   Call this script with argument "-f" to create a .py file from  notebook:

   python notebook_v4_to_py.py -f filename.ipynb

   Call the script with argument "--overwrite" to overwrite existing .py files.

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
from app.Formater import ToPy
from app.NotebookConverter import NotebookConverter


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                             '(This will overwrite default.)')
    args = parser.parse_args()
    nb2py = NotebookConverter()
    fm = ToPy()
    if args.file is not None:
        nb2py.convert(args.file, fm, overwrite=args.overwrite)
    else:
        nb2py.convert_all('.', fm, False, overwrite=args.overwrite)
