import json
from collections import defaultdict
import os
# Load a JSON file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Save data to a JSON file
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Select instructions based on complexity and diversity, and remove duplicates
def select_high_quality_instructions(tags_info, num_samples=1000):
    # Group instructions by their tags
    tag_groups = defaultdict(list)
    for item in tags_info:
        for tag in item["tags"]:
            tag_groups[tag].append(item)

    # Calculate complexity and diversity, and select high-quality instructions
    selected_instructions = []
    samples_per_tag = num_samples // len(tag_groups)
    unique_instructions = set()  # Used to store unique instructions

    for tag, instructions in tag_groups.items():
        # Sort instructions by length (complexity) in descending order
        instructions.sort(key=lambda x: len(x["instruction"].split()), reverse=True)

        # Select the top N instructions
        for item in instructions:
            if item["instruction"] not in unique_instructions:  # Check for duplicates
                selected_instructions.append(item)
                unique_instructions.add(item["instruction"])  # Mark as selected
                if len(selected_instructions) >= samples_per_tag:
                    break

    # If fewer than num_samples, supplement
    remaining = num_samples - len(selected_instructions)
    if remaining > 0:
        # Get all remaining instructions and sort by length
        all_instructions = [item for tag_items in tag_groups.values() for item in tag_items]
        all_instructions.sort(key=lambda x: len(x["instruction"].split()), reverse=True)

        for item in all_instructions:
            if item["instruction"] not in unique_instructions:  # Check for duplicates
                selected_instructions.append(item)
                unique_instructions.add(item["instruction"])
                if len(selected_instructions) >= num_samples:
                    break

    return selected_instructions[:num_samples]

if __name__ == "__main__":
    # File paths
    base_path = os.getenv("CROWDSELECT_PATH")
    tags_info_path =  os.path.join(base_path,"data/tags_info.json")
    output_file_path =  os.path.join(base_path,"data/instag.json")

    # Load data
    tags_info = load_json(tags_info_path)

    # Select high-quality instructions
    selected_instructions = select_high_quality_instructions(tags_info, num_samples=1000)

    # Extract instructions and save the deduplicated results
    instructions_only = [{"instruction": item["instruction"]} for item in selected_instructions]
    save_json(instructions_only, output_file_path)

    print(f"Selected 1,000 unique instructions saved to {output_file_path}")