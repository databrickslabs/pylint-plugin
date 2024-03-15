import astroid
from pylint.checkers import BaseChecker


class AirflowChecker(BaseChecker):
    name = "databricks-airflow"

    msgs = {
        "E9699": (
            "%s cluster missing 'data_security_mode' required for Unity Catalog compatibility",
            "missing-data-security-mode",
            "new_cluster is missing data_security_mode",
        ),
    }

    def visit_call(self, node: astroid.Call):
        operator = node.func.as_string()
        if operator not in ("DatabricksCreateJobsOperator", "DatabricksSubmitRunOperator"):
            return
        for kwarg in node.keywords:
            if kwarg.arg == "tasks":
                self._check_tasks(kwarg.value)
                continue
            if kwarg.arg == "job_clusters":
                self._check_job_clusters(kwarg.value)
                continue

    def _check_tasks(self, value: astroid.NodeNG):
        for inferred in value.infer():
            for task in self._infer_value(inferred):
                if "new_cluster" not in task:
                    continue
                raise ValueError("new_cluster is missing data_security_mode")

    def _check_job_clusters(self, value: astroid.NodeNG):
        for inferred in value.infer():
            for job_cluster in self._infer_value(inferred):
                if "new_cluster" not in job_cluster:
                    continue
                # add message that this job cluster is missing data_security_mode
                self.add_message("missing-data-security-mode", node=value, args=(job_cluster["job_cluster_key"],))

    def _infer_value(self, value: astroid.NodeNG):
        if isinstance(value, (str, int, bool, list, dict, type(None))):
            return value
        if isinstance(value, astroid.Dict):
            return self._infer_dict(value)
        if isinstance(value, astroid.List):
            return self._infer_list(value)
        if isinstance(value, astroid.Const):
            return value.value
        raise ValueError(f"Unsupported type {type(value)}")

    def _infer_dict(self, in_dict: astroid.Dict):
        out_dict = {}
        for in_key, in_value in in_dict.items:
            out_key = self._infer_value(in_key.value)
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
