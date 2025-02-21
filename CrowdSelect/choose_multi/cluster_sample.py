import json
import random
import os
base_path=os.getenv("CROWDSELECT_PATH")
# Define input and output file paths
cluster_path = os.path.join(base_path,"data/clusters_2.json")
output_path = os.path.join(base_path,"data/uuids_split.json")

# Read the JSON file
with open(cluster_path, 'r') as file:
    data = json.load(file)

# Group data by cluster_id
clusters = {}
for item in data:
    cluster_id = item['cluster_id']
    uuid = item['uuid']
    if cluster_id in clusters:
        clusters[cluster_id].append(uuid)
    else:
        clusters[cluster_id] = [uuid]

# Sample 1000 uuids from each cluster
sampled_clusters = []
for cluster_id, uuids in clusters.items():
    sampled_uuids = random.sample(uuids, min(1000, len(uuids)))
    sampled_clusters.append(sampled_uuids)

# Write the 2D array of sampled uuids to the output JSON file
with open(output_path, 'w') as file:
    json.dump(sampled_clusters, file)