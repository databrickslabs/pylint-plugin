# pylint checker for databricks dbutils
import astroid
from pylint.checkers import BaseChecker


class DbutilsChecker(BaseChecker):
    name = "dbutils"

    msgs = {
        "E9899": (
            "Use Databricks SDK instead: w.dbfs.copy(%s, %s)",
            "dbutils-fs-cp",
            "Migrate all usage of dbutils to Databricks SDK",
        ),
        "E9898": (
            "Use Databricks SDK instead: with w.dbfs.download(%s) as f: f.read()",
            "dbutils-fs-head",
            "Migrate all usage of dbutils to Databricks SDK",
        ),
        "E9897": (
            "Use Databricks SDK instead: w.dbfs.list(%s)",
            "dbutils-fs-ls",
            "Migrate all usage of dbutils to Databricks SDK",
        ),
        "E9896": (
            "Mounts are not supported with Unity Catalog, switch to using Unity Catalog Volumes instead",
            "dbutils-fs-mount",
            "Migrate all usage to Unity Catalog",
        ),
        "E9889": (
            "Credentials utility is not supported with Unity Catalog",
            "dbutils-credentials",
            "Migrate all usage to Unity Catalog",
        ),
        "E9879": (
            """Use Databricks SDK instead: w.jobs.submit(
                tasks=[jobs.SubmitTask(existing_cluster_id=...,
                                       notebook_task=jobs.NotebookTask(notebook_path=%s),
                                       task_key=...)
                ]).result(timeout=timedelta(minutes=%s))""",
            "dbutils-notebook-run",
            "Migrate all usage of dbutils to Databricks SDK",
        ),
        "E9869": (
            "Use Databricks SDK instead: from databricks.sdk import WorkspaceClient(); w = WorkspaceClient()",
            "pat-token-leaked",
            "Do not hardcode secrets in code, use Databricks Scopes instead",
        ),
    }

    def visit_call(self, node: astroid.Call):
        # add message if dbutils.fs.cp() is used
        if node.func.as_string() == "dbutils.fs.cp":
            self.add_message("dbutils-fs-cp", node=node, args=(node.args[0].as_string(), node.args[1].as_string()))
        # add message if dbutils.fs.head() is used
        if node.func.as_string() == "dbutils.fs.head":
            self.add_message("dbutils-fs-head", node=node, args=(node.args[0].as_string(),))
        # add message if dbutils.fs.ls("/tmp") is used
        if node.func.as_string() == "dbutils.fs.ls":
            self.add_message("dbutils-fs-ls", node=node, args=(node.args[0].as_string(),))
        # add message if dbutils.fs.mount("s3a://%s" % aws_bucket_name, "/mnt/%s" % mount_name) is used
        if node.func.as_string() in {
            "dbutils.fs.mount",
            "dbutils.fs.mounts",
            "dbutils.fs.unmount",
            "dbutils.fs.updateMount",
            "dbutils.fs.refreshMounts",
        }:
            self.add_message("dbutils-fs-mount", node=node)
        # add message if dbutils.credentials.* is used
        if node.func.as_string().startswith("dbutils.credentials."):
            self.add_message("dbutils-credentials", node=node)
        # add message if dbutils.notebook.run("My Other Notebook", 60) is used
        if node.func.as_string() == "dbutils.notebook.run":
            self.add_message(
                "dbutils-notebook-run", node=node, args=(node.args[0].as_string(), node.args[1].as_string())
            )

    def visit_const(self, node: astroid.Const):
        # add a message if string matches dapi[0-9a-f]{32}, dkea[0-9a-f]{32}, or dosa[0-9a-f]{32}
        if node.value.startswith("dapi") or node.value.startswith("dkea") or node.value.startswith("dosa"):
            self.add_message("pat-token-leaked", node=node)


def register(linter):
    linter.register_checker(DbutilsChecker(linter))
