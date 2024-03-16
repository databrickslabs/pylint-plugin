"""Experimental magic command for running Pylint on a cell.

This module provides a magic command for running Pylint on a cell. The
command is called `%%pylint` and is used as follows:

```python
%%pylint
def f(x):
    return x + 1
```

It doesn't fully work yet, but it's a start.

Development loop: `hatch build && databricks labs install .`
"""

import sys

from IPython import get_ipython
from IPython.core.magic import Magics, cell_magic, magics_class
from pylint.lint import PyLinter
from pylint.reporters.text import ColorizedTextReporter
from pylint.utils import ASTWalker


@magics_class
class PyLintMagic(Magics):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ipython = get_ipython()
        self._linter = PyLinter()
        self._ipython.user_ns["linter"] = self._linter
        self._linter.load_plugin_modules(["databricks.labs.pylint.all"])
        reporter = ColorizedTextReporter(sys.stderr)
        self._linter.set_reporter(reporter)
        self._walker = ASTWalker(self._linter)

    @cell_magic
    def pylint(self, _, cell):
        self._linter.set_current_module("notebook")
        node = self._linter.get_ast("notebook", "notebook", data=cell)
        if node is not None:
            walker = ASTWalker(self._linter)
            self._linter.check_astroid_module(node, walker, [], [])
            self._linter.generate_reports(verbose=True)
        self._ipython.run_cell(cell)


def load_ipython_extension(ipython):
    ipython.register_magics(PyLintMagic)


def enable():
    get_ipython().register_magics(PyLintMagic)
