FROM --platform=linux/amd64 python:3.10.7-slim-bullseye as build


# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
# Setup variables for the non-root user/group settings so that the container can be run with a
# not-root user
ENV NON_ROOT_GROUP nrgroup
ENV NON_ROOT_USER nruser
ENV NON_ROOT_GROUP_ID 2000
# Setup a non-root user by creating a group and assigning permissions to the user and group on the
# newly created users home directory
RUN addgroup --system --gid ${NON_ROOT_GROUP_ID} ${NON_ROOT_GROUP} \
    && adduser --system --ingroup ${NON_ROOT_GROUP} --home /home/${NON_ROOT_USER} \
    --shell /usr/sbin/nologin --uid ${NON_ROOT_GROUP_ID} ${NON_ROOT_USER} \
    && chown --recursive ${NON_ROOT_USER}:${NON_ROOT_GROUP} /home/${NON_ROOT_USER}

# Ensure all the relevant requirements are added
RUN apt-get update -y && apt-get install -y netcat

WORKDIR /app
ADD ./services/auth-service/Pipfile /app

RUN pip install pipenv
RUN cd /app && pipenv lock && pipenv install --system --deploy
RUN chown ${NON_ROOT_USER}:${NON_ROOT_GROUP} /app/

# Deploy code
FROM build as deploy
USER ${NON_ROOT_USER}
ENV PYTHONPATH=/app:/app/src
# This script will automatically run when the container starts ensuring the database
# is up and migrations run prior to starting the fastapi service.
COPY ./services/auth-service/entrypoint.sh entrypoint.sh
COPY ./services/auth-service/.env_docker ./services/auth-service/alembic.ini ./services/auth-service/db_init.py ./services/auth-service/pyproject.toml ./services/auth-service/README.md /app/
COPY ./services/auth-service/src /app/src/
COPY ./services/auth-service/scripts /app/scripts/
COPY ./services/auth-service/migrations /app/migrations/
COPY ./services/auth-service/tests /app/tests/
EXPOSE 8064
