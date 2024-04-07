# Use a Python 3.9 image as the base
FROM python:3.9-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r /app/requirements.txt
