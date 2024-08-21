# Use the official NVIDIA CUDA runtime image with cuDNN 8
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install Miniconda
RUN apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    /opt/conda/bin/conda init bash

# Set up the environment
ENV PATH=/opt/conda/bin:$PATH

WORKDIR /usr/src/app
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate the conda environment by default
RUN echo "source activate translator" > ~/.bashrc
ENV CONDA_DEFAULT_ENV=translator
ENV PATH /opt/conda/envs/translator/bin:$PATH

# Copy the application code
COPY . .

# Set the environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Download the model within the Conda environment
RUN conda run --no-capture-output -n translator python translator/download_model.py

# Set the entry point to use the conda environment and run the script
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "translator", "python", "translator/translate.py"]

# Default command, can be overridden
CMD ["--help"]