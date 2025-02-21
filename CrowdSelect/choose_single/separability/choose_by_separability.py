import json
from tqdm import tqdm
<<<<<<< HEAD
import os
base_path=os.getenv("CROWDSELECT_PATH")
score_path = os.path.join(base_path,'data/separability_score.json')
answer_path = os.path.join(base_path,'data/best_answer.json')
top_1k_path = os.path.join(base_path,'data/skywork_llama_separability_top_1k.json')
bottom_1k_path = os.path.join(base_path,'data/skywork_llama_separability_bottom_1k.json')
=======

score_path = '../../data/separability_score.json'
answer_path = '../../data/best_answer.json'
top_1k_path = '../../data/skywork_llama_separability_top_1k.json'
bottom_1k_path = '../../data/skywork_llama_separability_bottom_1k.json'
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

with open(score_path, 'r') as f:
    score_data = json.load(f)
    
with open(answer_path, 'r') as f:
    answer_data = json.load(f)

sorted_data = sorted(score_data, key=lambda x: x['separability_score'])
print("Sorted successfully!")
# print(sorted_data[0]['separability_score'])
# print(sorted_data[1]['separability_score'])
# print(sorted_data[2]['separability_score'])
# print(sorted_data[3]['separability_score'])
lowest_1000 = sorted_data[:1000]
highest_1000 = sorted_data[-1000:]


# get uuid
lowest_1000_uuids = [item['uuid'] for item in lowest_1000]
highest_1000_uuids = [item['uuid'] for item in highest_1000]

top_1k = []
bottom_1k = []

for item in tqdm(answer_data, desc="Processing items"):
    if item['uuid'] in highest_1000_uuids:
        top_1k.append(item)
    if item['uuid'] in lowest_1000_uuids:
        bottom_1k.append(item)

with open(top_1k_path, 'w') as f:
    json.dump(top_1k, f)
with open(bottom_1k_path, 'w') as f:
    json.dump(bottom_1k, f)


