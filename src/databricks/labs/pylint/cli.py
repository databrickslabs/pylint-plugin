import json
import logging
import os
import pathlib
import re
import subprocess
import sys
import tempfile

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ExportFormat, Language, ObjectInfo, ObjectType

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(asctime)s [%(name)s][%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

payload = json.loads(sys.argv[1])
flags = payload["flags"]

if flags.get("log_level", "info").lower() == "debug":
    logging.getLogger("databricks.sdk").setLevel(logging.DEBUG)

w = WorkspaceClient()

path = flags.get("path")
if not path:
    path = f"/Users/{w.current_user.me().user_name}"


def check_python_notebook(info: ObjectInfo):
    if info.object_type != ObjectType.NOTEBOOK:
        return
    if info.language != Language.PYTHON:
        return
    logger.info(f"👀 checking: {info.path}")
    with tempfile.TemporaryDirectory() as tmpdir:
        with w.workspace.download(info.path, format=ExportFormat.SOURCE) as f:
            basename = os.path.basename(info.path)
            # replace non-alphanumeric characters with underscores
            basename = re.sub(r"\W+", "_", basename)
            tmp_path = pathlib.Path(tmpdir, basename)
            with tmp_path.open("wb") as nb:
                nb.write(f.read())
            command = [
                "pylint",
                "--load-plugins=databricks.labs.pylint.all",
                "--disable=all",
                "--enable=missing-data-security-mode,unsupported-runtime,dbutils-fs-cp,dbutils-fs-head,dbutils-fs-ls,dbutils-fs-mount,dbutils-credentials,dbutils-notebook-run,pat-token-leaked,internal-api,legacy-cli,incompatible-with-uc,notebooks-too-many-cells,notebooks-percent-run,spark-outside-function,use-display-instead-of-show,no-spark-argument-in-function",
                tmp_path.as_posix(),
            ]
            with subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            ) as process:
                for line in iter(process.stdout.readline, ""):
                    print(line, end="")


status = w.workspace.get_status(path)
if status.object_type == ObjectType.DIRECTORY:
    for item in w.workspace.list(path):
        check_python_notebook(item)
elif status.object_type == ObjectType.NOTEBOOK:
    check_python_notebook(status)
else:
    print(f"❌ {path} is not a notebook or directory")
