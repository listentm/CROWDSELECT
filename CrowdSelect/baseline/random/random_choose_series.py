import json
import random
import os

base_path=os.getenv("CROWDSELECT_PATH")
# Path to the best_answer.json file
best_answer_path = os.path.join(base_path,"data/best_answer.json")
# Base path to save the randomly sampled files
base_path = os.path.join(base_path,"data/choose_period/random_series/")

# List of sample sizes to be extracted
sample_sizes = [100, 250, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# Set the size of each sample
sample_size = 1000
# Set the number of samples to extract
num_samples = 8

# Read the best_answer.json file
with open(best_answer_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create the base directory if it does not exist
if not os.path.exists(base_path):
    os.makedirs(base_path)

# Ensure the data size is sufficient for the required number of samples
assert len(data) >= sample_size * num_samples, "Insufficient data to extract the required number of samples"

# Randomly extract the specified number of elements and save them to new JSON files
for i in range(1, num_samples + 1):
    sample = random.sample(data, sample_size)
    file_name = f"random_1k_series_{i}.json"
    file_path = os.path.join(base_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, ensure_ascii=False, indent=4)