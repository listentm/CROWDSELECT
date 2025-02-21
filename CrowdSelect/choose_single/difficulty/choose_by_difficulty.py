import json
from tqdm import tqdm
<<<<<<< HEAD
import os
# Define file paths
base_path=os.getenv("CROWDSELECT_PATH")
score_path = os.path.join(base_path,'data/difficulty_score.json')
answer_path = os.path.join(base_path,'/data/best_answer.json')
top_1k_path = os.path.join(base_path,'data/skywork_llama_difficulty_top_1k.json')
bottom_1k_path = os.path.join(base_path,'data/skywork_llama_difficulty_bottom_1k.json')
=======

# Define file paths
score_path = 'difficulty_score.json'
answer_path = '../../data/best_answer.json'
top_1k_path = 'skywork_llama_difficulty_top_1k.json'
bottom_1k_path = 'skywork_llama_difficulty_bottom_1k.json'
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

# Load difficulty score data
with open(score_path, 'r') as f:
    score_data = json.load(f)

# Load best answer data
with open(answer_path, 'r') as f:
    answer_data = json.load(f)

# Sort the data by difficulty_score (higher score means higher difficulty, so higher scores appear later in the sorted array)
sorted_data = sorted(score_data, key=lambda x: x['difficulty_score'])
print("Sorted successfully!")

# Extract the lowest 1000 and highest 1000 items
lowest_1000 = sorted_data[:1000]
highest_1000 = sorted_data[-1000:]

# Get the UUIDs of these items
lowest_1000_uuids = [item['uuid'] for item in lowest_1000]
highest_1000_uuids = [item['uuid'] for item in highest_1000]

# Initialize lists to store the top 1k and bottom 1k items
top_1k = []
bottom_1k = []

# Filter the best answer data based on the extracted UUIDs
for item in tqdm(answer_data, desc="Processing items"):
    if item['uuid'] in highest_1000_uuids:
        top_1k.append(item)
    if item['uuid'] in lowest_1000_uuids:
        bottom_1k.append(item)

# Save the top 1k items to a JSON file
with open(top_1k_path, 'w') as f:
    json.dump(top_1k, f)

# Save the bottom 1k items to a JSON file
with open(bottom_1k_path, 'w') as f:
    json.dump(bottom_1k, f)