from pathlib import Path

import pytest
from pylint.testutils.functional import FunctionalTestFile, get_functional_test_files_from_directory
from pylint.testutils.lint_module_test import LintModuleTest

from databricks.labs.pylint import all

functional_tests = get_functional_test_files_from_directory(Path(__file__).parent / "samples")
ids = [f.base for f in functional_tests]


@pytest.mark.parametrize("sample", functional_tests, ids=ids)
def test_samples(sample: FunctionalTestFile) -> None:
    thing = LintModuleTest(sample)
    all.register(thing._linter)
    thing.setUp()
    thing.runTest()
