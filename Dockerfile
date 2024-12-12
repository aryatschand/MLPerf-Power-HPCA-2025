# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies, including Microsoft core fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app

# Make the run_all.sh script executable
RUN chmod +x ./run_all.sh

# Set the default command to run the script
CMD ["./run_all.sh"]
