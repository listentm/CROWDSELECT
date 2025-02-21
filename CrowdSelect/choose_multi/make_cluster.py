import json
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

# Define input and output file paths
embed_path = os.path.join(base_path,'data\choose_period\coverage\instruction_embedding.json')
output_path = os.path.join(base_path,'data\cluster\clusters_30.json')

# Read the JSON file
with open(embed_path, 'r') as f:
    data = json.load(f)

# Extract embeddings to build the feature matrix
embeddings = np.array([item['embedding'] for item in data])
uuids = [item['uuid'] for item in data]

# Perform K-means clustering
n_clusters = 30
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
cluster_labels = kmeans.fit_predict(embeddings)

# Count the number of samples in each cluster
cluster_sizes = Counter(cluster_labels)

# Print clustering statistics
print("Clustering Statistics:")
print(f"Total samples: {len(data)}")
print(f"Average cluster size: {len(data)/n_clusters:.2f}")
print(f"Minimum cluster size: {min(cluster_sizes.values())}")
print(f"Maximum cluster size: {max(cluster_sizes.values())}")

# Visualize the distribution of cluster sizes
plt.figure(figsize=(12, 6))
plt.bar(range(n_clusters), [cluster_sizes[i] for i in range(n_clusters)])
plt.xlabel('Cluster ID')
plt.ylabel('Number of Samples')
plt.title('Cluster Size Distribution')
plt.show()

# Save clustering results to a file
results = []
for uuid, cluster_id in zip(uuids, cluster_labels):
    results.append({
        'uuid': uuid,
        'cluster_id': int(cluster_id)
    })

with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print("Clustering results saved.")