# Databricks notebook source
# MAGIC %md # Here's markdown cell

# COMMAND ----------

# MAGIC %run ./something

# COMMAND ----------

# and here we do star import
from pyspark.sql.functions import *


# # COMMAND ----------
#
# # but no dbutils.library.restartPython()
# !pip install databricks-sdk

# COMMAND ----------

# MAGIC %md not good chaining

# COMMAND ----------

df = spark \
  .table('samples.nyctaxi.trips') \
  .limit(10)
display(df)

# COMMAND ----------

# MAGIC %md good chaining

# COMMAND ----------

df = (spark
  .table('samples.nyctaxi.trips')
  .limit(10))
display(df)
