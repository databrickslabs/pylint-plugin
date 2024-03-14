from typing import Generic, TypeVar

import astroid
import astroid.rebuilder
import pytest
from pylint.checkers import BaseChecker
from pylint.testutils import UnittestLinter

T = TypeVar("T", bound=BaseChecker)


class TestSupport(Generic[T]):
    def __init__(self, klass: type[T]):
        linter = UnittestLinter()
        checker = klass(linter)
        checker.open()
        linter.register_checker(checker)

        self._checker = checker
        self._linter = linter

    def __lshift__(self, code: str):
        node = astroid.extract_node(code)

        klass_name = node.__class__.__name__
        visitor = astroid.rebuilder.REDIRECT.get(klass_name, klass_name).lower()
        getattr(self._checker, f"visit_{visitor}")(node)

        out = set()
        for message in self._linter.release_messages():
            for message_definition in self._linter.msgs_store.get_message_definitions(message.msg_id):
                user_message = message_definition.msg
                if message.args:
                    user_message %= message.args
                out.add(f"[{message.msg_id}] {user_message}")

        return out


@pytest.fixture
def lint_with():
    def factory(klass: type[T]) -> TestSupport[T]:
        return TestSupport(klass)

    yield factory
