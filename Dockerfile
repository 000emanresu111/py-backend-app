FROM python:3.9

WORKDIR /code

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Configure poetry virtualenvs
RUN poetry config virtualenvs.in-project true

# Copy application files
COPY app /code/app
COPY README.md /code/README.md
COPY main.py /code/main.py
COPY playground.py /code/playground.py
COPY pyproject.toml /code/pyproject.toml
COPY poetry.lock /code/poetry.lock

# Install dependencies
RUN poetry install --only main

CMD ["poetry", "run", "uvicorn", "main:app", "--port", "8086", "--host", "0.0.0.0"]

EXPOSE 8086
