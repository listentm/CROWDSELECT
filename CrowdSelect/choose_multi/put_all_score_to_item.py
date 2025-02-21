import json

import os
base_path=os.getenv("CROWDSELECT_PATH")
difficulty_score_path = os.path.join(base_path,"data/difficult_score.json")
stability_score_path = os.path.join(base_path,"data/stability_score.json")
separability_score_path = os.path.join(base_path,"data/separability_score.json")
best_answer_path = os.path.join(base_path,"data/best_answer.json")
output_path = os.path.join(base_path,"data/all_score.json")


difficulty_score_path = r"\data\choose_period\difficulty\difficult_score.json"
novelty_score_path = r"\data\choose_period\novelty\novelty_score.json"
separability_score_path = r"\data\choose_period\separability\separability_score.json"
best_answer_path = r"\data\best_answer.json"
output_path = r"\data\multi_period\all_score.json"


with open(best_answer_path, 'r') as file:
    best_answer = json.load(file)

with open(difficulty_score_path, 'r') as file:
    difficulty_score = json.load(file)
    

with open(stability_score_path, 'r') as file:
    stability_score = json.load(file)

with open(novelty_score_path, 'r') as file:
    novelty_score = json.load(file)

    
with open(separability_score_path, 'r') as file:
    separability_score = json.load(file)
    
uuid_list = [item['uuid'] for item in best_answer]
uuid_to_difficulty_score = {item['uuid']: item['difficulty_score'] for item in difficulty_score}

uuid_to_stability_score = {item['uuid']: item['stability_score'] for item in stability_score}

uuid_to_novelty_score = {item['uuid']: item['novelty_score'] for item in novelty_score}

uuid_to_separability_score = {item['uuid']: item['separability_score'] for item in separability_score}

all_score_list = []
for uuid in uuid_list:
    result = {}
    result['uuid'] = uuid
    result['difficulty_score'] = uuid_to_difficulty_score[uuid]

    result['stability_score'] = uuid_to_stability_score[uuid]

    result['novelty_score'] = uuid_to_novelty_score[uuid]

    result['separability_score'] = uuid_to_separability_score[uuid]
    all_score_list.append(result)
    
with open(output_path, 'w') as file:
    json.dump(all_score_list, file, indent=4)