# Use the official Python 3.10 image from Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY flask_app/requirements.txt /app/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY flask_app/ /app/

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3500", "app:app"]
