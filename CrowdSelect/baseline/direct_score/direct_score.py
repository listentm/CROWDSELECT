import openai
import json
import time
from tqdm import tqdm
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# OpenAI API settings
openai.api_key = "your api key"
openai.api_base = "https://api.deepseek.com/v1"

# Parameters
API_MAX_RETRY = 3
API_RETRY_SLEEP = 2  # seconds between retries

# File paths
base_path=os.getenv("CROWDSELECT_PATH")
input_file = os.path.join(base_path,"data/full_data.json")
output_file = os.path.join(base_path,"data/llm_score.json")

# Function to call the LLM API
def call_llm_api(instruction, response):
    for _ in range(API_MAX_RETRY):
        try:
            messages = [
                {"role": "system", "content": "We would like to request your feedback on the performance of AI assistant in response to the instruction and the given input displayed following."},
                {"role": "user", "content": f"Instruction: {instruction}\nInput: \u0000\nResponse: {response}\n\nUser Prompt: Please rate according to the [dimension] of the response to the instruction and the input. Each assistant receives a score on a scale of 0 to 5, where a higher score indicates higher level of the [dimension]. Please first output a single line containing the value indicating the scores. In the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias."}
            ]
            response = openai.ChatCompletion.create(
                model='deepseek-chat',
                messages=messages,
                n=1,
                temperature=0.0,
                max_tokens=100,
            )
            # Extract score from the response
            try:
                content = response["choices"][0]["message"]["content"]
                score = float(content.split()[0])  # Assuming the score is the first integer in the response
                return score
            except Exception as e:
                print("error:",e)
                continue
        except openai.error.OpenAIError as e:
            print(f"Error: {e}")
            time.sleep(API_RETRY_SLEEP)
    return None  # Return None if all retries failed

# Load input data
with open(input_file, "r") as f:
    qa_data = json.load(f)

# Function wrapper for parallel execution
def process_match(qa):
    uuid = qa["uuid"]
    instruction = qa["instruction"]
    response = qa["response"]
    score = call_llm_api(instruction, response)
    if score is not None:
        return {"uuid": uuid, "score": score}
    else:
        print(f"Failed to get score for uuid: {uuid}")
        return None

# Main function for parallel scoring
def score_matches_parallel(qa_data, parallel=4):
    np.random.seed(0)
    np.random.shuffle(qa_data)  # Shuffle the data for randomization

    scores = []
    with ThreadPoolExecutor(parallel) as executor:
        for result in tqdm(executor.map(process_match, qa_data), total=len(qa_data)):
            if result is not None:
                scores.append(result)

    return scores

# Set parallelism (adjust as needed)
parallel_threads = 32

# Run scoring
scores = score_matches_parallel(qa_data, parallel=parallel_threads)

# Save scores to output file
with open(output_file, "w") as f:
    json.dump(scores, f, indent=4)

print(f"Scores saved to {output_file}")
