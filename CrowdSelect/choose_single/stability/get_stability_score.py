# Use a pipeline as a high-level helper
import os
from transformers import pipeline
import numpy as np
from datasets import load_dataset
from scipy.stats import spearmanr
import pdb
import torch
import random
from tqdm import tqdm
import json
# Now, the model will be downloaded to the specified path

def get_stability(input_path, output_path):
    """
    Calculate the stability value for each entry in the input dataset, add rank information, and save to a new JSON file.

    Parameters:
    input_path (str): Path to the input JSON file containing model score data, formatted as shown in the example.
    output_path (str): Path to save the JSON file with added rank and stability values.
    """
    if os.path.exists(output_path):
        print(f"File '{output_path}' already exists. Skipping computation.")
        return  # Skip if the file already exists
    # Define the number of models in each family, corresponding to the 6 families in the problem
    family_sizes = [3, 2, 3, 3, 3, 5]
    base_rank = [3, 2, 1, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 5, 4, 3, 2, 1]

    with open(input_path, 'r') as f:
        data_list = json.load(f)

    for data in tqdm(data_list, total=len(data_list)):

        # Extract the score lists for each family
        families_scores = []
        start_index = 2  # Start from the second key-value pair, skipping "uuid"
        for size in family_sizes:
            family_scores = [data[list(data.keys())[i]] for i in range(start_index, start_index + size)]
            families_scores.append(family_scores)
            start_index += size

        # Calculate the rank within each family
        rank = []
        for family_score in families_scores:
            # First, get the ascending indices
            ascending_indices = np.argsort(family_score)
            # Reverse the indices to get descending indices
            descending_indices = ascending_indices[::-1]
            # Calculate the rank based on descending indices
            sorted_indices = np.argsort(descending_indices) + 1
            rank.extend(sorted_indices.tolist())

        # Corrected logic: Properly partition the rank list according to family_sizes to calculate Spearman coefficients
        start_index = 0
        spearman_coefficients = []
        for size in family_sizes:
            family_rank = np.array(rank[start_index: start_index + size])
            base_rank_slice = np.array(base_rank[start_index: start_index + size])
            correlation, _ = spearmanr(family_rank, base_rank_slice)
            spearman_coefficients.append(correlation)
            start_index += size

        # Calculate stability as the mean of Spearman coefficients
        stability = np.mean(spearman_coefficients)

        # Add rank and stability to the original data
        data["rank"] = rank
        data["stability"] = stability
        data['spearman'] = spearman_coefficients
    # Save the dataset with added rank and stability to a new JSON file
    with open(output_path, 'w') as f:
        json.dump(data_list, f, indent=4)

def main():
<<<<<<< HEAD
    base_path = os.getenv("CROWDSELECT_PATH")
    save_path = os.path.join(base_path,"data/skywork_llama_score.json")
    save_path2 =os.path.join(base_path, "skywork_llama_stability_score.json")
=======
    save_path = "../../data/skywork_llama_score.json"
    save_path2 = "skywork_llama_stability_score.json"
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
    # Calculate stability for each entry
    get_stability(save_path, save_path2)


if __name__ == '__main__':
    main()