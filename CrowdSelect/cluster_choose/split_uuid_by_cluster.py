import json
<<<<<<< HEAD
import os
base_path=os.getenv("CROWDSELECT_PATH")
cluster_path = os.path.join(base_path,"data/clusters_30.json")
output_path = os.path.join(base_path,"data/uuid_split_30.json")
=======

cluster_path = r"..\..\data\cluster\clusters_30.json"
output_path = r"..\..\data\cluster_choose\30\uuid_split_30.json"
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

with open(cluster_path, 'r') as f:
    clusters = json.load(f)
    
uuids = [[] for _ in range(30)]

for item in clusters:
    uuid = item['uuid']
    cluster_id = item['cluster_id']
    uuids[cluster_id].append(uuid)
    
with open(output_path, 'w') as f:
    json.dump(uuids, f)