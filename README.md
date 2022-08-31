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

### Easy install

 OR you can run this simple shell script to take care of the steps above.
 
### Start podman

To spin up netbox podman containers follow these steps:

```console
$ cd netbox-install
```
```console
##This command will list the available tasks
$ invoke --list 
```
```bash

```
```console
```
```console
```
$ invoke dev.start ## This will start podman-compose
$
```

The whole application will be available after a few minutes.
Open the URL `http://0.0.0.0:8000/` in a web-browser.
You should see the NetBox homepage.
In the top-right corner you can login.
The default credentials are:

* Username: **admin**
* Password: **admin**
* API Token: **0123456789abcdef0123456789abcdef01234567**
