from datasets import load_dataset
import json
from tqdm import tqdm
<<<<<<< HEAD
import os
base_path=os.getenv("CROWDSELECT_PATH")
data_path = os.path.join(base_path,"magpie_100k")

ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo", cache_dir=data_path)
output_path = os.path.join(base_path,"data/best_answer.json")
=======

ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo", cache_dir='../magpie_100k')
output_path = "../data/best_answer.json"
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
train_dataset = ds['train']

def choose_best_response(data):
    for item in data:
        best_model = max(item.keys(), key=lambda k: item[k]['Skywork-Reward-Llama-3.1-8B'] if isinstance(item[k], dict) and 'Skywork-Reward-Llama-3.1-8B' in item[k] else float('-inf'))
        item['response'] = item[best_model]['content']

result_list =[]
   
for item in tqdm(train_dataset, desc="Processing items"):
    result = {}
    
    result['uuid'] = item['uuid']
    result['instruction'] = item['instruction']
    best_model = max(item.keys(), key=lambda k: item[k]['Skywork-Reward-Llama-3.1-8B'] if isinstance(item[k], dict) and 'Skywork-Reward-Llama-3.1-8B' in item[k] else float('-inf'))
    result['response'] = item[best_model]['content']
    
    result_list.append(result)
    
with open(output_path, 'w') as f:
    json.dump(result_list, f)