import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import CONTROL_FLOW, INFERENCE


class SparkChecker(BaseChecker):
    name = "spark"

    msgs = {
        "C8915": (
            "Using spark outside the function is leading to untestable code",
            "spark-outside-function",
            "Do not use global spark object, pass it as an argument to the function instead, "
            "so that the function becomes testable in a CI/CD pipelines.",
        ),
        "W8916": (
            "Function %s is missing a 'spark' argument",
            "no-spark-argument-in-function",
            "Function refers to a global spark variable, which may not always be available. "
            "Pass the spark object as an argument to the function instead, so that the function "
            "becomes testable in a CI/CD pipelines.",
        ),
        "C8917": (
            "Rewrite to display in a notebook: display(%s)",
            "use-display-instead-of-show",
            "Use display() instead of show() to visualize the data in a notebook.",
        ),
    }

    def visit_name(self, node: astroid.Name):
        if node.name != "spark":
            return
        in_node = node
        while in_node and not isinstance(in_node, astroid.FunctionDef):
            in_node = in_node.parent
        if not in_node:
            self.add_message("spark-outside-function", node=node, confidence=CONTROL_FLOW)
            return
        has_spark_arg = False
        for arg in in_node.args.arguments:
            if arg.name == "spark":
                has_spark_arg = True
                break
        if not has_spark_arg:
            self.add_message(
                "no-spark-argument-in-function", node=in_node, args=(in_node.name,), confidence=CONTROL_FLOW
            )

    def visit_attribute(self, node: astroid.Attribute):
        if node.attrname == "show" and isinstance(node.expr, astroid.Call):
            self.add_message(
                "use-display-instead-of-show", node=node, args=(node.expr.as_string(),), confidence=INFERENCE
            )


def register(linter):
    linter.register_checker(SparkChecker(linter))
