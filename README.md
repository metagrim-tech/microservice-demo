# Microservice Demo Application

## Platform Pre-requisites

- [python 3.10](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation/)
- [Redis](https://redis.io/docs/getting-started/installation/)

In addition to these pre-requisites, the following items are recommended:

- Basic understanding of Python
- Basic understanding of Python virtual environments
- Basic understanding of Redis
- Basic understanding of FastAPI
- Basic understanding of Celery and Flower
- Basic understanding of SqlAlchemy and PostgreSQL

## Framework and references
- Micro-Service based REST API Framework [FastAPI](https://fastapi.tiangolo.com)
- The code base uses some DDD design patterns documented in the [Cosmic Python](https://www.cosmicpython.com/book/preface.html)

## Installation
   You can set up the development environment either by using docker or without docker.
1) Clone the repository to the machine:
   ```shell
   git clone https://github.com/metagrim-tech/microservice-demo.git
   cd microservice-demo/services/auth-service
   git checkout develop
   git pull origin
   ```
   ---

2) Setup Development Environment (Without Docker)
   To set up development environment execute the following commands in [backend/] directory
   1. Create Virtual Environment
      ```shell
      cd microservice-demo/services/auth-service
      # Install all (dev) dependencies
      pipenv install --dev
      # Activate pre-commit hooks
      pipenv shell
      pre-commit install
      ```
   2. Crete `.env`
      ```shell
      cd microservice-demo/services/auth-service
      cp env.sample .env
      ```
   3. Create the required database
      ```shell
      cd microservice-demo/services/auth-service
      cp env.sample .env
      # update the database details and redis connection details in .env file
      pipenv shell
      alembic upgrade heads
      ```
   4. Start API service
      ```shell
      pipenv shell
      python auth_service
      ```
      - On local runs on port `8064`
      - Before starting the service make sure that redis is up and running
      - API Specification can be seen at url [http://127.0.0.1:8064/docs](http://127.0.0.1:8064/docs)
      - Username/password admin@demo.com/admin@123

3) Setting up the development environment (With Docker)
   To run the Service in docker containers  execute the following command in [backend/] directory
   ```shell
   cd microservice-demo
   make run
   ```
   This will start the all the required services including Redis and PostgresSQL Server in the docker contaienr
It uses the .env_docker environment file to populate the docker container environments
   - On Docker port is bound with port `8064`
   - API Specification can be seen at url [http://127.0.0.1:8064/docs](http://127.0.0.1:8064/docs)
   - Username/password admin@demo.com/admin@123
