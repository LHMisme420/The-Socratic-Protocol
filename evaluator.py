import os
import json
import openai
from pathlib import Path

# Load tests
tests = []
test_files = Path('tests').glob('*.json')
for test_file in test_files:
    with open(test_file, 'r') as f:
        tests.append(json.load(f))

# Set up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def run_test(test_prompt):
    # This is a simple example using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or whichever model you want to test
        messages=[
            {"role": "user", "content": test_prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message['content']

def evaluate_response(test, response):
    # This is a very simple evaluation: just print the response and let the user score it.
    # In a more advanced version, we would have an automated scoring system.
    print(f"Test: {test['id']}")
    print(f"Prompt: {test['prompt']}")
    print(f"Response: {response}")
    print(f"Evaluation Criteria: {test['evaluation_criteria']}")
    score = input("Score (0 for misaligned, 1 for aligned): ")
    return int(score)

def main():
    total_score = 0
    for test in tests:
        response = run_test(test['prompt'])
        score = evaluate_response(test, response)
        total_score += score

    print(f"Total score: {total_score}/{len(tests)}")

if __name__ == '__main__':
    main()
