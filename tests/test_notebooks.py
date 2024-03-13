import astroid
import pylint.testutils

from pylint.lint.pylinter import PyLinter

from databricks.labs.pylint.notebooks import NotebookChecker


def test_percent_run():
    linter = PyLinter()
    checker = NotebookChecker(linter)
    linter.disable("all")
    linter.register_checker(checker)
    linter.check(["samples/TestForPylint.py"])

    assert 1 == len(linter.reporter.messages)


class TestNotebookChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NotebookChecker

    def test_import_from_pyspark(self):
        node = astroid.extract_node("""
        from pyspark.sql.functions import *
        """)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="notebooks-star-import",
                node=node,
            ), ignore_position=True
        ):
            self.checker.visit_importfrom(node)

    def test_percent_run(self):
        node = astroid.extract_node("""# Databricks notebook source
# MAGIC %md # Here's markdown cell

# COMMAND ----------

# MAGIC %run ./something

# COMMAND ----------

print('hello')
        """)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="notebooks-percent-run",
                node=node,
            ), ignore_position=True
        ):
            self.checker.process_module(node)
