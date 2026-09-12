FROM python:3.13-slim

# Prevent Python from writing bytecode (.pyc) and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy dependency requirements file first to utilize Docker layer caching
COPY requirements.txt /app/

# Upgrade pip and install all Python requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files (including db.sqlite3, media/, static/, etc.)
COPY . /app/

# Expose port 8000 to allow traffic
EXPOSE 8000

# Start the Django server on all container network interfaces (0.0.0.0)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]