import astroid
from pylint.checkers import BaseChecker, BaseRawFileChecker


class NotebookChecker(BaseRawFileChecker):
    __implements__ = (BaseRawFileChecker,)

    name = 'databricks-notebooks'
    msgs = {
        'E9999': (
            'dbutils.notebook.run() is not allowed',
            'notebooks-dbutils-run',
            'Used when dbutils.notebook.run() is used'
        ),
        'E9998': (
            'dbutils.fs is not allowed',
            'notebooks-dbutils-fs',
            'Used when dbutils.fs is used'
        ),
        'E9997': (
            'dbutils.credentials is not allowed',
            'notebooks-dbutils-credentials',
            'Used when dbutils.credentials is used'
        ),
        'E9996': (
            'Notebooks should not have more than 75 cells',
            'notebooks-too-many-cells',
            'Used when the number of cells in a notebook is greater than 75'
        ),
        'E9995': (
            'Star import is not allowed',
            'notebooks-star-import',
            'Used when there is a star import from pyspark.sql.functions'
        ),
        'E9994': (
            'Using %run is not allowed',
            'notebooks-percent-run',
            'Used when `# MAGIC %run` comment is used',
        ),
    }

    def process_module(self, node: astroid.Module):
        """Read raw module. Need to do some tricks, as `ast` doesn't provide access for comments.

        Alternative libraries that can parse comments along with the code:
        - https://github.com/Instagram/LibCST/ (MIT + PSF)
        - https://github.com/python/cpython/tree/3.10/Lib/lib2to3 (PSF), removed in Python 3.12
        - https://github.com/t3rn0/ast-comments (MIT)
        - https://github.com/facebookincubator/bowler (MIT), abandoned
        - https://github.com/PyCQA/redbaron (LGPLv3)
        """
        cells = 1
        with node.stream() as stream:
            for (lineno, line) in enumerate(stream):
                lineno += 1
                if lineno == 1 and line != b'# Databricks notebook source\n':
                    # this is not a Databricks notebook
                    return
                if line == b'# COMMAND ----------\n':
                    cells += 1
                if cells > 75:
                    self.add_message('notebooks-too-many-cells', line=lineno)
                    continue
                if line.startswith(b'# MAGIC %run'):
                    self.add_message('notebooks-percent-run', line=lineno)

    def visit_module(self, node):
        # add message if dbutils.notebook.run() is used
        if node.name == 'dbutils.notebook.run':
            self.add_message('notebooks-dbutils-run', node=node)

        # add message if dbutils.fs is used
        if node.name == 'dbutils.fs':
            self.add_message('notebooks-dbutils-fs', node=node)

        # add message if dbutils.credentials is used
        if node.name == 'dbutils.credentials':
            self.add_message('notebooks-dbutils-credentials', node=node)

        # Notebooks should not have more than 75 cells.
        if len(node.body) > 75:
            self.add_message('notebooks-too-many-cells', node=node)

    def visit_importfrom(self, node: astroid.ImportFrom):
        # add message if there's a star import from pyspark.sql.functions import *
        if node.modname == 'pyspark.sql.functions' and node.names[0][0] == '*':
            self.add_message('notebooks-star-import', node=node)


def register(linter):
    linter.register_checker(NotebookChecker(linter))