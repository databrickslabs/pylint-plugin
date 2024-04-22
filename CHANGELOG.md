# Version changelog

## 0.3.0

* Added integration with `eradicate` to highlight dead code ([#39](https://github.com/databrickslabs/pylint-plugin/issues/39)). This release integrates the `eradicate` project, a tool for identifying dead code in Python, into the project's code analysis and testing workflow. This integration will help enforce dead code removal, improve code quality, and make debugging easier by identifying and highlighting dead code. The `C8920` check in the Pylint plugin reports any commented out code, and it can be disabled on a specific line by adding `# pylint: disable=dead-code` at the end of it.


## 0.2.0

* Added documentation on how to enable specific checkers and how to silence specific warnings ([#37](https://github.com/databrickslabs/pylint-plugin/issues/37)). The latest release introduces new documentation in the README file for enabling specific checkers and disabling specific warnings for the pylint plugin for Databricks. The plugin offers checkers such as `databricks-airflow`, `databricks-dbutils`, `databricks-legacy`, `databricks-notebooks`, `spark`, and `mocking`, each with unique checks and codes. Users can use these checkers by adding the corresponding module name to the `load-plugins` configuration in their `pylintrc` or `pyproject.toml` file. The release also explains how to disable certain checks on specific lines using a comment with the `disable` directive followed by the corresponding symbol. Additionally, it includes information on how to use the Databricks SDK instead of internal APIs, legacy CLI, and dbutils. The `docs.py` script has also been updated with the new instructions on how to enable or disable specific checkers and warnings.


## 0.1.1

* Fixed ToC for `mocking` checker ([#29](https://github.com/databrickslabs/pylint-plugin/issues/29)). In this release, we have made significant improvements to the `mocking` checker in our open-source library, which is specifically designed for identifying common mistakes and issues in Spark code written in Python. We have added two new rules, `R8918: explicit-dependency-required` and `R8919: obscure-mock`, which respectively check for the requirement of explicit dependencies and the use of obscure mocks. This update enhances the accuracy and quality of the code review process for Spark code written in Python, ensuring that the code meets the highest standards of quality and reliability. Additionally, we have fixed an issue in the Table of Contents (ToC) for the `mocking` checker, making it easier for users to navigate and utilize this feature.
* Fixed project urls for PyPI ([#32](https://github.com/databrickslabs/pylint-plugin/issues/32)). In this release, the `pyproject.toml` configuration file for the Python project has been updated to fix project URLs for PyPI. Specifically, the URLs for the `Issues` and `Source` fields have been changed from "<https://github.com/databrickslabs/pylint/issues>" and "<https://github.com/databrickslabs/pylint>" to "<https://github.com/databrickslabs/pylint-plugin/issues>" and "<https://github.com/databrickslabs/pylint-plugin>", respectively. This modification ensures that users can correctly report issues and access the source code for the pylint-plugin project on GitHub. The rest of the file remains unchanged. This enhancement provides a seamless experience for users who want to contribute to the project or seek support for any issues they encounter.
* Updated README.md to fix pip install command ([#30](https://github.com/databrickslabs/pylint-plugin/issues/30)). In this release, we have updated the installation command for the project to fix the pip install process. Previously, users installed the project using the command "pip install pylint-plugin-for-databricks", but this has been changed to "pip install databricks-labs-pylint". This update is part of issue [#30](https://github.com/databrickslabs/pylint-plugin/issues/30) and is intended to improve the installation experience for users. It is important to note that no new methods have been added and no existing functionality has been changed; only the installation command has been updated. Software engineers adopting this project should use the new command to install it.


## 0.1.0

* Added checks for mocking best practices ([#27](https://github.com/databrickslabs/pylint-plugin/issues/27)). A new `mocking` checker has been added to the pylint plugin for Databricks to improve the quality of unit tests by enforcing best practices in mocking. This checker introduces two rules: `explicit-dependency-required` and `obscure-mock`. The `explicit-dependency-required` rule encourages injecting dependencies through constructors instead of using `mock.patch`, promoting code readability, maintainability, and dependency inversion for unit testing. The `obscure-mock` rule recommends using `create_autospec(ConcreteType)` over `MagicMock` to create mock objects that behave like concrete classes, resulting in more robust and maintainable unit tests. These rules can be configured to specify package names containing project code. This addition helps developers create reliable, maintainable, and testable code by adhering to recommended mocking practices.


## 0.0.1

Initial public release

## 0.0.0

Initial pylint plugin commit
