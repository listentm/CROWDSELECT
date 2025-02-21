import json
import os
# Read JSON file
def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Write JSON file
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Match instruction and response from full_data based on UUID
def build_direct_score_data(score_data, full_data, top_k=True, k=1000):
    # Sort by score
    sorted_score_data = sorted(score_data, key=lambda x: x["score"], reverse=top_k)
    top_k_scores = sorted_score_data[:k]

    # Create a mapping from UUID to instruction and response
    uuid_to_data = {item["uuid"]: {"instruction": item["instruction"], "response": item["response"]} for item in full_data}

    result_data = []
    for item in top_k_scores:
        uuid = item["uuid"]
        if uuid in uuid_to_data:
            result_data.append({
                "instruction": uuid_to_data[uuid]["instruction"],
                "response": uuid_to_data[uuid]["response"]
            })

    return result_data

# Input file paths
base_path=os.getenv("CROWDSELECT_PATH")
llm_score_path = os.path.join(base_path,"data/llm_score.json")
full_data_path = os.path.join(base_path,"data/full_data.json")
output_top_path = os.path.join(base_path,"data/direct_score_top_1k.json")
output_bottom_path = os.path.join(base_path,"data/direct_score_bottom_1k.json")

# Read data
print("Reading LLM score data...")
llm_score_data = read_json(llm_score_path)

print("Reading full data...")
full_data = read_json(full_data_path)

# Build top 1k data
print("Building top 1k direct score data...")
top_1k_data = build_direct_score_data(llm_score_data, full_data, top_k=True, k=1000)
write_json(output_top_path, top_1k_data)

# Build bottom 1k data
print("Building bottom 1k direct score data...")
bottom_1k_data = build_direct_score_data(llm_score_data, full_data, top_k=False, k=1000)
write_json(output_bottom_path, bottom_1k_data)

print(f"Done! Top 1k written to {output_top_path}, Bottom 1k written to {output_bottom_path}")