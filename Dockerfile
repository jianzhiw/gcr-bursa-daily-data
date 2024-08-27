# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True


# Define Proxy
ENV http_proxy=deb.debian.org
ENV https_proxy=deb.debian.org/debian

# Copy local code to the container image.
ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME
COPY . ./

# Install Ghostscript
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y ghostscript ffmpeg libsm6 libxext6 libgl1

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app