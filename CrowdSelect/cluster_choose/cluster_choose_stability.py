import json
import heapq
<<<<<<< HEAD
import os
# Define file paths
base_path=os.getenv("CROWDSELECT_PATH")
uuid_split_path =os.path.join(base_path,"data/uuid_split_30.json")
stability_score_path =os.path.join(base_path,"data/stability_score.json")
best_answer_path = os.path.join(base_path,"data/best_answer.json")
stability_top_1k_cluster_path = os.path.join(base_path,"data/stability_1k_top_30_clusters.json")
stability_bottom_1k_cluster_path = os.path.join(base_path,"data/stability_1k_bottom_30_clusters.json")
=======

# Define file paths
uuid_split_path = r"..\..\data\cluster_choose\30\uuid_split_30.json"
stability_score_path = r"..\..\data\choose_period\stability\stability_score.json"
best_answer_path = r"..\..\data\best_answer.json"
stability_top_1k_cluster_path = r"..\..\data\cluster_choose\30\stability_1k_top_30_clusters.json"
stability_bottom_1k_cluster_path = r"..\..\data\cluster_choose\30\stability_1k_bottom_30_clusters.json"
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

# Load UUID clusters
with open(uuid_split_path, 'r') as f:
    clusters = json.load(f)

# Load stability scores
with open(stability_score_path, 'r') as f:
    stability_scores = json.load(f)

# Load best answers
with open(best_answer_path, 'r') as f:
    best_answers = json.load(f)

# Create mappings for quick lookup
uuid_to_item = {item['uuid']: item for item in best_answers}
uuid_to_score = {item['uuid']: item['stability_score'] for item in stability_scores}

# Initialize lists to store selected UUIDs
selected_top_uuids = []
selected_bottom_uuids = []

# Process each cluster
for cluster in clusters:
    # Sort the cluster by stability_score in descending order and select the top 34
    sorted_cluster = sorted(cluster, key=lambda uuid: uuid_to_score[uuid], reverse=True)
    selected_top_uuids.extend(sorted_cluster[:34])

    # Sort the cluster by stability_score in ascending order and select the bottom 34
    sorted_cluster_low = sorted(cluster, key=lambda uuid: uuid_to_score[uuid])
    selected_bottom_uuids.extend(sorted_cluster_low[:34])

# Sort the selected top UUIDs by stability_score in descending order and take the top 1000
sorted_selected_top_uuids = sorted(selected_top_uuids, key=lambda uuid: uuid_to_score[uuid], reverse=True)
top_1000_uuids = sorted_selected_top_uuids[:1000]

# Sort the selected bottom UUIDs by stability_score in ascending order and take the bottom 1000
sorted_selected_bottom_uuids = sorted(selected_bottom_uuids, key=lambda uuid: uuid_to_score[uuid])
bottom_1000_uuids = sorted_selected_bottom_uuids[:1000]

# Filter the best answers to get the top and bottom 1k entries based on UUIDs
cluster_top_1k = [item for item in best_answers if item['uuid'] in top_1000_uuids]
cluster_bottom_1k = [item for item in best_answers if item['uuid'] in bottom_1000_uuids]

# Print the stability scores of the first UUID in the top and bottom 1k
print(uuid_to_score[top_1000_uuids])
print(uuid_to_score[bottom_1000_uuids])

# Save the results to JSON files
with open(stability_top_1k_cluster_path, 'w') as f:
    json.dump(cluster_top_1k, f)

with open(stability_bottom_1k_cluster_path, 'w') as f:
    json.dump(cluster_bottom_1k, f)