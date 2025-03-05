FROM python:3.12-slim-bookworm AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYSETUP_PATH="/opt/code" \
    VENV_PATH="/opt/code/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS development
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential
ENV POETRY_VERSION=1.8.4
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./
RUN poetry install
RUN ln -sf /bin/bash /bin/sh

# The rest of the configuration is specified in the compose.yml file
# EXPOSE 8000
# ENTRYPOINT ["fastapi", "dev", "/opt/code/app/entrypoint/rest_api/main.py"]
# CMD ["--host", "0.0.0.0"]
