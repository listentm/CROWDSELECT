import json

<<<<<<< HEAD
difficulty_score_path = os.path.join(base_path,'data/difficult_score.json')
answer_path = os.path.join(base_path,'data/best_answer.json')
base_path = os.path.join(base_path,'data/difficulty_series')
=======
difficulty_score_path = r'difficult_score.json'
answer_path = r'best_answer.json'
base_path = r'difficulty_series'
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
difficulty_bottom_100 = base_path + r'\difficulty_bottom_0.1k.json' 
difficulty_bottom_250 = base_path + r'\difficulty_bottom_0.25k.json'
difficulty_bottom_500 = base_path + r'\difficulty_bottom_0.5k.json'
difficulty_bottom_1000 = base_path + r'\difficulty_bottom_1k.json'
difficulty_bottom_2000 = base_path + r'\difficulty_bottom_2k.json'
difficulty_bottom_3000 = base_path + r'\difficulty_bottom_3k.json'
difficulty_bottom_4000 = base_path + r'\difficulty_bottom_4k.json'
difficulty_bottom_5000 = base_path + r'\difficulty_bottom_5k.json'
difficulty_bottom_6000 = base_path + r'\difficulty_bottom_6k.json'
difficulty_bottom_7000 = base_path + r'\difficulty_bottom_7k.json'
difficulty_bottom_8000 = base_path + r'\difficulty_bottom_8k.json'
difficulty_bottom_9000 = base_path + r'\difficulty_bottom_9k.json'
difficulty_bottom_10000 = base_path + r'\difficulty_bottom_10k.json'

with open(answer_path, 'r') as f:
    answer_data = json.load(f)
    
uuid_to_item = {item['uuid']: item for item in answer_data}

with open(difficulty_score_path, 'r') as f:
    difficulty_data = json.load(f)
    
sorted_difficulty_data = sorted(difficulty_data, key=lambda x: x['difficulty_score'])
sorted_uuids = [item['uuid'] for item in sorted_difficulty_data]

bottom_100_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:100]]
bottom_250_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:250]]
bottom_500_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:500]]
bottom_1000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:1000]]
bottom_2000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:2000]]
bottom_3000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:3000]]
bottom_4000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:4000]]
bottom_5000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:5000]]
bottom_6000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:6000]]
bottom_7000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:7000]]
bottom_8000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:8000]]
bottom_9000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:9000]]
bottom_10000_items = [uuid_to_item[uuid] for uuid in sorted_uuids[:10000]]

with open(difficulty_bottom_100, 'w') as f:
    json.dump(bottom_100_items, f)
    
with open(difficulty_bottom_250, 'w') as f:
    json.dump(bottom_250_items, f)
    
with open(difficulty_bottom_500, 'w') as f:
    json.dump(bottom_500_items, f)
    
with open(difficulty_bottom_1000, 'w') as f:
    json.dump(bottom_1000_items, f)
    
with open(difficulty_bottom_2000, 'w') as f:
    json.dump(bottom_2000_items, f)
    
with open(difficulty_bottom_3000, 'w') as f:
    json.dump(bottom_3000_items, f)
    
with open(difficulty_bottom_4000, 'w') as f:
    json.dump(bottom_4000_items, f)
    
with open(difficulty_bottom_5000, 'w') as f:
    json.dump(bottom_5000_items, f)
    
with open(difficulty_bottom_6000, 'w') as f:
    json.dump(bottom_6000_items, f)
    
with open(difficulty_bottom_7000, 'w') as f:
    json.dump(bottom_7000_items, f)
    
with open(difficulty_bottom_8000, 'w') as f:
    json.dump(bottom_8000_items, f)
    
with open(difficulty_bottom_9000, 'w') as f:
    json.dump(bottom_9000_items, f)
    
with open(difficulty_bottom_10000, 'w') as f:
    json.dump(bottom_10000_items, f)