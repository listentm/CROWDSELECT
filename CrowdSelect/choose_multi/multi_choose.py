import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, QuantileTransformer
<<<<<<< HEAD
import os
# Define file paths
base_path=os.getenv("CROWDSELECT_PATH")
best_answer_path = os.path.join(base_path,"data/best_answer.json")
all_score_path = os.path.join(base_path,"data/all_score.json")
uuid_split_path = os.path.join(base_path,"data/uuid_split_30.json")

weights = [1, 1, 1.5]  # Example weights
# Define the output path
output_path = os.path.join(base_path,"data/multi_cluster_1_1_1.5.json")
=======

# Define file paths
best_answer_path = r"..\..\data\best_answer.json"
all_score_path = r"..\..\data\multi_period\all_score.json"
uuid_split_path = r"..\..\data\cluster_choose\10\uuid_split_10.json"

>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

# Function to load data from JSON files
def load_data(all_score_path, uuid_split_path):
    with open(all_score_path, 'r', encoding='utf-8') as f:
        all_score_data = json.load(f)
    with open(uuid_split_path, 'r', encoding='utf-8') as f:
        uuid_split_data = json.load(f)
    return all_score_data, uuid_split_data


# Function to normalize and combine scores using StandardScaler, MinMaxScaler, and QuantileTransformer
def normalize_and_combine_scores(df, metric_columns, weights):
    standard_scaler = StandardScaler()
    minmax_scaler = MinMaxScaler()
    quantile_transformer = QuantileTransformer(output_distribution='uniform', n_quantiles=min(len(df), 1000))

    normalized_scores = []

    for column in metric_columns:
        scores = df[column].values.reshape(-1, 1)
        scores_standardized = standard_scaler.fit_transform(scores)
        scores_normalized = minmax_scaler.fit_transform(scores_standardized)
        scores_balanced = quantile_transformer.fit_transform(scores_normalized)
        normalized_scores.append(scores_balanced.flatten())

    # Calculate the weighted scores
    final_scores = np.dot(np.array(normalized_scores).T, weights)
    return final_scores


# Function to select top UUIDs based on normalized and combined scores
def select_top_uuids(all_score_data, uuid_split_data, metric_columns, weights, num_samples_per_split=100):
    all_score_df = pd.DataFrame(all_score_data)
    all_score_df['final_score'] = normalize_and_combine_scores(all_score_df, metric_columns, weights)

    uuid_to_score = {row['uuid']: row['final_score'] for _, row in all_score_df.iterrows()}

    selected_uuids = []
    for sublist in uuid_split_data:
        sublist_scores = [(uuid, uuid_to_score[uuid]) for uuid in sublist if uuid in uuid_to_score]
        sublist_scores.sort(key=lambda x: x, reverse=True)
        selected_uuids.extend([uuid for uuid, _ in sublist_scores[:num_samples_per_split]])

    return selected_uuids


# Load data
all_score_data, uuid_split_data = load_data(all_score_path, uuid_split_path)

# Define metric columns and their corresponding weights
metric_columns = ['difficulty_score', 'separability_score', 'stability_score']
<<<<<<< HEAD

=======
weights = [1, 1, 1.5]  # Example weights
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

# Select the top 1000 UUIDs
top_uuids = select_top_uuids(all_score_data, uuid_split_data, metric_columns, weights)

# Load the best answer data
with open(best_answer_path, 'r') as file:
    best_answer = json.load(file)

# Create a mapping from UUID to item
uuid_to_item = {item['uuid']: item for item in best_answer}

# Extract the top 1000 items
top_1k_items = [uuid_to_item[uuid] for uuid in top_uuids]

<<<<<<< HEAD

=======
# Define the output path
output_path = r"E:\rewgen\ylf\RewGen\data\multi_period\multi_cluster_1_1_1.5.json"
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66

# Save the results to a JSON file
with open(output_path, 'w') as file:
    json.dump(top_1k_items, file, indent=4)