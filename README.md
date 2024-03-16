<!-- FOR CONTRIBUTORS: Edit this file in Visual Studio Code with the recommended extensions, so that we update the table of contents automatically -->
# Databricks Labs PyLint Plugin


[![python](https://img.shields.io/badge/python-3.8,%203.9,%20,3.10,%203.11,%203.12-green)](https://github.com/databrickslabs/pylint-plugin/actions/workflows/push.yml)
[![codecov](https://codecov.io/github/databrickslabs/pylint-plugin/graph/badge.svg?token=x1JSVddfZa)](https://codecov.io/github/databrickslabs/pylint-plugin) [![lines of code](https://tokei.rs/b1/github/databrickslabs/pylint-plugin)]([https://codecov.io/github/databrickslabs/pylint-plugin](https://github.com/databrickslabs/pylint-plugin))


Checks for common mistakes and issues in Python code specifically in Databricks Environment.

<!-- TOC -->
* [Databricks Labs PyLint Plugin](#databricks-labs-pylint-plugin)
* [Installation](#installation)
* [Automated code analysis](#automated-code-analysis)
  * [`databricks-airflow` checker](#databricks-airflow-checker)
    * [`E9698`: `unsupported-runtime`](#e9698-unsupported-runtime)
    * [`E9699`: `missing-data-security-mode`](#e9699-missing-data-security-mode)
  * [`databricks-dbutils` checker](#databricks-dbutils-checker)
    * [`E9859`: `internal-api`](#e9859-internal-api)
    * [`E9869`: `pat-token-leaked`](#e9869-pat-token-leaked)
    * [`E9879`: `dbutils-notebook-run`](#e9879-dbutils-notebook-run)
    * [`E9889`: `dbutils-credentials`](#e9889-dbutils-credentials)
    * [`E9896`: `dbutils-fs-mount`](#e9896-dbutils-fs-mount)
    * [`E9897`: `dbutils-fs-ls`](#e9897-dbutils-fs-ls)
    * [`E9898`: `dbutils-fs-head`](#e9898-dbutils-fs-head)
    * [`E9899`: `dbutils-fs-cp`](#e9899-dbutils-fs-cp)
  * [`databricks-legacy` checker](#databricks-legacy-checker)
    * [`E9789`: `incompatible-with-uc`](#e9789-incompatible-with-uc)
    * [`E9799`: `legacy-cli`](#e9799-legacy-cli)
  * [`databricks-notebooks` checker](#databricks-notebooks-checker)
    * [`E9994`: `notebooks-percent-run`](#e9994-notebooks-percent-run)
    * [`E9996`: `notebooks-too-many-cells`](#e9996-notebooks-too-many-cells)
  * [`spark` checker](#spark-checker)
    * [`E9700`: `spark-outside-function`](#e9700-spark-outside-function)
    * [`E9701`: `no-spark-argument-in-function`](#e9701-no-spark-argument-in-function)
    * [`E9702`: `use-display-instead-of-show`](#e9702-use-display-instead-of-show)
  * [Testing in isolation](#testing-in-isolation)
* [Project Support](#project-support)
<!-- TOC -->

# Installation

You can install this project via `pip`:

```
pip install databricks-labs-pylint-plugin
```

and then use it with `pylint`:

```
pylint --load-plugins=databricks.labs.pylint.all <your-python-file>.py
```

[[back to top](#databricks-labs-pylint-plugin)]

# Automated code analysis

[[back to top](#databricks-labs-pylint-plugin)]

<!-- CHECKS -->

## `databricks-airflow` checker

[[back to top](#databricks-labs-pylint-plugin)]

### `E9698`: `unsupported-runtime`

XXX cluster has unsupported runtime: XXX. The runtime version is not supported by Unity Catalog. Please upgrade to a runtime greater than or equal to 11.3.

[[back to top](#databricks-labs-pylint-plugin)]

### `E9699`: `missing-data-security-mode`

XXX cluster missing `data_security_mode` required for Unity Catalog compatibility. Before you enable Unity Catalog, you must set the `data_security_mode` to 'NONE', so that your existing jobs would keep the same behavior. Failure to do so may cause your jobs to fail with unexpected errors.

[[back to top](#databricks-labs-pylint-plugin)]

## `databricks-dbutils` checker

[[back to top](#databricks-labs-pylint-plugin)]

### `E9859`: `internal-api`

Do not use internal APIs, rewrite using Databricks SDK: XXX. Do not use internal APIs. Use Databricks SDK for Python: https://databricks-sdk-py.readthedocs.io/en/latest/index.html

[[back to top](#databricks-labs-pylint-plugin)]

### `E9869`: `pat-token-leaked`

Use Databricks SDK instead: from databricks.sdk import WorkspaceClient(); w = WorkspaceClient(). Do not hardcode secrets in code, use Databricks SDK instead, which natively authenticates in Databricks Notebooks. See more at https://databricks-sdk-py.readthedocs.io/en/latest/authentication.html

[[back to top](#databricks-labs-pylint-plugin)]

### `E9879`: `dbutils-notebook-run`

Use Databricks SDK instead: w.jobs.submit(
                tasks=[jobs.SubmitTask(existing_cluster_id=...,
                                       notebook_task=jobs.NotebookTask(notebook_path=XXX),
                                       task_key=...)
                ]).result(timeout=timedelta(minutes=XXX)). Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at https://databricks-sdk-py.readthedocs.io/en/latest/workspace/jobs/jobs.html

[[back to top](#databricks-labs-pylint-plugin)]

### `E9889`: `dbutils-credentials`

Credentials utility is not supported with Unity Catalog. Migrate all usage to Unity Catalog

[[back to top](#databricks-labs-pylint-plugin)]

### `E9896`: `dbutils-fs-mount`

Mounts are not supported with Unity Catalog, switch to using Unity Catalog Volumes instead. Migrate all usage to Unity Catalog

[[back to top](#databricks-labs-pylint-plugin)]

### `E9897`: `dbutils-fs-ls`

Use Databricks SDK instead: w.dbfs.list(XXX). Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at https://databricks-sdk-py.readthedocs.io/en/latest/workspace/files/dbfs.html

[[back to top](#databricks-labs-pylint-plugin)]

### `E9898`: `dbutils-fs-head`

Use Databricks SDK instead: with w.dbfs.download(XXX) as f: f.read(). Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at https://databricks-sdk-py.readthedocs.io/en/latest/workspace/files/dbfs.html

[[back to top](#databricks-labs-pylint-plugin)]

### `E9899`: `dbutils-fs-cp`

Use Databricks SDK instead: w.dbfs.copy(XXX, XXX). Migrate all usage of dbutils to Databricks SDK. See the more detailed documentation at https://databricks-sdk-py.readthedocs.io/en/latest/workspace/files/dbfs.html

[[back to top](#databricks-labs-pylint-plugin)]

## `databricks-legacy` checker

[[back to top](#databricks-labs-pylint-plugin)]

### `E9789`: `incompatible-with-uc`

Incompatible with Unity Catalog: XXX. Migrate all usage to Databricks Unity Catalog. Use https://github.com/databrickslabs/ucx for more details

[[back to top](#databricks-labs-pylint-plugin)]

### `E9799`: `legacy-cli`

Don't use databricks_cli, use databricks.sdk instead: pip install databricks-sdk. Migrate all usage of Legacy CLI to Databricks SDK. See the more detailed documentation at https://databricks-sdk-py.readthedocs.io/en/latest/index.html

[[back to top](#databricks-labs-pylint-plugin)]

## `databricks-notebooks` checker

[[back to top](#databricks-labs-pylint-plugin)]

### `E9994`: `notebooks-percent-run`

Using %run is not allowed. Use functions instead of %run to avoid side effects and make the code more testable. If you need to share code between notebooks, consider creating a library. If still need to call another code as a separate job, use Databricks SDK for Python: https://databricks-sdk-py.readthedocs.io/en/latest/index.html

[[back to top](#databricks-labs-pylint-plugin)]

### `E9996`: `notebooks-too-many-cells`

Notebooks should not have more than 75 cells. Otherwise, it's hard to maintain and understand the notebook for other people and the future you

[[back to top](#databricks-labs-pylint-plugin)]

## `spark` checker

[[back to top](#databricks-labs-pylint-plugin)]

### `E9700`: `spark-outside-function`

Using spark outside the function is leading to untestable code. Do not use global spark object, pass it as an argument to the function instead, so that the function becomes testable in a CI/CD pipelines.

[[back to top](#databricks-labs-pylint-plugin)]

### `E9701`: `no-spark-argument-in-function`

Function XXX is missing a 'spark' argument. Function refers to a global spark variable, which may not always be available. Pass the spark object as an argument to the function instead, so that the function becomes testable in a CI/CD pipelines.

[[back to top](#databricks-labs-pylint-plugin)]

### `E9702`: `use-display-instead-of-show`

Rewrite to display in a notebook: display(XXX). Use display() instead of show() to visualize the data in a notebook.

[[back to top](#databricks-labs-pylint-plugin)]

## Testing in isolation
To test this plugin in isolation, you can use the following command:

```bash
pylint --load-plugins=databricks.labs.pylint.all --disable=all --enable=unsupported-runtime,missing-data-security-mode,internal-api,pat-token-leaked,dbutils-notebook-run,dbutils-credentials,dbutils-fs-mount,dbutils-fs-ls,dbutils-fs-head,dbutils-fs-cp,incompatible-with-uc,legacy-cli,notebooks-percent-run,notebooks-too-many-cells,spark-outside-function,no-spark-argument-in-function,use-display-instead-of-show .
```

[[back to top](#databricks-labs-pylint-plugin)]

<!-- END CHECKS -->

# Project Support

Please note that this project is provided for your exploration only and is not 
formally supported by Databricks with Service Level Agreements (SLAs). They are 
provided AS-IS, and we do not make any guarantees of any kind. Please do not 
submit a support ticket relating to any issues arising from the use of this project.

Any issues discovered through the use of this project should be filed as GitHub 
[Issues on this repository](https://github.com/databrickslabs/pylint-plugin/issues). 
They will be reviewed as time permits, but no formal SLAs for support exist.
