# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install necessary libraries for GPU support
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV HF_TOKEN=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
ENV MODEL_NAME=meta-llama/Meta-Llama-3-8B-Instruct
ENV MAX_TOKENS=128
ENV TEMPERATURE=0.7

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the app
CMD ["python", "app.py"]
