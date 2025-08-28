FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system dependencies and uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends bash && \
    pip install --no-cache-dir uv

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv pip compile pyproject.toml -o /tmp/requirements.txt && \
    uv pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Copy project
COPY . .

# Set up static files
ENV STATIC_ROOT=/app/staticfiles
RUN mkdir -p $STATIC_ROOT && \
    chmod -R 755 $STATIC_ROOT

# Create media directory
RUN mkdir -p /app/media && \
    chmod -R 755 /app/media

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "EasyRent.wsgi:application"]
