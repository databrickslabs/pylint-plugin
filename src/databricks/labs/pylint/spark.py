import astroid
from pylint.checkers import BaseChecker


class SparkChecker(BaseChecker):
    name = "spark"

    msgs = {
        "E9700": (
            "Using spark outside the function is leading to untestable code",
            "spark-outside-function",
            "spark used outside of function",
        ),
        "E9701": (
            "Function %s is missing a 'spark' argument",
            "no-spark-argument-in-function",
            "function missing spark argument",
        ),
    }

    def visit_name(self, node: astroid.Name):
        if node.name != "spark":
            return
        in_node = node
        while in_node and not isinstance(in_node, astroid.FunctionDef):
            in_node = in_node.parent
        if not in_node:
            self.add_message("spark-outside-function", node=node)
            return
        has_spark_arg = False
        for arg in in_node.args.arguments:
            if arg.name == "spark":
                has_spark_arg = True
                break
        if not has_spark_arg:
            self.add_message("no-spark-argument-in-function", node=in_node, args=(in_node.name,))


def register(linter):
    linter.register_checker(SparkChecker(linter))
