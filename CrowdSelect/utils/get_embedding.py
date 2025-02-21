from transformers import AutoModel, AutoTokenizer
import torch
import os
import json
from tqdm import tqdm

<<<<<<< HEAD
# Set proxy
os.environ['HTTP_PROXY'] = '127.0.0.1:7891'
os.environ['HTTPS_PROXY'] = '127.0.0.1:7891'

# Load model and tokenizer
model_name = "jinaai/jina-embeddings-v3"
model = AutoModel.from_pretrained(model_name, trust_remote_code=True, cache_dir=r'jinnai_embedding_v3')
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, cache_dir=r'jinnai_embedding_v3')

# Define file paths
base_path = os.getenv("CROWDSELECT_PATH")
answer_path = os.path.join(base_path, 'data/best_answer.json')
instruction_embedding_path = os.path.join(base_path, 'data/instruction_embedding.json')
answer_embedding_path = os.path.join(base_path, 'data/answer_embedding.json')

# Move model to GPU if available
=======
# 设置代理
os.environ['HTTP_PROXY'] = '127.0.0.1:7891'
os.environ['HTTPS_PROXY'] = '127.0.0.1:7891'

# 加载模型和分词器
model_name = "jinaai/jina-embeddings-v3"
model = AutoModel.from_pretrained(model_name, trust_remote_code=True, cache_dir=r'/mnt/liyisen/abandon/ylf/RewGen/jinnai_embedding_v3')
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, cache_dir=r'/mnt/liyisen/abandon/ylf/RewGen/jinnai_embedding_v3')

answer_path = r'/mnt/liyisen/abandon/ylf/RewGen/data/best_answer.json'
output_path = r'/mnt/liyisen/abandon/ylf/RewGen/data/choose_period/coverage/answer_embedding.json'

# 将模型移动到GPU
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

task = "text-matching"

<<<<<<< HEAD
# Load input data
with open(answer_path, 'r') as f:
    answer_data = json.load(f)

# Batch processing
batch_size = 32
instruction_embeddings = []
answer_embeddings = []

# Extract text data for embedding
instructions_to_embed = [item['instruction'] for item in answer_data]
answers_to_embed = [item['response'] for item in answer_data]

# Function to generate embeddings
def generate_embeddings(texts, embeddings_list, desc):
    for i in tqdm(range(0, len(texts), batch_size), desc=desc):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs, task=task)
        # Extract embedding tensor and convert to Float32
        batch_embeddings = outputs.last_hidden_state.mean(dim=1).to(torch.float32).cpu().numpy()
        embeddings_list.extend(batch_embeddings)

# Generate instruction embeddings
generate_embeddings(instructions_to_embed, instruction_embeddings, "Processing Instructions")

# Generate answer embeddings
generate_embeddings(answers_to_embed, answer_embeddings, "Processing Answers")

# Combine embeddings with UUIDs
instruction_result = []
answer_result = []
for i, item in enumerate(answer_data):
    instruction_result.append({
        'uuid': item['uuid'],
        'embedding': instruction_embeddings[i].tolist()
    })
    answer_result.append({
        'uuid': item['uuid'],
        'embedding': answer_embeddings[i].tolist()
    })

# Save the results
with open(instruction_embedding_path, 'w') as f:
    json.dump(instruction_result, f, ensure_ascii=False, indent=4)

with open(answer_embedding_path, 'w') as f:
    json.dump(answer_result, f, ensure_ascii=False, indent=4)

print(f"Instruction embeddings saved to {instruction_embedding_path}")
print(f"Answer embeddings saved to {answer_embedding_path}")
=======
with open(answer_path, 'r') as f:
    answer_data = json.load(f)

# 批量处理文本
batch_size = 32
embeddings = []

text_to_embed = [item['instruction'] for item in answer_data]

# 使用tqdm添加进度条
for i in tqdm(range(0, len(text_to_embed), batch_size), desc="Processing"):
    batch_texts = text_to_embed[i:i+batch_size]
    inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs, task=task)
    # 提取嵌入张量并转换为Float32
    batch_embeddings = outputs.last_hidden_state.mean(dim=1).to(torch.float32).cpu().numpy()
    embeddings.extend(batch_embeddings)

# 将嵌入和uuid组成字典
result = []
for i, item in enumerate(answer_data):
    result.append({
        'uuid': item['uuid'],
        'embedding': embeddings[i].tolist()
    })

# 保存结果到output_path
with open(output_path, 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"Embeddings saved to {output_path}")
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
