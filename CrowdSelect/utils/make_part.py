import json
import random

# 设置随机种子以确保结果可重现
random.seed(43)

answer_path = r"E:\rewgen\ylf\RewGen\data\cluster_choose\10\difficulty_1k_bottom_10_clusters.json"
temp_path = r"E:\rewgen\ylf\RewGen\data\temp\6-10.json"

# 读取answer数据
with open(answer_path, 'r', encoding='utf-8') as f: 
    answer = json.load(f)

# 随机选择5个数据
items = random.sample(answer, 5)

# 保存选中的数据
with open(temp_path, 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print(f"已随机选择 {len(items)} 个数据并保存到 {temp_path}")
