from databricks.labs.pylint.airflow import AirflowChecker
from databricks.labs.pylint.dbutils import DbutilsChecker
from databricks.labs.pylint.legacy import LegacyChecker
from databricks.labs.pylint.mocking import MockingChecker
from databricks.labs.pylint.notebooks import NotebookChecker
from databricks.labs.pylint.spark import SparkChecker


def register(linter):
    linter.register_checker(NotebookChecker(linter))
    linter.register_checker(DbutilsChecker(linter))
    linter.register_checker(LegacyChecker(linter))
    linter.register_checker(AirflowChecker(linter))
    linter.register_checker(SparkChecker(linter))
    linter.register_checker(MockingChecker(linter))
