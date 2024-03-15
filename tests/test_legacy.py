import pytest

from databricks.labs.pylint.legacy import LegacyChecker


@pytest.mark.parametrize(
    "code",
    [
        """import databricks_cli.foo""",
        """from databricks_cli.foo import bar""",
    ],
)
def test_legacy_cli(lint_with, code):
    messages = lint_with(LegacyChecker) << code
    assert "[legacy-cli] Don't use databricks_cli, use databricks.sdk instead: pip install databricks-sdk" in messages


@pytest.mark.parametrize(
    "code",
    [
        """spark.sql(
            'SELECT * FROM hive_metastore.default.foo' #@
        )""",
        """spark.read.format('delta').load(
            'dbfs:/foo/bar' #@
        )""",
        """{
            'kafka.sasl.client.callback.handler.class': 'foo', #@
        }""",
        """import pyspark.ml.foo""",
        """from pyspark.ml import bar""",
        """import graphframes""",
        """import boto3""",
        """import s3fs""",
        "spark.catalog.list()",
        "spark._jsparkSession.catalog.listTables()",
        "spark._jspark.anything()",
        "spark._jvm.anything()",
        "df._jdf.anything()",
        "df['foo']._jcol.anything()",
        "sc.setLocalProperty('foo', 'bar')",
    ],
)
def test_un_incompatible(lint_with, code):
    messages = lint_with(LegacyChecker) << code
    assert "[incompatible-with-uc] Incompatible with Unity Catalog" in messages.pop()
