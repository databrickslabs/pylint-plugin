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


def test_mock_in_function_arg(lint_with):
    messages = (
        lint_with(MockingChecker)
        << """some_fn(
    some_arg,
    create_autospec(ConcreteType), #@
    True,
)"""
    )

    assert "[mock-no-assign] Mock not assigned to a variable: create_autospec(ConcreteType)" in messages


def test_mock_not_assigned(lint_with):
    messages = (
        lint_with(MockingChecker)
        << """_ = 1
create_autospec(ConcreteType) #@
some_fn(some_arg, True)
"""
    )

    assert "[mock-no-assign] Mock not assigned to a variable: create_autospec(ConcreteType)" in messages


def test_mock_return_value_real(lint_with):
    messages = (
        lint_with(MockingChecker)
        << """with _lock:
    installation = mock_installation()
    if 'workspace_client' not in replace:
        ws = (
            create_autospec(WorkspaceClient) #@
        )
        ws.api_client.do.return_value = {}
        ws.permissions.get.return_value = {}
        replace['workspace_client'] = ws
    if 'sql_backend' not in replace:
        replace['sql_backend'] = MockBackend()
"""
    )

    assert not messages


def test_mock_is_asserted(lint_with):
    messages = (
        lint_with(MockingChecker)
        << """_ = 1
mocked_thing = ( # wrapping in parentheses to fetch call node
    create_autospec(ConcreteType) #@
)
mocked_thing.foo.bar.return_value = 42
some_fn(some_arg, mocked_thing, True)
mocked_thing.foo.bar.assert_called_once()
"""
    )

    assert not messages
