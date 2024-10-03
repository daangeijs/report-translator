# GPT4All Report Translator

This script translates reports from a specified input language to English using the GPT4All framework and the `"Meta-Llama-3-8B-Instruct.Q4_0.gguf"` model. The input and output are JSON files, and the model can run on different devices.

## Usage

### Arguments

- **`input_file`**: Path to the input JSON file containing reports.
- **`output_file`**: Path to the output JSON file where translated reports will be saved.
- **`device`**: The processing unit for running the GPT4All model. Options include:
  - `"cpu"`: Use the CPU.
  - `"gpu"`: Use Metal on ARM64 macOS, otherwise the same as "kompute".
  - `"kompute"`: Use the best GPU provided by the Kompute backend.
  - `"cuda"`: Use the best GPU provided by the CUDA backend (default).
  - `"amd"`: Use the best GPU provided by the Kompute backend from AMD.
  - `"nvidia"`: Use the best GPU provided by the Kompute backend from NVIDIA.
- **`input_language`**: The language of the input reports. Default is `"dutch"`.
- **`custom_prompt`**: Optional. If provided, this prompt will completely override the default prompt used for translation. The input language does not need to be specified in this case.

### Building the Docker Image

To build the Docker image and tag it as `translator:latest`, run the following command:

```bash
docker build -t translator:latest .
```

### Running the Docker Container

#### Basic Usage

```bash
docker run --rm --gpus all -v /path/to/local/input:/input -v /path/to/local/output:/output translator:latest --input-file /input/input.json --output-file /output/output.json

```

This command will translate the reports in the specified JSON file using the CUDA backend, assuming the reports are in Dutch, and save the results to the output file. Adjust the --device and --input-language arguments as needed.

#### Advanced Usage

```bash
docker run --rm --gpus all -v /path/to/local/input:/input -v /path/to/local/output:/output translator:latest --input-file /input/input.json --output-file /output/output.json --device cuda --input-language dutch --custom-prompt "Make a haiku from this report in English:"

```

This command will translate the reports in the specified JSON file using the CUDA backend, assuming the reports are in Dutch, and save the results to the output file. You can specify a custom_prompt to override the default translation prompt, such as shown above. Adjust the --device, --input-language, and --custom-prompt arguments as needed.


### ARM (macOS M1/M2/M3) Users

For users with ARM-based Macs (M1, M2, etc.), I’m aware that the Docker image might not work smoothly with Metal. Therefore, I recommend running the script locally using Conda. Don't forget to use the `--device=gpu` argument to leverage the Metal backend.

#### Steps to Install Locally:

1. **Install Conda** (e.g., Miniconda or Anaconda).
2. **Create the Environment**:
   ```bash
   conda env create -f environment.yml
    ```

3. **Activate the Environment**:
    ```bash
    conda activate translator
    ```

4. **Run the Script**:
    ```bash
    python translator/translate.py  /path/to/input.json /path/to/output.json --device=gpu 
    ```

### Running the scripts with SLURM
Here an example on how to load this script on a SLURM cluster using a sbatch script:

```bash
#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=4:00:00
#SBATCH --container-mounts=/your_input_path:/input,/your_output_path:/output
#SBATCH --container-image="your_registery#translate:latest"

# Run the Python script with arguments
python translator/translate.py /input/demo_input.json /output/output.json
```