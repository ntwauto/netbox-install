"""Common utilities for task commands."""
# pylint: disable=too-many-arguments
import os
import sys
from distutils.util import strtobool
from dotenv import load_dotenv
from rich.console import Console
from rich.theme import Theme

load_dotenv()

console = Console(
    color_system="truecolor",
    log_path=False,
    record=True,
    theme=Theme({"info": "cyan", "warning": "bold magenta", "error": "bold red", "good": "bold green"}),
    force_terminal=True,
)


try:
    import toml
except ImportError:
    sys.exit("Please make sure to `pip install toml` or enable the Poetry shell and run `poetry install`.")


def project_ver():
    """Find version from pyproject.toml to use for docker image tagging."""
    with open("pyproject.toml") as file:
        return toml.load(file)["tool"]["poetry"].get("version", "latest")


def project_name():
    """Find name from pyproject.toml to use for docker image tagging."""
    with open("pyproject.toml") as file:
        return toml.load(file)["tool"]["poetry"].get("name", "kittobs-builder")


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
    ```python
        >>> is_truthy('yes')
        True
    ```

    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(arg))

GIT_USER = os.getenv("GIT_USER", "ntwauto")
GIT_TOKEN = os.getenv("GIT_TOKEN", "")
DOCKER_USER = os.getenv("DOCKER_USER", "ntwauto")
DOCKER_TOKEN = os.getenv("DOCKER_TOKEN", "")
NETBOX_VER = os.getenv("NETBOX_VER", "v3.3.0")
NGINX_VER = os.getenv("NGINX_VER", "1.14.1")
GIT_REGISTRY = os.getenv("GIT_REGISTORY", "ghcr.io")
DOCKER_REGISTRY = os.getenv("DOCKER_REGISTORY", "docker.io")
NETBOX_PATH = os.getenv("NETBOX_PATH", ".netbox")
GIT_REPOSITORY_TAG = f"{GIT_REGISTRY}/{GIT_USER}/netbox:{NETBOX_VER}"
DOCKER_REPOSITORY_TAG = f"{DOCKER_REGISTRY}/{DOCKER_USER}/netbox:{NETBOX_VER}"
BUILD_ENV = {"NETBOX_VER": NETBOX_VER }
PROJECT_NAME = os.getenv("PROJECT_NAME", "netbox_devel")
PYTHON_VER = os.getenv("PYTHON_VER", "39")



def run_cmd(context, exec_cmd, envvars={}, exit_on_failure=True):  # pylint: disable=dangerous-default-value
    """Wrapper to run the invoke task commands."""
    console.log(f"Running command [orange1 i]{exec_cmd}", style="info")
    result = context.run(
        exec_cmd,
        pty=True,
        warn=True,
        env=envvars,
    )
    console.log(f"End of command: [orange1 i]{exec_cmd}", style="info")

    if exit_on_failure and not result.ok:
        console.log(f"Error has occurred\n{result.stderr}", style="error")
        sys.exit(result.return_code)

    return result.ok


def task_executor(result_ok, task_name):
    """Task execution wrapper around tasks that evaluates the result status and prints it Rich friendly.

    NOTE: This could have been a decorator but I haven't found a why that it can play nicely with the @task decorator
    Args:
        result_ok (bool): Run command status
        task_name (str): Name of the task executed to print out to terminal
    Returns:
        bool: Returns back the tasks result status
    """
    if result_ok:
        console.log(f"Successfully ran {task_name}", style="good")
    else:
        console.log(f"Issues encountered running {task_name}", style="warning")
    console.rule(f"End of task: [b i]{task_name}", style="info")
    console.print()
    return result_ok


def render_bool(value):
    """Rich string that renders from a boolean value.

    Args:
        value (bool): Bool value
    Returns:
        str: Rich-style string
    """
    return "[green b]Yes" if value is True else "[red b]No"
