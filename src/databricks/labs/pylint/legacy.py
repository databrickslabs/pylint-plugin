# pylint checker for imports

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH, INFERENCE


class LegacyChecker(BaseChecker):
    name = "databricks-legacy"

    msgs = {
        "R8911": (
            "Don't use databricks_cli, use databricks.sdk instead: pip install databricks-sdk",
            "legacy-cli",
            "Migrate all usage of Legacy CLI to Databricks SDK. See the more detailed documentation at "
            "https://databricks-sdk-py.readthedocs.io/en/latest/index.html",
        ),
        "W8912": (
            "Incompatible with Unity Catalog: %s",
            "incompatible-with-uc",
            "Migrate all usage to Databricks Unity Catalog. Use https://github.com/databrickslabs/ucx for more details",
        ),
    }

    UC_INCOMPATIBLE_BRUTE_FORCE = {
        "s3fs",
        "boto3",
        "graphframes",
        "pyspark.ml",
        # literals
        "dbfs:",
        "hive_metastore.",
        "kafka.sasl.client.callback.handler.class",
        "kafka.sasl.login.callback.handler.class",
        "kafka.sasl.login.class",
        "kafka.partition.assignment.strategy",
        "kafka.ssl.truststore.location",
        "kafka.ssl.keystore.location",
        # calls
        # "sc.", triggers false positives for "misc."
        "spark.catalog.",
        "spark._jsparkSession.catalog",
        "spark._jspark",
        "spark._jvm",
        "._jdf",
        "._jcol",
        "spark.udf.registerJavaFunction",
        "applyInPandas",
        "mapInPandas",
        "_jvm",
        "SQLContext",
        "emptyRDD",
        "pickleFile",
        "textFile",
        "newAPIHadoopFile",
        "newAPIHadoopRDD",
        "hadoopFile",
        "hadoopRDD",
        "saveAsHadoopFile",
        "saveAsHadoopDataset",
        "saveAsNewAPIHadoopFile",
        "saveAsNewAPIHadoopDataset",
        "setJobGroup",
        "setLocalProperty",
        "applyInPandasWithState",
    }

    def visit_import(self, node: astroid.Import):
        # add message if databricks_cli is imported
        for name, _ in node.names:
            if name.startswith("databricks_cli"):
                self.add_message("legacy-cli", node=node, confidence=HIGH)
            # very coarse check for UC incompatibility
            for needle in self.UC_INCOMPATIBLE_BRUTE_FORCE:
                if needle in name:
                    self.add_message("incompatible-with-uc", node=node, args=(node.as_string(),), confidence=INFERENCE)

    def visit_importfrom(self, node: astroid.ImportFrom):
        if node.modname.startswith("databricks_cli"):
            self.add_message("legacy-cli", node=node)
        # very coarse check for UC incompatibility
        for needle in self.UC_INCOMPATIBLE_BRUTE_FORCE:
            if needle in node.modname:
                self.add_message("incompatible-with-uc", node=node, args=(node.as_string(),), confidence=INFERENCE)

    def visit_call(self, node: astroid.Call):
        func_as_string = node.func.as_string()
        # very coarse check for UC incompatibility
        for needle in self.UC_INCOMPATIBLE_BRUTE_FORCE:
            if needle in func_as_string:
                self.add_message("incompatible-with-uc", node=node, args=(node.as_string(),), confidence=INFERENCE)

    def visit_const(self, node: astroid.Const):
        # very coarse check for UC incompatibility
        value = node.value
        if not isinstance(value, str):
            return
        for needle in self.UC_INCOMPATIBLE_BRUTE_FORCE:
            if needle in value:
                self.add_message("incompatible-with-uc", node=node, args=(node.as_string(),), confidence=INFERENCE)


def register(linter):
    linter.register_checker(LegacyChecker(linter))
