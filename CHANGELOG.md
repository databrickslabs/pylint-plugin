# Version changelog

## 0.1.0

* Added checks for mocking best practices ([#27](https://github.com/databrickslabs/pylint-plugin/issues/27)). A new `mocking` checker has been added to the pylint plugin for Databricks to improve the quality of unit tests by enforcing best practices in mocking. This checker introduces two rules: `explicit-dependency-required` and `obscure-mock`. The `explicit-dependency-required` rule encourages injecting dependencies through constructors instead of using `mock.patch`, promoting code readability, maintainability, and dependency inversion for unit testing. The `obscure-mock` rule recommends using `create_autospec(ConcreteType)` over `MagicMock` to create mock objects that behave like concrete classes, resulting in more robust and maintainable unit tests. These rules can be configured to specify package names containing project code. This addition helps developers create reliable, maintainable, and testable code by adhering to recommended mocking practices.


## 0.0.1

Initial public release

## 0.0.0

Initial pylint plugin commit
