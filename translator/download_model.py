from gpt4all import GPT4All

# Initialize the model, to trigger the download. Only used during Docker build.
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", model_path='.')
