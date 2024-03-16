import astroid
from pylint.checkers import BaseRawFileChecker
from pylint.interfaces import CONTROL_FLOW, HIGH


class NotebookChecker(BaseRawFileChecker):
    __implements__ = (BaseRawFileChecker,)

    name = "databricks-notebooks"
    msgs = {
        "C8913": (
            "Notebooks should not have more than 75 cells",
            "notebooks-too-many-cells",
            "Otherwise, it's hard to maintain and understand the notebook for other people and the future you",
        ),
        "R8914": (
            "Using %run is not allowed",
            "notebooks-percent-run",
            "Use functions instead of %run to avoid side effects and make the code more testable. "
            "If you need to share code between notebooks, consider creating a library. "
            "If still need to call another code as a separate job, use Databricks SDK for Python:"
            " https://databricks-sdk-py.readthedocs.io/en/latest/index.html",
        ),
    }

    options = (
        (
            "max-cells",
            {
                "default": 75,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum number of cells in the notebook",
            },
        ),
    )

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
        too_many_cells_raised = False
        with node.stream() as stream:
            for lineno, line in enumerate(stream):
                lineno += 1
                if lineno == 1 and line != b"# Databricks notebook source\n":
                    # this is not a Databricks notebook
                    return
                if line == b"# COMMAND ----------\n":
                    cells += 1
                if cells > self.linter.config.max_cells and not too_many_cells_raised:
                    self.add_message("notebooks-too-many-cells", line=lineno + 1, confidence=CONTROL_FLOW)
                    too_many_cells_raised = True
                    continue
                if line.startswith(b"# MAGIC %run"):
                    self.add_message("notebooks-percent-run", line=lineno, confidence=HIGH)


def register(linter):
    linter.register_checker(NotebookChecker(linter))
