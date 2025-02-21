import json
from tqdm import tqdm
import numpy as np
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import euclidean_distances
import os
base_path=os.getenv("CROWDSELECT_PATH")
#coverage
uuid_split_path = os.path.join(base_path,'data/uuids_split.json')
embedding_path = os.path.join(base_path,'data/instruction_embedding.json')
output_path = os.path.join(base_path,'data/coverage_score.json')
    
def get_the_entities(text_list, batch_size=16):
    """
    Get the entities from the text using batch processing.
    """
    device = 0 if torch.cuda.is_available() else -1
    ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", device=device)
    entities = set()

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        ner_results = ner_model(batch)
        for ner_result in ner_results:
            for item in ner_result:
                word = item['word'].replace("##", "")
                entities.add(word)

    return entities

src_data_path = os.path.join(base_path,'data/truthful_QA.json')
best_answer_path = os.path.join(base_path,'data/best_answer.json')
uuid_split_path = os.path.join(base_path,'data/uuids_split.json')
output_path = os.path.join(base_path,'data/choose_period/fidelity/fidelity_score.json')

with open(src_data_path, 'r') as f:
    src_data = json.load(f)

with open(best_answer_path, 'r') as f:
    best_answer_data = json.load(f)
    
with open(uuid_split_path, 'r') as f:
    uuid_split = json.load(f)

src_text = []

for item in src_data:
    src_text.append(item['input'])
    src_text.append(item['output'])

src_entities = get_the_entities(src_text)

uuid_to_item = {item['uuid']: item for item in best_answer_data}

result_list = []
i = 0

for sublist in tqdm(uuid_split, desc="Processing UUID split"):
    gen_text = []
    
    for uuid in sublist:
        item = uuid_to_item[uuid]
        gen_text.append(item['instruction'])
        gen_text.append(item['response'])
        
    gen_entities = get_the_entities(gen_text)
    shared_entities = set(src_entities) & set(gen_entities)
    
    fidelity_score = len(shared_entities) / len(set(gen_entities))
    result_list.append(
        {
            "split_id": i,
            "fidelity_score": fidelity_score
        }
    )
    i += 1
    
with open(output_path, 'w') as f:
    json.dump(result_list, f)