from astroid import nodes  # type: ignore
from pylint.checkers import BaseChecker

DOC_EXPLICIT_DEPENDENCY_REQUIRED = """Using `patch` to mock dependencies in unit tests can introduce implicit 
dependencies within a class, making it unclear to other developers. Constructor arguments, on the other hand, 
explicitly declare dependencies, enhancing code readability and maintainability. However, reliance on `patch` 
for testing may lead to issues during refactoring, as updates to underlying implementations would necessitate 
changes across multiple unrelated unit tests. Moreover, the use of hard-coded strings in `patch` can obscure 
which unit tests require modification, as they lack strongly typed references. This coupling of the class 
under test to concrete classes signifies a code smell, and such code is not easily portable to statically typed 
languages where monkey patching isn't feasible without significant effort. In essence, extensive patching of 
external clients suggests a need for refactoring, with experienced engineers recognizing the potential for 
dependency inversion in such scenarios.

To address this issue, refactor the code to inject dependencies through the constructor. This approach
explicitly declares dependencies, enhancing code readability and maintainability. Moreover, it allows for
dependency inversion, enabling the use of interfaces to decouple the class under test from concrete classes.
This decoupling facilitates unit testing, as it allows for the substitution of mock objects for concrete
implementations, ensuring that the class under test behaves as expected. By following this approach, you can
create more robust and maintainable unit tests, improving the overall quality of your codebase.

Use `require-explicit-dependency` option to specify the package names that contain code for your project."""

DOC_OBSCURE_MOCK = """Using `MagicMock` to mock dependencies in unit tests can introduce implicit dependencies 
within a class, making it unclear to other developers. create_autospec(ConcreteType) is a better alternative, as it
automatically creates a mock object with the same attributes and methods as the concrete class. This
approach ensures that the mock object behaves like the concrete class, allowing for more robust and
maintainable unit tests. Moreover, reliance on `MagicMock` for testing leads to issues during refactoring,
as updates to underlying implementations would necessitate changes across multiple unrelated unit tests."""


class MockingChecker(BaseChecker):
    name = "mocking"
    msgs = {
        "R8918": (
            "Obscure implicit test dependency with mock.patch(%s). Rewrite to inject dependencies through constructor.",
            "explicit-dependency-required",
            DOC_EXPLICIT_DEPENDENCY_REQUIRED,
        ),
        "R8919": (
            "Obscure implicit test dependency with MagicMock(). Rewrite with create_autospec(ConcreteType).",
            "obscure-mock",
            DOC_OBSCURE_MOCK,
        ),
    }

    options = (
        (
            "require-explicit-dependency",
            {
                "default": ("databricks",),
                "type": "csv",
                "metavar": "<modules>",
                "help": "Package names that contain code for your project.",
            },
        ),
    )

    def open(self) -> None:
        self._require_explicit_dependency = self.linter.config.require_explicit_dependency

    def visit_call(self, node: nodes.Call) -> None:
        # this also means that rare cases, like MagicMock(side_effect=...) are fine
        if node.as_string() == "MagicMock()":
            # here we can go and figure out the expected type of the object being mocked based on the arguments
            # where it is being assigned to, but that is a bit too much for this check. Other people can add this later.
            self.add_message("obscure-mock", node=node)
        if not node.args:
            return
        if self._require_explicit_dependency and node.func.as_string() in {"mocker.patch", "patch"}:
            argument_value = node.args[0].as_string()
            no_quotes = argument_value.strip("'\"")
            for module in self._require_explicit_dependency:
                if not no_quotes.startswith(module):
                    continue
                self.add_message("explicit-dependency-required", node=node, args=argument_value)


def register(linter):
    linter.register_checker(MockingChecker(linter))
