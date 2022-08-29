"""Tasks for use with Invoke.

(c) 2020-2021 Network To Code
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import time
from datetime import datetime
from pathlib import Path
from distutils.util import strtobool
from invoke import task
from .common import (
    BUILD_ENV,
    PROJECT_NAME,
    run_cmd,
    console,
    task_executor,
)

COMPOSE_DIR = os.getenv("COMPOSE_DIR", "deployment")
COMPOSE_FILE_DEV = os.getenv("COMPOSE_FILE_DEV", "docker-compose.dev.yml")
COMPOSE_OVERRIDE_FILE = os.getenv("COMPOSE_OVERRIDE_FILE", "")
COMPOSE_FILE_PATH = os.path.join(COMPOSE_DIR, COMPOSE_FILE_DEV)
COMPOSE_OVERRIDE_PATH = os.path.join(COMPOSE_DIR, COMPOSE_OVERRIDE_FILE)


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task
def debug(context, exit_on_failure=True):
    """Start Netbox and its dependencies in debug mode."""
    console.log("Starting Netbox in debug mode...")

    pg_data = Path(COMPOSE_DIR) / "postgres_data"
    pg_data.mkdir(exist_ok=True)

    exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" up'
    return task_executor(
        run_cmd(
            context,
            exec_cmd,
            envvars=BUILD_ENV,
            exit_on_failure=exit_on_failure,
        ),
        "debugg deployment",
    )


@task
def start(context, exit_on_failure=True):
    """Start Netbox and its dependencies in detached mode."""
    console.log("Starting Netbox in detached mode...")

    pg_data = Path(COMPOSE_DIR) / "postgres_data"
    pg_data.mkdir(exist_ok=True)
    
    if os.path.exists(COMPOSE_OVERRIDE_PATH):
        exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" -f "{COMPOSE_OVERRIDE_PATH}" up -d --remove-orphans'
    else:
        exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" up -d --remove-orphans'
        
    return task_executor(
        run_cmd(
            context,
            exec_cmd,
            envvars=BUILD_ENV,
            exit_on_failure=exit_on_failure,
        ),
        "start deployment",
    )


@task
def restart(context, exit_on_failure=True):
    """Gracefully restart all containers."""
    console.log("Restarting Netbox...")
    exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" restart netbox redis postgres worker scheduler'
    return task_executor(
        run_cmd(
            context,
            exec_cmd,
            envvars=BUILD_ENV,
            exit_on_failure=exit_on_failure,
        ),
        "restart deployment",
    )


@task
def restart_scheduler(context, exit_on_failure=True):
    """Gracefully restart all containers."""
    console.log("Restarting Netbox...")
    exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" restart scheduler'
    return task_executor(
        run_cmd(
            context,
            exec_cmd,
            envvars=BUILD_ENV,
            exit_on_failure=exit_on_failure,
        ),
        "restart deployment",
    )


@task
def stop(context, exit_on_failure=True):
    """Stop Netbox and its dependencies."""
    console.log("Stopping Netbox...")
    exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" stop netbox redis postgres worker scheduler'
    return task_executor(
        run_cmd(
            context,
            exec_cmd,
            envvars=BUILD_ENV,
            exit_on_failure=exit_on_failure,
        ),
        "stop deployment",
    )


@task
def destroy(context, exit_on_failure=True):
    """Destroy all containers and volumes."""
    console.log("Destroying Netbox...")
    exec_cmd = f'podman-compose --project-name "{PROJECT_NAME}" -f "{COMPOSE_FILE_PATH}" down'
    return task_executor(
        run_cmd(
            context,
            exec_cmd,
            envvars=BUILD_ENV,
            exit_on_failure=exit_on_failure,
        ),
        "destroy deployment",
    )

