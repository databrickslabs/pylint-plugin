# pylint checker for databricks dbutils
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH


class DbutilsChecker(BaseChecker):
    name = "databricks-dbutils"

    msgs = {
        "R8903": (
            "Use Databricks SDK instead: w.dbfs.copy(%s, %s)",
            "dbutils-fs-cp",
            "Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at "
            "https://databricks-sdk-py.readthedocs.io/en/latest/workspace/files/dbfs.html",
        ),
        "R8904": (
            "Use Databricks SDK instead: with w.dbfs.download(%s) as f: f.read()",
            "dbutils-fs-head",
            "Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at "
            "https://databricks-sdk-py.readthedocs.io/en/latest/workspace/files/dbfs.html",
        ),
        "R8905": (
            "Use Databricks SDK instead: w.dbfs.list(%s)",
            "dbutils-fs-ls",
            "Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at "
            "https://databricks-sdk-py.readthedocs.io/en/latest/workspace/files/dbfs.html",
        ),
        "R8906": (
            "Mounts are not supported with Unity Catalog, switch to using Unity Catalog Volumes instead",
            "dbutils-fs-mount",
            "Migrate all usage to Unity Catalog",
        ),
        "R8907": (
            "Credentials utility is not supported with Unity Catalog",
            "dbutils-credentials",
            "Migrate all usage to Unity Catalog",
        ),
        "R8908": (
            """Use Databricks SDK instead: w.jobs.submit(
                tasks=[jobs.SubmitTask(existing_cluster_id=...,
                                       notebook_task=jobs.NotebookTask(notebook_path=%s),
                                       task_key=...)
                ]).result(timeout=timedelta(minutes=%s))""",
            "dbutils-notebook-run",
            "Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at "
            "https://databricks-sdk-py.readthedocs.io/en/latest/workspace/jobs/jobs.html",
        ),
        "R8909": (
            "Use Databricks SDK instead: from databricks.sdk import WorkspaceClient(); w = WorkspaceClient()",
            "pat-token-leaked",
            "Do not hardcode secrets in code, use Databricks SDK instead, which natively authenticates in Databricks "
            "Notebooks. See more at https://databricks-sdk-py.readthedocs.io/en/latest/authentication.html",
        ),
        "R8910": (
            "Do not use internal APIs, rewrite using Databricks SDK: %s",
            "internal-api",
            "Do not use internal APIs. Use Databricks SDK for Python: "
            "https://databricks-sdk-py.readthedocs.io/en/latest/index.html",
        ),
    }

    def visit_call(self, node: astroid.Call):
        # add message if dbutils.fs.cp() is used
        func_as_string = node.func.as_string()
        if func_as_string == "dbutils.fs.cp":
            self.add_message(
                "dbutils-fs-cp", node=node, args=(node.args[0].as_string(), node.args[1].as_string()), confidence=HIGH
            )
        # add message if dbutils.fs.head() is used
        elif func_as_string == "dbutils.fs.head":
            self.add_message("dbutils-fs-head", node=node, args=(node.args[0].as_string(),), confidence=HIGH)
        # add message if dbutils.fs.ls("/tmp") is used
        elif func_as_string == "dbutils.fs.ls":
            self.add_message("dbutils-fs-ls", node=node, args=(node.args[0].as_string(),), confidence=HIGH)
        # add message if dbutils.fs.mount("s3a://%s" % aws_bucket_name, "/mnt/%s" % mount_name) is used
        elif func_as_string in {
            "dbutils.fs.mount",
            "dbutils.fs.mounts",
            "dbutils.fs.unmount",
            "dbutils.fs.updateMount",
            "dbutils.fs.refreshMounts",
        }:
            self.add_message("dbutils-fs-mount", node=node, confidence=HIGH)
        # add message if dbutils.credentials.* is used
        elif func_as_string.startswith("dbutils.credentials."):
            self.add_message("dbutils-credentials", node=node, confidence=HIGH)
        # add message if dbutils.notebook.run("My Other Notebook", 60) is used
        elif func_as_string == "dbutils.notebook.run":
            self.add_message(
                "dbutils-notebook-run",
                node=node,
                args=(node.args[0].as_string(), node.args[1].as_string()),
                confidence=HIGH,
            )
        elif func_as_string.endswith("getDbutils"):
            self.add_message("internal-api", node=node, args=(node.as_string(),), confidence=HIGH)
        elif ".notebook().getContext()" in func_as_string:
            self.add_message("internal-api", node=node, args=(node.as_string(),), confidence=HIGH)
        elif ".notebook.entry_point" in func_as_string:
            self.add_message("internal-api", node=node, args=(node.as_string(),), confidence=HIGH)
        elif ".apiToken" in func_as_string:
            self.add_message("internal-api", node=node, args=(node.as_string(),), confidence=HIGH)

    def visit_const(self, node: astroid.Const):
        value = node.value
        if not isinstance(value, str):
            return
        # add a message if string matches dapi[0-9a-f]{32}, dkea[0-9a-f]{32}, or dosa[0-9a-f]{32}
        if value.startswith("dapi") or value.startswith("dkea") or value.startswith("dosa"):
            self.add_message("pat-token-leaked", node=node, confidence=HIGH)

    def visit_import(self, node: astroid.Import):
        # add a message if dbruntime is imported
        for name_tuple in node.names:
            real_name, _ = name_tuple
            if real_name.startswith("dbruntime"):
                self.add_message("internal-api", node=node, args=(node.as_string(),), confidence=HIGH)

    def visit_importfrom(self, node: astroid.ImportFrom):
        # add a message if dbruntime is imported
        if node.modname.startswith("dbruntime"):
            self.add_message("internal-api", node=node, args=(node.as_string(),), confidence=HIGH)


def register(linter):
    linter.register_checker(DbutilsChecker(linter))
