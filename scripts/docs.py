import re
from pathlib import Path

from pylint.lint import PyLinter

from databricks.labs.pylint.airflow import AirflowChecker
from databricks.labs.pylint.dbutils import DbutilsChecker
from databricks.labs.pylint.legacy import LegacyChecker
from databricks.labs.pylint.notebooks import NotebookChecker
from databricks.labs.pylint.spark import SparkChecker


def do_something():
    out = ["<!-- CHECKS -->\n"]
    linter = PyLinter()
    for checker in [
        AirflowChecker(linter),
        DbutilsChecker(linter),
        LegacyChecker(linter),
        NotebookChecker(linter),
        SparkChecker(linter),
    ]:
        out.append(f"## `{checker.name}` checker")
        out.append("\n[[back to top](#databricks-labs-pylint-plugin)]\n")
        for msg_def in checker.messages:
            out.append(f"### `{msg_def.msgid}`: `{msg_def.symbol}`\n")
            out.append(f"{msg_def.msg.replace('%s', 'XXX')}. {msg_def.description}")
            out.append("\n[[back to top](#databricks-labs-pylint-plugin)]\n")
    out.append("<!-- END CHECKS -->")
    checker_docs = "\n".join(out)
    readme_file = Path(__file__).parent.parent.joinpath("README.md")
    with readme_file.open("r") as f:
        pattern = r"<!-- CHECKS -->\n(.*)\n<!-- END CHECKS -->"
        new_readme = re.sub(pattern, checker_docs, f.read(), 0, re.MULTILINE | re.DOTALL)
    with readme_file.open("w") as f:
        f.write(new_readme)


if __name__ == "__main__":
    do_something()
