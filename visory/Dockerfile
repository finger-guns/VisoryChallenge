# Base image
FROM python AS base

ENV PORT=8000
EXPOSE ${PORT}

# Set working directory
WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install poetry

# Copy project files
COPY ./api /app/api

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Provide default arguments, including the PORT environment variable
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
