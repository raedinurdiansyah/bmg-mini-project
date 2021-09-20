# Technical Test BMG Indonesia

Backend Service (Flask) for Technical Test Purpose

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Docker and docker-compose

Docker and docker-compose are used for running the database.

1. Install Docker and docker-compose
    visit [here](https://docs.docker.com/) to read more about docker installation

    ```shell
    $ docker --version
    Docker version 19.03.3, build a872fc2f86

    $ docker-compose --version
    docker-compose version 1.24.1, build 4667896b
    ```

2. Run docker container for database

    ```shell
    $ docker-compose -f docker/docker-compose.yml -p bmg up -d
    Creating bmg_test_db ... done
    ```

#### Pre-commit

Pre-commit is used to make sure the code stay healthy and readable and to prevent accidentaly commit to master or main

1. Goto your project directory

    ```shell
    $ cd /path/to/your/project/
    -
    ```

2. Activate your virtualenv

    ```shell
    $ source .venv/bin/activate
    (.venv) $
    ```

3. Install pre commit using pip

    ```shell
    $ pip install pre-commit
    Installing collected packages: pre-commit
    Successfully installed pre-commit-2.1.1
    ```

4. Install pre-commit hooks

    ```shell
    $ pre-commit install
    pre-commit installed at .git/hooks/pre-commit
    ```

5. Run pre-commit

    ```shell
    $ pre-commit run
    Trim trailing whitespace.................................Passed
    Fix end of files.........................................Passed
    Flake8...................................................Passed
    Detect private key.......................................Passed
    Don't commit to branch...................................Passed
    Check for merge conflicts................................Passed
    black....................................................Passed
    isort....................................................Passed
    ```

### Installing

1. Installing dependencies

    Installing python dependencies using poetry

    ```shell
    $ pip install poetry
    Collecting poetry...
    ```

    Then just install dependencies

    ```shell
    $ poetry install
    -
    ```

2. Update database migrations to the latest version

    ```shell
    $ flask db upgrade head
    -
    ```

3. Running development server

    ```shell
    $ flask run
    -
    ```

    if you need to launch flask shell

    ```shell
    $ flask shell
    -
    ```


### Test

* Always write your test first
* Keep coverage higher than 80%

* running the test with coverage info

    ```shell script
    coverage run -m unittest discover
    ```
    then to show the report

    ```shell script
    coverage report
    ```

***TBD***


## Built With

* [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
* [docker-compose](https://docs.docker.com/compose/) - Compose is a tool for defining and running multi-container Docker applications.
* [Flask](https://flask.palletsprojects.com) - web development framework
* [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) - marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.
* [SQLAlchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* [Poetry](https://python-poetry.org/) - Poetry is a tool for dependency management and packaging in Python.

## Authors

* **RaediConda**
