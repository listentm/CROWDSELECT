import json
from tqdm import tqdm
import numpy as np
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import euclidean_distances
import os
base_path=os.getenv("CROWDSELECT_PATH")
data_path = os.path.join(base_path,'data/skywork_llama_score.json')
best_answer_path = os.path.join(base_path,'data/best_answer.json')
separability_path = os.path.join(base_path,'data/separability_score.json')

with open(data_path, 'r') as f:
    data = json.load(f)


result_list = []

#separability
for item in tqdm(data, desc="Processing items"):
    result = {}
    result['uuid'] = item['uuid']
    result['instruction'] = item['instruction']
    scores = [value for key, value in item.items() if key not in ['uuid', 'instruction']]
    separability_score = np.var(scores)
    result['separability_score'] = separability_score
    result_list.append(result)
    
with open(separability_path, 'w') as f:
    json.dump(result_list, f)
