from pylint.testutils import UnittestLinter

from databricks.labs.pylint.notebooks import NotebookChecker


def test_percent_run():
    linter = UnittestLinter()
    checker = NotebookChecker(linter)
    linter.register_checker(checker)
    linter.check(["samples/TestForPylint.py"])

    msgs = {_.msg_id for _ in linter.release_messages()}

    assert "notebooks-percent-run" in msgs
