import webbrowser
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat

this = Path(__file__)
w = WorkspaceClient()

whl = "databricks_labs_pylint-0.0.0-py3-none-any.whl"
home_dir = f"/Users/{w.current_user.me().user_name}/pylint"
w.workspace.mkdirs(home_dir)

with this.parent.parent.joinpath(f"dist/{whl}").open("rb") as f:
    w.workspace.upload(f"{home_dir}/{whl}", f, overwrite=True, format=ImportFormat.AUTO)

with this.parent.joinpath("runner.py").open("rb") as f:
    w.workspace.upload(f"{home_dir}/sample.py", f, overwrite=True, format=ImportFormat.AUTO)

webbrowser.open(f"{w.config.host}/#workspace{home_dir}/sample")
