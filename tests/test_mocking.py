from databricks.labs.pylint.mocking import MockingChecker


def test_obscure_mock(lint_with):
    messages = lint_with(MockingChecker) << "MagicMock()"
    _ = "[obscure-mock] Obscure implicit test dependency with MagicMock(). Rewrite with create_autospec(ConcreteType)."
    assert _ in messages


def test_explicit_dependency_required(lint_with):
    messages = lint_with(MockingChecker) << "mocker.patch('databricks.sdk.foo')"

    _ = (
        "[explicit-dependency-required] Obscure implicit test dependency with mock.patch('databricks.sdk.foo'). "
        "Rewrite to inject dependencies through constructor."
    )
    assert _ in messages
