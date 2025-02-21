import json
from transformers import AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

# Define paths and parameters
base_path=os.getenv("CROWDSELECT_PATH")
data_path = os.path.join(base_path,"magpie_100k")
model_path = os.path.join(base_path,"opensource_models/llama-3.2-3B-Instruct")
output_file = os.path.join(base_path,"data/length_1k_bottom.json")

# Load the dataset
ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo", cache_dir=data_path)

# Initialize AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Extract all instructions and their token lengths
instructions = []
for idx, item in enumerate(tqdm(ds["train"], desc="Processing instructions")):
    instruction = item["instruction"]
    token_length = len(tokenizer.tokenize(instruction))
    instructions.append({"index": idx, "instruction": instruction, "token_length": token_length})

# Sort by token length and take the top 1000 shortest instructions
instructions = sorted(instructions, key=lambda x: x["token_length"])
bottom_1000_instructions = instructions[:1000]

# Find the shortest response for each instruction
result = []
model_keys = [
    "gemma-2-2b-it", "gemma-2-9b-it", "gemma-2-27b-it", "Meta-Llama-3-8B-Instruct", "Meta-Llama-3-70B-Instruct",
    "Meta-Llama-3.1-8B-Instruct", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct",
    "Phi-3-mini-128k-instruct", "Phi-3-small-128k-instruct", "Phi-3-medium-128k-instruct",
    "Qwen2-1.5B-Instruct", "Qwen2-7B-Instruct", "Qwen2-72B-Instruct", "Qwen2.5-3B-Instruct",
    "Qwen2.5-7B-Instruct", "Qwen2.5-14B-Instruct", "Qwen2.5-32B-Instruct", "Qwen2.5-72B-Instruct"
]

for item in tqdm(bottom_1000_instructions, desc="Processing bottom 1000 instructions"):
    idx = item["index"]
    instruction = item["instruction"]

    shortest_response = {"model": None, "content": "", "token_length": float('inf')}
    for model_key in model_keys:
        response_content = ds["train"][idx][model_key]["content"] if model_key in ds["train"][idx] else ""
        response_length = len(tokenizer.tokenize(response_content))
        if response_length < shortest_response["token_length"] and response_length > 0:
            shortest_response = {"model": model_key, "content": response_content, "token_length": response_length}

    result.append({
        "instruction": instruction,
        "response": shortest_response["content"]
    })

# Save the results to a JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"The top 1000 shortest instructions and their shortest responses have been saved to {output_file}")