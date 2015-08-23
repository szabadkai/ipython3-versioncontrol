import unittest
import os
from app.Notebook import Cell, Notebook
from app.Formater import ToNotebook,ToPy


class FormaterTests(unittest.TestCase):
    def test_topy_class_creation(self):
        topy = ToPy()
        self.assertIsInstance(topy, ToPy)

    def test_to_notebook_class_creation(self):
        tonb = ToNotebook()
        self.assertIsInstance(tonb, ToNotebook)

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
