from gpt4all import GPT4All
import typer
import json
from typing import Dict, Any
from tqdm import tqdm

def generate_translation(prompt: str, model: GPT4All) -> str:
    """
    Generates a translation to English using GPT4All.

    Args:
        prompt (str): The prompt to be used for translation.
        model (GPT4All): The GPT4All model instance.

    Returns:
        str: The translated English text or "TRANSLATION FAILED" if an error occurs.
    """
    try:
        with model.chat_session():
            translation = model.generate(prompt, max_tokens=4096)
        return translation
    except Exception as e:
        print(f"Error translating report: {e}")
        return "TRANSLATION FAILED"

def main(input_file: str, output_file: str, device: str = "cuda", input_language: str = "dutch", custom_prompt: str = None) -> None:
    """
    Reads a JSON file with reports in a specified language, translates them to English,
    and writes the results to an output JSON file. Displays progress
    using a progress bar and skips entries that fail to translate.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file.
        device (str): The processing unit on which the GPT4All model will run.
                      Options are "cpu", "gpu", "kompute", "cuda", "amd", "nvidia".
        input_language (str): The language of the input reports. Default is "dutch".
        custom_prompt (str): Optional custom prompt to use instead of the default prompt.
    """
    print("Loading model...")
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", model_path='.', device=device)
    print(f"Model loaded with device: {device} using input language: {input_language}")
    
    # Construct the prompt
    prompt_base = custom_prompt if custom_prompt else f"Please translate this {input_language.capitalize()} pathology report to english without changing the context or medical diagnosis. Leave everything as it is, dont add notes:"
    
    # Show the user the base prompt that will be used
    print(f"Using prompt: {prompt_base}")
    
    # Read input JSON file
    with open(input_file, 'r') as f:
        data: Dict[str, Any] = json.load(f)
    
    # Process the JSON data with progress bar
    for key, value in tqdm(data.items(), desc="Translating reports", unit="report"):
        report = value[input_language.lower()]
        prompt = f"{prompt_base}\n\n{report}"
        english_translation = generate_translation(prompt, model)
        data[key]["english"] = english_translation
        
        # Write the updated entry to the output file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    typer.run(main)
