from databricks.labs.pylint.airflow import AirflowChecker


def test_missing_data_security_mode_in_job_clusters(lint_with):
    messages = (
        lint_with(AirflowChecker)
        << """from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
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
        "[missing-data-security-mode] banana cluster missing 'data_security_mode' "
        "required for Unity Catalog compatibility"
    ) in messages


def test_missing_data_security_mode_in_task_clusters(lint_with):
    messages = (
        lint_with(AirflowChecker)
        << """from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
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
        "[missing-data-security-mode] banana cluster missing 'data_security_mode' "
        "required for Unity Catalog compatibility"
    ) in messages
