import astroid
from eradicate import Eradicator
from pylint.checkers import BaseRawFileChecker
from pylint.interfaces import HIGH


class EradicateChecker(BaseRawFileChecker):
    name = "eradicate"

    msgs = {
        "C8920": (
            "Remove commented out code: %s",
            "dead-code",
            "Version control helps with keeping track of code changes. There is no need to keep commented out code in "
            "the codebase. Remove it to keep the codebase clean.",
        ),
    }

    def open(self) -> None:
        self._eradicator = Eradicator()

    def process_module(self, node: astroid.Module):
        with node.stream() as stream:
            source = stream.read().decode()
            lines = source.splitlines()
            for line_no in self._eradicator.commented_out_code_line_numbers(source):
                src_line = lines[line_no - 1].strip()
                self.add_message("dead-code", line=line_no, confidence=HIGH, args=(src_line,))


def register(linter):
    linter.register_checker(EradicateChecker(linter))
