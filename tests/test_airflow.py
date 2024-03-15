from databricks.labs.pylint.airflow import AirflowChecker


def test_missing_data_security_mode_in_job_clusters(lint_with):
    messages = (
        lint_with(AirflowChecker)
        << """from airflow.providers.databricks.operators.databricks import DatabricksCreateJobsOperator
tasks = [
    {
        "task_key": "test",
        "job_cluster_key": "job_cluster",
        "notebook_task": {
            "notebook_path": "/Shared/test",
        },
    },
]
job_clusters = [
    {
        "job_cluster_key": "banana",
        "new_cluster": {
            "spark_version": "7.3.x-scala2.12",
            "node_type_id": "i3.xlarge",
            "num_workers": 2,
        },
    },
]
DatabricksCreateJobsOperator( #@
    task_id="jobs_create_named", 
    tasks=tasks, 
    job_clusters=job_clusters
)"""
    )
    assert (
        "[missing-data-security-mode] banana cluster missing `data_security_mode` "
        "required for Unity Catalog compatibility"
    ) in messages


def test_missing_data_security_mode_in_task_clusters(lint_with):
    messages = (
        lint_with(AirflowChecker)
        << """from airflow.providers.databricks.operators.databricks import DatabricksCreateJobsOperator
tasks = [
    {
        "task_key": "banana",
        "notebook_task": {
            "notebook_path": "/Shared/test",
        },
        'new_cluster': {
            "spark_version": "7.3.x-scala2.12",
            "node_type_id": "i3.xlarge",
            "num_workers": 2,
        },
    },
]
DatabricksCreateJobsOperator( #@
    task_id="jobs_create_named", 
    tasks=tasks
)"""
    )
    assert (
        "[missing-data-security-mode] banana cluster missing `data_security_mode` "
        "required for Unity Catalog compatibility"
    ) in messages


def test_missing_data_security_mode_in_submit_run_clusters(lint_with):
    messages = (
        lint_with(AirflowChecker)
        << """from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
new_cluster = {"spark_version": "10.1.x-scala2.12", "num_workers": 2}
notebook_task = {
    "notebook_path": "/Users/airflow@example.com/PrepareData",
}
DatabricksSubmitRunOperator( #@
    task_id="notebook_run", new_cluster=new_cluster, notebook_task=notebook_task
)"""
    )
    assert "[unsupported-runtime] ephemeral cluster has unsupported runtime: 10.1.x-scala2.12" in messages
    assert (
        "[missing-data-security-mode] ephemeral cluster missing `data_security_mode` "
        "required for Unity Catalog compatibility"
    ) in messages
