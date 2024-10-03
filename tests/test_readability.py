from databricks.labs.pylint.readability import ReadabilityChecker


def test_single_line_list_comprehensions_allowed(lint_with):
    messages = lint_with(ReadabilityChecker) << """[x for x in range(10) if x % 2 == 0]"""
    assert not messages


def test_multi_line_list_comprehensions_not_allowed(lint_with):
    messages = (
        lint_with(ReadabilityChecker)
        << """[
        x for x in range(10) if x % 2 == 0
    ]"""
    )
    assert messages == {"[rewrite-as-for-loop] List comprehension spans multiple lines, rewrite as for loop"}
