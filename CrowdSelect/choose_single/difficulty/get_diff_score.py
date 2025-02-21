import json
from tqdm import tqdm
import numpy as np
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import euclidean_distances
<<<<<<< HEAD
import os
base_path=os.getenv("CROWDSELECT_PATH")
data_path = os.path.join(base_path,'data/skywork_llama_score.json')
difficult_path = os.path.join(base_path,'data/difficulty_score.json')
=======

data_path = '../../data/skywork_llama_score.json'
difficult_path = r'difficulty_score.json'
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

with open(data_path, 'r') as f:
    data = json.load(f)

result_list = []

#difficulty_score
for item in tqdm(data, desc="Processing items"):
    result = {}
    result['uuid'] = item['uuid']
    result['instruction'] = item['instruction']
    scores = [value for key, value in item.items() if key not in ['uuid', 'instruction']]
    difficulty_score = sum(scores) / len(scores)
    result['difficulty_score'] = -difficulty_score
    result_list.append(result)
    
with open(difficult_path, 'w') as f:
    json.dump(result_list, f)
