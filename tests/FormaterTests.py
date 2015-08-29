import unittest
import os
from app.Formatter import ToNotebook, ToPy


class FormaterTests(unittest.TestCase):
    def test_topy_class_creation(self):
        topy = ToPy()
        self.assertIsInstance(topy, ToPy)

    def test_to_notebook_class_creation(self):
        tonb = ToNotebook()
        self.assertIsInstance(tonb, ToNotebook)

    def test_topy_empty_constructor_creation(self):
        topy = ToPy()
        self.assertEquals((topy.dry_run, topy.overwrite), (False, False))

    def test_to_notebook_empty_constructor_creation(self):
        tonb = ToNotebook()
        self.assertEquals((tonb.dry_run, tonb.overwrite), (False, False))

    def test_nb_constructor(self):
        tonb = ToNotebook(True, True)
        self.assertEquals((tonb.dry_run, tonb.overwrite), (True, True))

    def test_py_constructor(self):
        topy = ToPy(True, True)
        self.assertEquals((topy.dry_run, topy.overwrite), (True, True))

    def test_topy_construct_path_method(self):
        topy = ToPy()
        path = topy.construct_output_path('a.exe')
        self.assertEquals(path, 'a.py')

    def test_tonb_construct_path_method(self):
        topy = ToNotebook()
        path = topy.construct_output_path('a.exe')
        self.assertEquals(path, 'a.ipynb')

    def test_add_header_method(self):
        with open('header', 'w') as header:
            topy = ToPy()
            topy.add_header(header, '4')
        with open('header', 'r') as header:
            tmp = header.readlines()
            os.remove('header')
            self.assertEquals((tmp[0], tmp[1]), ('# -*- coding: utf-8 -*-\n', '# <nbformat>4</nbformat>\n'))


if __name__ == '__main__':
    unittest.main()
