def register(linter):
    from databricks.labs.pylint.dbutils import DbutilsChecker
    from databricks.labs.pylint.notebooks import NotebookChecker

    linter.register_checker(NotebookChecker(linter))
    linter.register_checker(DbutilsChecker(linter))
