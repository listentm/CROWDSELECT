from datasets import load_dataset
import json
import random
random_1k_path = r"E:\rewgen\ylf\RewGen\data\choose_period\random_series\random_1k_series_3.json"
output_path_1 = r"E:\rewgen\ylf\RewGen\data\other_answer\random_1k_random_answer.json"
output_path_2 = r"E:\rewgen\ylf\RewGen\data\other_answer\random_1k_top_5_answers.json"

# 加载数据集
dataset = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo", 
                 cache_dir=r"E:\rewgen\ylf\RewGen\magpie")

with open(random_1k_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
selected_uuids = [d['uuid'] for d in data]
train_data = dataset['train']
uuid_to_item = {item['uuid']: item for item in train_data}  
selected_items = [uuid_to_item[uuid] for uuid in selected_uuids]

model_names = [key for key in selected_items[0].keys() 
              if key not in ['uuid', 'instruction']]

# 第一个任务：随机选择response
random_selected = []
for item in selected_items:
    # 随机选择一个模型
    random_model = random.choice(model_names)
    selected_dict = {
        'uuid': item['uuid'],
        'instruction': item['instruction'],
        'response': item[random_model]['content']
    }
    random_selected.append(selected_dict)

# 写入第一个输出文件
with open(output_path_1, 'w', encoding='utf-8') as f:
    json.dump(random_selected, f, ensure_ascii=False, indent=2)

# 第二个任务：从分数最高的前五个中选择一个
top_5_selected = []
for item in selected_items:
    # 获取所有模型的分数
    scores = [(model_name, item[model_name]['Skywork-Reward-Llama-3.1-8B']) 
             for model_name in model_names]
    # 按分数排序并获取前5个
    top_5_models = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    # 从前5个中随机选择一个
    chosen_model = random.choice(top_5_models)[0]
    
    selected_dict = {
        'uuid': item['uuid'],
        'instruction': item['instruction'],
        'response': item[chosen_model]['content']
    }
    top_5_selected.append(selected_dict)

# 写入第二个输出文件
with open(output_path_2, 'w', encoding='utf-8') as f:
    json.dump(top_5_selected, f, ensure_ascii=False, indent=2)
