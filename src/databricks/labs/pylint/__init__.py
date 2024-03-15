import logging

from databricks.labs.pylint.__about__ import __version__

logger = logging.getLogger(__name__)

try:
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient(product="pylint", product_version=__version__)
    w.current_user.me()
except ValueError:
    logger.warning(
        "Set DATABRICKS_HOST environment variable to track the usage of this plugin and support "
        "its development. This will help us to understand the usage of this plugin and improve it. "
        "See https://docs.databricks.com/en/dev-tools/auth.html#databricks-client-unified-authentication"
    )
except ImportError:
    pass
