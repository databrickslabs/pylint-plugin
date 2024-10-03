import re
from pathlib import Path

from pylint.lint import PyLinter

from databricks.labs.pylint.airflow import AirflowChecker
from databricks.labs.pylint.dbutils import DbutilsChecker
from databricks.labs.pylint.eradicate import EradicateChecker
from databricks.labs.pylint.legacy import LegacyChecker
from databricks.labs.pylint.mocking import MockingChecker
from databricks.labs.pylint.notebooks import NotebookChecker
from databricks.labs.pylint.readability import ReadabilityChecker
from databricks.labs.pylint.spark import SparkChecker


def do_something():
    heading_anchor = "\n[[back to top](#pylint-plugin-for-databricks)]\n"
    out = ["<!-- CHECKS -->\n"]
    symbols = []
    linter = PyLinter()
    for checker in [
        AirflowChecker(linter),
        DbutilsChecker(linter),
        LegacyChecker(linter),
        NotebookChecker(linter),
        SparkChecker(linter),
        ReadabilityChecker(linter),
        MockingChecker(linter),
        EradicateChecker(linter),
    ]:
        out.append(f"## `{checker.name}` checker")
        out.append(
            f"To use this checker, add `{checker.__module__}` to `load-plugins` "
            f"configuration in your `pylintrc` or `pyproject.toml` file."
        )
        out.append(heading_anchor)
        for msg_def in checker.messages:
            out.append(f"### `{msg_def.msgid}`: `{msg_def.symbol}`\n")
            out.append(f"{msg_def.msg.replace('%s', 'XXX')}. {msg_def.description}")
            out.append("")
            disable_comment = f"# pylint: disable={msg_def.symbol}"
            out.append(f"To disable this check on a specific line, add `{disable_comment}` at the end of it.")
            out.append(heading_anchor)
            symbols.append(msg_def.symbol)
    out.append("## Testing in isolation")
    out.append("To test this plugin in isolation, you can use the following command:\n")
    out.append("```bash")
    out.append(f"pylint --load-plugins=databricks.labs.pylint.all --disable=all --enable={','.join(symbols)} .")
    out.append("```")
    out.append(heading_anchor)
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
