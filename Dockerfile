FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy dependency files first
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry to not use virtualenvs
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-root --only main

# Copy the rest of the project
COPY . .

# Run the app
CMD ["streamlit", "run", "src/sentiment_analysis/main.py", "--server.port=8080", "--server.address=0.0.0.0"]


