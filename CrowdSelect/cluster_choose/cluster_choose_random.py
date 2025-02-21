import json
import heapq
import random
import os

<<<<<<< HEAD
# Define base path and file paths
base_path = os.getenv("CROWDSELECT_PATH")
uuid_split_path = os.path.join(base_path, "data/uuid_split_30.json")
best_answer_path = os.path.join(base_path, "data/best_answer.json")
base_path = os.path.join(base_path, "data/random_30")

# Load best_answer data
with open(best_answer_path, 'r') as file:
    best_answer = json.load(file)

# Load uuid_split data
with open(uuid_split_path, 'r') as file:
    uuid_data = json.load(file)

# Create a mapping from UUID to item
uuid_to_item = {item['uuid']: item for item in best_answer}

# Check if uuid_data is in the expected format
if not isinstance(uuid_data, list) or len(uuid_data) != 30 or not all(
        isinstance(sublist, list) for sublist in uuid_data):
    raise ValueError("The format of uuid_split_path file is incorrect")


# Define a function to randomly sample UUIDs
def get_random_uuids(data, num_samples=50):
    return random.sample(data, num_samples)


# Define a list of seeds
seeds =

i = 1

# Process each seed
=======
uuid_split_path = r"E:\rewgen\ylf\RewGen\data\cluster_choose\30\uuid_split_30.json"
best_answer_path = r"E:\rewgen\ylf\RewGen\data\best_answer.json" 
base_path = r"E:\rewgen\ylf\RewGen\data\cluster_choose\30"

with open(best_answer_path, 'r') as file:
    best_answer = json.load(file)

with open(uuid_split_path, 'r') as file:
    uuid_data = json.load(file)

uuid_to_item = {item['uuid']: item for item in best_answer}

# 检查uuid_data是否符合预期
if not isinstance(uuid_data, list) or len(uuid_data) != 30 or not all(isinstance(sublist, list) for sublist in uuid_data):
    raise ValueError("uuid_split_path文件的格式不正确")

# 定义一个函数来随机抽取100条UUID
def get_random_uuids(data, num_samples=50):
    return random.sample(data, num_samples)

# 定义种子列表
seeds = [42]

i = 1

>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
for seed in seeds:
    random.seed(seed)
    selected_uuids = []
    for sublist in uuid_data:
        selected_uuids.extend(get_random_uuids(sublist))
<<<<<<< HEAD

    # Generate the output file path
    file_path = os.path.join(base_path, f"cluster_random_1k_seed_30_clusters_{seed}.json")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Generate the file content
=======
    
    # 生成文件名
    file_path = os.path.join(base_path, f"cluster_random_1k_seed_30_clusters_{seed}.json")
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # 生成文件内容
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
    items = [uuid_to_item[uuid] for uuid in selected_uuids]
    with open(file_path, 'w') as file:
        json.dump(items, file, indent=4)