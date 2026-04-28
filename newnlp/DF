# Use Python 3.10 image as base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update pip and install necessary dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with retries in case of download failure
RUN pip install --upgrade pip && \
    pip install --retries 5 --extra-index-url https://pypi.org/simple/ -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "app.py"]
