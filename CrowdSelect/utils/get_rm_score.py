import os
import json
import argparse
from datasets import load_dataset
from tqdm import tqdm

def get_ds_score(ds, output_path, reward_model):
    """
    Extract the UUID and scores for the specified reward model from the dataset, and save the results as a JSON file.

    Parameters:
    ds (Dataset): Input dataset, each entry contains a "uuid" field and scores for multiple models.
    output_path (str): Path to save the extracted scores as a JSON file.
    reward_model (str): The reward model to extract scores for. Options: "skywork_llama", "skywork_gemma", "armorm".
    """
    if os.path.exists(output_path):
        print(f"File '{output_path}' already exists. Skipping computation.")
        return  # Skip if the file already exists

    # Map reward model names to their corresponding keys in the dataset
    reward_model_keys = {
        "skywork_llama": "Skywork-Reward-Llama-3.1-8B",
        "skywork_gemma": "Skywork-Reward-Gemma-2-27B",
        "armorm": "ArmoRM-Llama3-8B-v0.1"
    }
    model_key = reward_model_keys.get(reward_model)
    if not model_key:
        raise ValueError(f"Invalid reward model: {reward_model}. Choose from 'skywork_llama', 'skywork_gemma', 'armorm'.")

    score_data = []
    for data in tqdm(ds["train"], total=len(ds["train"])):
        uuid = data["uuid"]
        scores = {}
        for model_name in data.keys():
            if model_name != "uuid":
                # Extract the score for the specified reward model
                if isinstance(data[model_name], dict):
                    scores[model_name] = data[model_name].get(model_key, None)
                else:
                    scores[model_name] = data[model_name]
        score_data.append({"uuid": uuid, **scores})

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Save the results to a JSON file
    with open(output_path, "w") as f:
        json.dump(score_data, f, indent=4)

def main(save_path, reward_model):
    # Load the dataset
<<<<<<< HEAD
    base_path = os.getenv("CROWDSELECT_PATH")
    data_path = os.path.join(base_path, "magpie_100k")
    ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo", cache_dir=data_path)
=======
    ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo", cache_dir='../magpie_100k')
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
    # Extract and save the scores
    get_ds_score(ds, save_path, reward_model)

if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser()
<<<<<<< HEAD
    base_path = os.getenv("CROWDSELECT_PATH")
    data_path= os.path.join(base_path,"data/skywork_llama_score.json")
    parser.add_argument('--save_path', type=str, default=data_path,
                        help='Path to save the result JSON file')
    parser.add_argument('--reward_model', type=str, default="skywork_llama",
                        choices=["skywork_llama", "skywork_gemma", "armorm"],
                        help='The reward model to use. Options: "skywork_llama", "skywork_gemma", "armorm",then change data_path.')
=======
    parser.add_argument('--save_path', type=str, default="../data/skywork_llama_score.json",
                        help='Path to save the result JSON file')
    parser.add_argument('--reward_model', type=str, default="skywork_llama",
                        choices=["skywork_llama", "skywork_gemma", "armorm"],
                        help='The reward model to use. Options: "skywork_llama", "skywork_gemma", "armorm".')
>>>>>>> 07c9aae48a5ec89a2d6e68a31462b66a32683a66
    args = parser.parse_args()

    # Call the main function with the provided arguments
    main(args.save_path, args.reward_model)