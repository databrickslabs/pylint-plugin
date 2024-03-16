# Databricks notebook source

# COMMAND ----------

# MAGIC %pip install ./databricks_labs_pylint-0.0.0-py3-none-any.whl --force-reinstall
dbutils.library.restartPython()  # noqa
# MAGIC %load_ext databricks.labs.pylint.magic

# COMMAND ----------

from databricks.labs.pylint.magic import enable

enable()

# COMMAND ----------

# MAGIC %%pylint
# MAGIC print('dbfs:foo')
