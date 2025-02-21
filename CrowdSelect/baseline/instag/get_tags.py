# File 1: generate_tags.py
import json
import time
from multiprocessing import Pool
import openai
import uuid
from tqdm import tqdm  # Import progress bar library

# Set up DeepSeek API
openai.api_key = "your key"
openai.api_base = "https://api.deepseek.com/v1"

# Use the full range of labels based on reference images
labels = [
    "information", "request", "data", "research", "analysis", "retrieval", "inquiry", "writing", "creative", "program", "loop", "mathematics", "solve", "coding", "problem", "operation", "creation", "generation", "development", "handling", "declaration", "comparison", "arithmetic", "statement", "reasoning", "extraction", "roleplay", "humanities", "STEM"
]

# Call DeepSeek API to get real tags
def get_tags_with_deepseek(item):
    instruction = item["instruction"]
    messages = [
        {"role": "system", "content": "You are a tag generator. Classify the instruction into relevant tags from this list: " + ", ".join(labels)},
        {"role": "user", "content": instruction}
    ]
    output = "API_ERROR_OUTPUT"
    for _ in range(3):  # Retry mechanism
        try:
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=messages,
                n=1,
                temperature=0,
                max_tokens=50,
            )
            output = response["choices"]["message"]["content"]
            break
        except openai.error.OpenAIError as e:
            print(f"API error: {e}. Retrying...")
            time.sleep(2)
    return {"uuid": str(uuid.uuid4()), "instruction": instruction, "tags": output.strip().split(", ")}

# Process data in parallel and display a progress bar
def process_data_parallel(data):
    results = []
    with Pool(processes=32) as pool:  # Use 4 processes in parallel
        for result in tqdm(pool.imap(get_tags_with_deepseek, data), total=len(data), desc="Processing"):
            results.append(result)
    return results

if __name__ == "__main__":
    base_path = os.getenv("CROWDSELECT_PATH")
    input_file_path = os.path.join(base_path,"data/full_data.json")
    output_file_path = os.path.join(base_path,"data/tags_info.json")

    # Load data
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Get tag information
    tagged_data = process_data_parallel(data)

    # Save results
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(tagged_data, output_file, ensure_ascii=False, indent=4)

    print(f"Tagged data saved to {output_file_path}")