import json
import random
import os

base_path=os.getenv("CROWDSELECT_PATH")

best_answer_path = os.path.join(base_path,"data/best_answer.json")
base_path = os.path.join(base_path,"data")

data_size = 1000

with open(best_answer_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
random_seeds = [1,2,3,4,5,6]

for i, seed in enumerate(random_seeds):
    random.seed(seed)
    sample = random.sample(data, data_size)
    file_name = f"random_1k_seed_{seed}.json"
    file_path = os.path.join(base_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, ensure_ascii=False, indent=4)