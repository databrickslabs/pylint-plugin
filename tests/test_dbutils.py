import pytest

from databricks.labs.pylint.dbutils import DbutilsChecker


def test_checks_cp(lint_with):
    messages = lint_with(DbutilsChecker) << "dbutils.fs.cp('foo', 'bar')"
    assert "[dbutils-fs-cp] Use Databricks SDK instead: w.dbfs.copy('foo', 'bar')" in messages


def test_checks_head(lint_with):
    messages = lint_with(DbutilsChecker) << """dbutils.fs.head("/tmp/my_file.txt", 25)"""
    assert (
        "[dbutils-fs-head] Use Databricks SDK instead: with "
        "w.dbfs.download('/tmp/my_file.txt') as f: f.read()" in messages
    )


def test_checks_list(lint_with):
    messages = lint_with(DbutilsChecker) << """dbutils.fs.ls("/tmp")"""
    assert "[dbutils-fs-ls] Use Databricks SDK instead: w.dbfs.list('/tmp')" in messages


def test_checks_mount(lint_with):
    messages = (
        lint_with(DbutilsChecker)
        << """aws_bucket_name = "my-bucket"
mount_name = "s3-my-bucket"
dbutils.fs.mount("s3a://%s" % aws_bucket_name, "/mnt/%s" % mount_name)"""
    )
    assert (
        "[dbutils-fs-mount] Mounts are not supported with Unity Catalog, "
        "switch to using Unity Catalog Volumes instead"
    ) in messages


def test_checks_credentials(lint_with):
    messages = lint_with(DbutilsChecker) << """dbutils.credentials.assumeRole("arn:aws:iam::...:roles/my-role")"""
    assert "[dbutils-credentials] Credentials utility is not supported with Unity Catalog" in messages


def test_checks_notebook_run(lint_with):
    messages = lint_with(DbutilsChecker) << """dbutils.notebook.run("my_notebook", 5)"""
    assert len(messages) == 1


def test_checks_secrets(lint_with):
    messages = (
        lint_with(DbutilsChecker)
        << """do_something(
        'dapi00000000', #@ 
        'other',
    )"""
    )
    assert (
        "[pat-token-leaked] Use Databricks SDK instead: from databricks.sdk import "
        "WorkspaceClient(); w = WorkspaceClient()"
    ) in messages


@pytest.mark.parametrize(
    "code",
    [
        """import dbruntime.foo, bar""",
        """from dbruntime.foo import bar, baz""",
        "dbutils.notebook.entry_point.getDbutils()",
        """whatever['foo'].notebook.entry_point.getDbutils()""",
        """dbutils.notebook.entry_point.getDbutils().notebook().getContext()""",
        """blueberry.notebook().getContext().foo()""",
        """banana.apiToken()""",
    ],
)
def test_internal_api(lint_with, code):
    messages = lint_with(DbutilsChecker) << code
    assert f"[internal-api] Do not use internal APIs, rewrite using Databricks SDK: {code}" in messages
