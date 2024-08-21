from gpt4all import GPT4All

# Initialize the model, to trigger the download. Only used during Docker build.
model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", model_path='.')
