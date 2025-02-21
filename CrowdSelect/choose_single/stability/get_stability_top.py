import json
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset

# Step 1: Read the data.json file
with open('skywork_llama_stability_score.json', 'r') as f:
    data = json.load(f)

# Step 2: Convert to DataFrame and sort by stability, then select the top 1k entries
df = pd.DataFrame(data)
top_1k_df = df.sort_values(by='stability', ascending=False).head(1000)

# Step 3: Load the dataset
ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo",
                  cache_dir='../../magpie_100k')['train']

# Define all 19 model columns
model_columns = [
    'gemma-2-2b-it', 'gemma-2-9b-it', 'gemma-2-27b-it',
    'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3-70B-Instruct', 'Meta-Llama-3.1-8B-Instruct',
    'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-405B-Instruct',
    'Phi-3-mini-128k-instruct', 'Phi-3-small-128k-instruct', 'Phi-3-medium-128k-instruct',
    'Qwen2-1.5B-Instruct', 'Qwen2-7B-Instruct', 'Qwen2-72B-Instruct',
    'Qwen2.5-3B-Instruct', 'Qwen2.5-7B-Instruct', 'Qwen2.5-14B-Instruct',
    'Qwen2.5-32B-Instruct', 'Qwen2.5-72B-Instruct'
]

# Store the final results
top_1k_output = []

# Step 4: Iterate through the top 1k data and select the model with the highest score
for _, row in tqdm(top_1k_df.iterrows(), total=top_1k_df.shape, desc="Processing Top 1k Data"):
    # Find the model with the highest score
    top_model = max(model_columns, key=lambda col: row[col])

    # Get basic information
    uuid = row['uuid']
    instruction = row['instruction']

    # Find the response content for the corresponding `uuid` and `top_model` in the dataset
    matched_row = next((item for item in ds if item['uuid'] == uuid), None)
    response = matched_row[top_model]['content']

    # Add to the results
    top_1k_output.append({
        'uuid': uuid,
        'instruction': instruction,
        'response': response
    })

# Step 5: Save the results to a JSON file
with open('skywork_gemma_stability_1k_top.json', 'w') as f:
    json.dump(top_1k_output, f, indent=4)

print("Top 1k stability data saved to 'skywork_gemma_stability_1k_top.json'")