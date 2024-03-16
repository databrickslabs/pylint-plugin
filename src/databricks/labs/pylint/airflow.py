from typing import Any, Dict, List

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import INFERENCE


class AirflowChecker(BaseChecker):
    name = "databricks-airflow"

    msgs = {
        "W8901": (
            "%s cluster missing `data_security_mode` required for Unity Catalog compatibility",
            "missing-data-security-mode",
            "Before you enable Unity Catalog, you must set the `data_security_mode` to 'NONE',"
            " so that your existing jobs would keep the same behavior. Failure to do so may cause "
            "your jobs to fail with unexpected errors.",
        ),
        "W8902": (
            "%s cluster has unsupported runtime: %s",
            "unsupported-runtime",
            "The runtime version is not supported by Unity Catalog. Please upgrade to a runtime greater "
            "than or equal to 11.3.",
        ),
    }

    def visit_call(self, node: astroid.Call):
        operator = node.func.as_string()
        if operator not in ("DatabricksCreateJobsOperator", "DatabricksSubmitRunOperator"):
            return
        for arg, value in self._infer_kwargs(node.keywords).items():
            if arg == "tasks":
                self._check_tasks(value, node)
            elif arg == "job_clusters":
                self._check_job_clusters(value, node)
            elif arg == "new_cluster":
                self._check_new_cluster("ephemeral", value, node)

    def _check_new_cluster(self, key: str, new_cluster: Dict[str, Any], node: astroid.NodeNG):
        if "data_security_mode" not in new_cluster:
            self.add_message("missing-data-security-mode", node=node, args=(key,), confidence=INFERENCE)
        if "spark_version" in new_cluster and not self._is_supported(new_cluster["spark_version"]):
            self.add_message(
                "unsupported-runtime", node=node, args=(key, new_cluster["spark_version"]), confidence=INFERENCE
            )

    @staticmethod
    def _is_supported(spark_version: str):
        try:
            split = spark_version.split("-")
            if len(split) < 2:
                return False
            digits = split[0].split(".")
            if len(digits) < 2:
                return False
            return (int(digits[0]), int(digits[1])) >= (11, 3)
        except ValueError:
            return False

    def _check_tasks(self, tasks: List[Dict[str, Any]], node: astroid.NodeNG):
        for task in tasks:
            if "new_cluster" not in task:
                return
            self._check_new_cluster(task["task_key"], task["new_cluster"], node)

    def _check_job_clusters(self, job_clusters: List[Dict[str, Any]], node: astroid.NodeNG):
        for job_cluster in job_clusters:
            if "new_cluster" not in job_cluster:
                return
            self._check_new_cluster(job_cluster["job_cluster_key"], job_cluster["new_cluster"], node)

    def _infer_kwargs(self, keywords: List[astroid.Keyword]):
        kwargs = {}
        for keyword in keywords:
            kwargs[keyword.arg] = self._infer_value(keyword.value)
        return kwargs

    def _infer_value(self, value: astroid.NodeNG):
        if isinstance(value, astroid.Dict):
            return self._infer_dict(value)
        if isinstance(value, astroid.List):
            return self._infer_list(value)
        if isinstance(value, astroid.Const):
            return value.value
        if isinstance(value, astroid.Tuple):
            return tuple(self._infer_value(elem) for elem in value.elts)
        if isinstance(value, astroid.DictUnpack):
            return {self._infer_value(key): self._infer_value(value) for key, value in value.items}
        if isinstance(value, astroid.Name):
            for inferred in value.inferred():
                return self._infer_value(inferred)
            raise ValueError(f"Cannot resolve variable: {value.name}")
        raise ValueError(f"Unsupported type {type(value)}")

    def _infer_dict(self, in_dict: astroid.Dict):
        out_dict = {}
        for in_key, in_value in in_dict.items:
            out_key = self._infer_value(in_key)
            out_value = self._infer_value(in_value)
            out_dict[out_key] = out_value
        return out_dict

    def _infer_list(self, list_: astroid.List):
        out_list = []
        for elem in list_.elts:
            list_ = self._infer_value(elem)
            out_list.append(list_)
        return out_list


def register(linter):
    linter.register_checker(AirflowChecker(linter))
