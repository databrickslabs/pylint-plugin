from databricks.labs.pylint.spark import SparkChecker


def test_spark_inside_function(lint_with):
    messages = (
        lint_with(SparkChecker)
        << """def do_something(spark, x):
    for i in range(10):
        if i > 3:
            continue
        spark #@
"""
    )
    assert not messages


def test_spark_outside_function(lint_with):
    messages = (
        lint_with(SparkChecker)
        << """for i in range(10):
    if i > 3:
        continue
    spark #@
"""
    )
    assert "[spark-outside-function] Using spark outside the function is leading to untestable code" in messages


def test_spark_inside_of_function_but_not_in_args(lint_with):
    messages = (
        lint_with(SparkChecker)
        << """def do_something(x):
    for i in range(10):
        if i > 3:
            continue
        spark #@
"""
    )
    assert "[no-spark-argument-in-function] Function do_something is missing a 'spark' argument" in messages


def test_df_show(lint_with):
    messages = lint_with(SparkChecker) << """__(spark.read.csv('file.csv').show)()"""
    assert (
        "[use-display-instead-of-show] Rewrite to display in a notebook: display(spark.read.csv('file.csv'))"
        in messages
    )
