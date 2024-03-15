import astroid
from pylint.checkers import BaseChecker


class SparkChecker(BaseChecker):
    name = "spark"

    msgs = {
        "E9700": (
            "Using spark outside the function is leading to untestable code",
            "spark-outside-function",
            "Do not use global spark object, pass it as an argument to the function instead, "
            "so that the function becomes testable in a CI/CD pipelines.",
        ),
        "E9701": (
            "Function %s is missing a 'spark' argument",
            "no-spark-argument-in-function",
            "Function refers to a global spark variable, which may not always be available. "
            "Pass the spark object as an argument to the function instead, so that the function "
            "becomes testable in a CI/CD pipelines.",
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
