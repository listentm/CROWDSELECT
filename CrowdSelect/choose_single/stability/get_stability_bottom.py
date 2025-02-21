import json
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
<<<<<<< HEAD
import os

base_path=os.getenv("CROWDSELECT_PATH")
magpie_path = os.path.join(base_path,"magpie_100k")
# Step 1: Read the data.json file
with open('skywork_llama_stability_score.json', 'r') as f:
=======

# Step 1: Read the data.json file
with open('skywork_gemma_stability_score.json', 'r') as f:
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
    data = json.load(f)

# Step 2: Convert to DataFrame and sort by stability, then select the smallest top 1k entries
df = pd.DataFrame(data)
bottom_1k_df = df.sort_values(by='stability', ascending=True).head(1000)

# Step 3: Load the dataset
ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo",
<<<<<<< HEAD
                  cache_dir=magpie_path)['train']
=======
                  cache_dir='../../magpie_100k')['train']
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

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
bottom_1k_output = []

# Step 4: Iterate through the bottom 1k data and select the model with the highest score
for _, row in tqdm(bottom_1k_df.iterrows(), total=bottom_1k_df.shape, desc="Processing Bottom 1k Data"):
    # Find the model with the highest score
    top_model = max(model_columns, key=lambda col: row[col])

    # Get basic information
    uuid = row['uuid']
    instruction = row['instruction']

    # Find the response content for the corresponding `uuid` and `top_model` in the dataset
    matched_row = next((item for item in ds if item['uuid'] == uuid), None)
    response = matched_row[top_model]['content']

    # Add to the results
    bottom_1k_output.append({
        'uuid': uuid,
        'instruction': instruction,
        'response': response
    })

<<<<<<< HEAD
output_file=os.path.join(base_path,'data/skywork_llama_stability_1k_bottom.json')
# Step 5: Save the results to a JSON file
with open(output_file, 'w') as f:
    json.dump(bottom_1k_output, f, indent=4)

print("Bottom 1k stability data saved to 'skywork_llama_stability_1k_bottom.json'")
=======
# Step 5: Save the results to a JSON file
with open('skywork_gemma_stability_1k_bottom.json', 'w') as f:
    json.dump(bottom_1k_output, f, indent=4)

print("Bottom 1k stability data saved to 'skywork_gemma_stability_1k_bottom.json'")
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
