# netbox-install on podman

[The GitHub repository](netbox-install-github) houses the components needed to build NetBox as a container.
Netbox image was built on `ubi9' and pushed to [Docker Hub]. See the docker-compose.dev.yml file.

## Requirements
- python3 --version >= 3.6
- podman --version == 4.0.2
- podman-compose --version == 1.0.3 
- podman-plugins rpm installed

## Quickstart

To get Netbox up and running on podman run the following commands.

```console
$ git clone https://github.com/ntwauto/netbox-install.git
$ cd netbox-install
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U pip wheel setuptools
$ pip install -r requirements.txt
$ cp env.example .env
```

## Starting podman

To spin up netbox podman containers follow these steps:

```console
$ cd netbox-install
```
```console
##This command will list the available tasks
$ invoke --list 
```
```bash
(venv) [automate@devbox01 netbox-install]$ invoke --list
Available tasks:

  dev.debug               Start Netbox and its dependencies in debug mode.
  dev.destroy             Destroy all containers and volumes.
  dev.restart             Gracefully restart all containers.
  dev.restart-scheduler   Gracefully restart all containers.
  dev.start               Start Netbox and its dependencies in detached mode.
  dev.stop                Stop Netbox and its dependencies.
```
```console
##This command will list netbox containers
$ invoke dev.start
```
```bash
##You should see this output.

(venv) [automate@devbox01 netbox-install]$ podman ps
CONTAINER ID  IMAGE                                 COMMAND               CREATED         STATUS             PORTS                   NAMES
e69b3162b100  docker.io/library/postgres:14-alpine  postgres              24 seconds ago  Up 24 seconds ago                          netbox_devel_postgres_1
1cd4698b81e9  docker.io/library/redis:7-alpine      sh -c redis-serve...  22 seconds ago  Up 23 seconds ago                          netbox_devel_redis_1
17b113dcec79  docker.io/library/redis:7-alpine      sh -c redis-serve...  21 seconds ago  Up 21 seconds ago                          netbox_devel_redis-cache_1
5c2a47057f10  docker.io/ntwauto/netbox:v3.3.0       /opt/netbox/venv/...  19 seconds ago  Up 19 seconds ago                          netbox_devel_netbox-worker_1
68c4f900d329  docker.io/ntwauto/netbox:v3.3.0       /opt/netbox/house...  17 seconds ago  Up 17 seconds ago                          netbox_devel_netbox-housekeeping_1
19d733bbb42a  docker.io/ntwauto/netbox:v3.3.0       /opt/netbox/docke...  14 seconds ago  Up 12 seconds ago  0.0.0.0:8000->8080/tcp  netbox_devel_netbox_1

```console
## This will stop and remove all the containers
$ invoke dev.destroy
```

The whole application will be available after a few minutes.
Open the URL `http://0.0.0.0:8000/` in a web-browser.
You should see the NetBox homepage.
In the top-right corner you can login.
The default credentials are:

* Username: **admin**
* Password: **admin**
* API Token: **0123456789abcdef0123456789abcdef01234567**
