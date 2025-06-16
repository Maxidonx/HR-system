# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
# Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
# Copy the rest of the application's code into the container
COPY . /app/

# The command to run when the container starts
# We'll use a script for this in docker-compose for more flexibility,
# but you could also run the server directly here:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
