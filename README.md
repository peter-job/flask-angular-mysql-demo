# Water quality management system

## Local development

### Dev Container

Included is a [dev container](https://containers.dev) configuration for creating an ephemeral development environment that should work out of the box.

See the [configuration file](../.devcontainer/devcontainer.json) for more details.

**Tested on:**

- MacOS 15

#### 1. Install dependencies

- [VS Code](https://code.visualstudio.com/download)
- [VS Code Extension: Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

#### 2. Clone the repo locally and open in VS Code

```bash
cd <path-to-your-projects>
git clone https://github.com/peter-job/<this-repo>.git
code <this-repo>
```

#### 3. Reopen the project in a dev container

Run the command `Dev Containers: Reopen in Container` from the command palette (Cmd+Shift+P or Ctrl+Shift+P)

This will open a new development environment for VS Code in a container. It might take a few minutes to build the first time.

> [!TIP]
> If you don't see this option, make sure you have the Dev Containers extension installed.

### Local development commands

Development commands are available in the [makefile](./makefile).

Required dependencies are automatically installed in the dev container, but you can also (re)install them using the provided makefile target:

```bash
make setup
```

### Local database

A local MySQL database and admin UI can be run using `docker compose`.
The configuration file is located at [db/docker-compose.yml](db/docker-compose.yml).

> [!IMPORTANT]
> The database is not started by default. You will need to start it manually.

> [!WARNING]
> The database is not persistent and any data will be lost when the container is stopped.
> To make it persistent, add a named volume to the [docker compose](db/docker-compose.yml) file.

To start the database, you can use the following command:

```bash
make db_start
```

To stop the database, you can use the following command:

```bash
make db_stop
```

To view the admin UI, you can navigate to [http://localhost:8080](http://localhost:8080) in your browser.
The default credentials are:

- username: `user`
- password: `password`
- database: `water_quality`

### Local Flask API

To run the API locally, you can use the following makefile target:

```bash
make api_start
```

The API will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

Water quality routes are defined in a [Flask blueprint](./api/blueprints/records/routes.py), and have the prefix `/records`.

You can run a manual test using the following command:

```bash
curl http://127.0.0.1:5000/records
```

To stop the API, you can kill the process in your terminal with `Ctrl+C`.

### Testing the API

Unit tests are available for the API and can be run using the following makefile target:

```bash
make api_test
```

### Local Angular UI

To run the Angular UI locally, you can use the following makefile target:

```bash
make ui_start
```

The UI will be available at [http://127.0.0.1:4200](http://127.0.0.1:4200).

> [!IMPORTANT]
> The UI will not work without the API running.

To stop the UI, you can kill the process in your terminal with `Ctrl+C`.

## Python dependency management with uv

[uv](https://docs.astral.sh/uv/) is a python package and project manager that is used here to manage dependencies.

If it hasn't already been installed, you can install it using the following makefile target:

```bash
make uv_install
```

A virtual environment should also be created under the [venv](./venv) directory. You can also create it using the makefile target:

```bash
make uv_venv
```

Python packages should already be installed in the virtual environment. You can install them yourself using the following makefile target:

```bash
make uv_sync
```

Packages are tracked in the [pyproject.toml](./pyproject.toml) file. You can add or remove them with the uv command line:

```bash
uv add <package>
uv remove <package>
```

### Python linting and formatting

Linting and formatting for Python code is done using [ruff](https://docs.astral.sh/ruff/).

You can run both linting and formatting using the following makefile target:

```bash
make ruff_check
```
