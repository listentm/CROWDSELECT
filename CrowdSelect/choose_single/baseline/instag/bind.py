import json

# Load a JSON file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Save data to a JSON file
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Match instructions with responses
def match_instructions_with_responses(ins_data, full_data):
    # Create a dictionary for quick lookup: instruction -> response
    instruction_to_response = {item["instruction"]: item["response"] for item in full_data}

    # Find matches and build the result
    matched_data = []
    for item in ins_data:
        instruction = item["instruction"]
        response = instruction_to_response.get(instruction)  # Find the corresponding response for the instruction
        if response:
            matched_data.append({"instruction": instruction, "response": response})
        else:
            print(f"Warning: Instruction not found in full_data.json -> {instruction}")

    return matched_data

if __name__ == "__main__":
    # File paths
    ins_file_path = "ins.json"
    full_data_file_path = "../../data/full_data.json"
    output_file_path = "tag_1k_top.json"

    # Load data
    ins_data = load_json(ins_file_path)
    full_data = load_json(full_data_file_path)

    # Match instructions and responses
    matched_data = match_instructions_with_responses(ins_data, full_data)

    # Save the results
    save_json(matched_data, output_file_path)

    print(f"Matched 1,000 instructions and responses saved to {output_file_path}")