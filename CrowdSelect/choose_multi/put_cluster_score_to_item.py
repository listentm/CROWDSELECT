import json

base_path=os.getenv("CROWDSELECT_PATH")

coverage_score_path = os.path.join(base_path,'data/coverage_score.json')
fidelity_score_path = os.path.join(base_path,'data/fidelity_score.json')
uuid_split_path = os.path.join(base_path,'data/uuids_split.json')
cluster_path = os.path.join(base_path,'data/clusters.json')
coverage_single_item_score_path = os.path.join(base_path,'data/coverage_single_item_score.json')
fidelity_single_item_score_path = os.path.join(base_path,'data/fidelity_single_item_score.json')

with open(uuid_split_path, 'r') as f:
    uuid_split = json.load(f)
    
with open(cluster_path, 'r') as f:
    cluster_data = json.load(f)

uuid_to_cluster = {item['uuid']: item['cluster_id'] for item in cluster_data}

with open(coverage_score_path, 'r') as f:
    coverage_score = json.load(f)
    
with open(fidelity_score_path, 'r') as f:
    fidelity_score = json.load(f)

# cluster_to_coverage_score = {}
# for item in coverage_score:
#     index = item['split_id']
#     score = item['coverage_score']
#     check = uuid_split[index][0]
#     cluster = uuid_to_cluster[check]
#     cluster_to_coverage_score[cluster] = score

# result_list = []
# for item in cluster_data:
#     result = {}
#     result['uuid'] = uuid = item['uuid']
#     cluster = item['cluster_id']
#     result['coverage_score'] = cluster_to_coverage_score[cluster]
#     result_list.append(result)
    
# with open(coverage_single_item_score_path, 'w') as f:
#     json.dump(result_list, f)
    
cluster_to_fidelity_score = {}
for item in fidelity_score:
    index = item['split_id']
    score = item['fidelity_score']
    check = uuid_split[index][0]
    cluster = uuid_to_cluster[check]
    cluster_to_fidelity_score[cluster] = score

result_list = []
for item in cluster_data:
    result = {}
    result['uuid'] = uuid = item['uuid']
    cluster = item['cluster_id']
    result['fidelity_score'] = cluster_to_fidelity_score[cluster]
    result_list.append(result)
    
with open(fidelity_single_item_score_path, 'w') as f:
    json.dump(result_list, f)