from astroid import nodes  # type: ignore
from pylint.checkers import BaseChecker


class ReadabilityChecker(BaseChecker):
    name = "readability"
    msgs = {
        "R8923": (
            "List comprehension spans multiple lines, rewrite as for loop",
            "rewrite-as-for-loop",
            """List comprehensions in Python are typically used to create new lists by iterating over an existing
            iterable in a concise, one-line syntax. However, when a list comprehension becomes too complex or spans 
            multiple lines, it may lose its readability and clarity, which are key advantages of Python's syntax.""",
        ),
    }

    def visit_listcomp(self, node: nodes.ListComp) -> None:
        if node.lineno != node.end_lineno:
            self.add_message("rewrite-as-for-loop", node=node)


def register(linter):
    linter.register_checker(ReadabilityChecker(linter))
