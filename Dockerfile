# Use the official Python 3.9 image as the base image
FROM python:3.9

# Set environment variables to ensure a clean Python environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the requirements file to leverage Docker caching
COPY requirements.txt /usr/src/app

# Install dependencies specified in the requirements file
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port on which the Django app will run (defined in docker-compose.yml)
# Note: This line is not necessary if the port is defined in docker-compose.yml
EXPOSE 8010

# Command to run the Django app when the container starts
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8010" ]