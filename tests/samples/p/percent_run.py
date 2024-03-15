# Databricks notebook source
# pylint: disable=missing-module-docstring,undefined-variable

# COMMAND ----------

# +1: [notebooks-percent-run]
# MAGIC %run ./something

# COMMAND ----------

# MAGIC %md not good chaining

# COMMAND ----------

df = spark.table("samples.nyctaxi.trips").limit(10)  # [spark-outside-function]
display(df)

# COMMAND ----------

# MAGIC %md good chaining

# COMMAND ----------

df = spark.table("samples.nyctaxi.trips").limit(10)  # [spark-outside-function]
display(df)
