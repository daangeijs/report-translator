# GPT4All Report Translator

This script translates reports from a specified input language to English using the GPT4All framework and the `Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf` model. The input and output are JSON files, and the model can run on different devices.

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

