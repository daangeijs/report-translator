# Use the official NVIDIA CUDA runtime image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables to force GPU usage
ENV CUDA_VISIBLE_DEVICES=0

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    openssh-client \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Run the Python script during the build process to download the model
RUN python3 download_model.py

# Run the application with typer
ENTRYPOINT ["python3", "translate.py"]

# By default, show help when no arguments are passed
CMD ["--help"]