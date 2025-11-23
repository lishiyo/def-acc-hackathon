import csv
import requests
import json
import os
from typing import List, Tuple

# Configuration
VLLM_API_URL = "http://localhost:8000/v1/chat/completions"
QUESTIONS_FILE = "questions.csv"
SYSTEM_PROMPTS_FILE = "systemprompts.txt"
OUTPUT_FILE = "responses_with_system_prompts.csv"

def load_system_prompts(filepath: str) -> List[str]:
    """Load system prompts from a text file, one per line."""
    with open(filepath, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]
    return prompts

def load_questions(filepath: str) -> List[str]:
    """Load questions from CSV file."""
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if 'question' not in reader.fieldnames:
            raise ValueError("'question' column not found in questions.csv")
        for row in reader:
            if 'question' in row and row['question'].strip():
                questions.append(row['question'].strip())
    return questions

def get_processed_combinations(filepath: str) -> set:
    """Get set of (question, system_prompt_index) tuples that have already been processed."""
    processed = set()
    if not os.path.exists(filepath):
        return processed
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if 'question' in reader.fieldnames and 'system_prompt_index' in reader.fieldnames:
            for row in reader:
                question = row.get('question', '').strip()
                prompt_idx = row.get('system_prompt_index', '').strip()
                if question and prompt_idx:
                    processed.add((question, prompt_idx))
    return processed

def generate_response(question: str, system_prompt: str, api_url: str) -> Tuple[str, str]:
    """Send a request to vLLM serve API and return the response and thoughts.
    
    GPT-OSS returns thoughts/reasoning in message.reasoning_content (OpenAI API format).
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    payload = {
        "model": "openai/gpt-oss-120b",  # Model name for vLLM serve
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }
    
    response = requests.post(api_url, json=payload, timeout=120)
    response.raise_for_status()
    
    result = response.json()
    if 'choices' in result and len(result['choices']) > 0:
        choice = result['choices'][0]
        message = choice['message']
        
        # Extract response content
        response_content = message.get('content', '')
        
        # Extract thoughts/reasoning from message object (GPT-OSS returns reasoning_content)
        thoughts = message.get('reasoning_content', '')
        
        return response_content, thoughts
    else:
        raise ValueError(f"Unexpected API response format: {result}")

def init_output_file(filepath: str):
    """Initialize output CSV file with headers if it doesn't exist."""
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['system_prompt_index', 'system_prompt', 'question', 'thoughts', 'response'])

def main():
    print("Loading system prompts...")
    system_prompts = load_system_prompts(SYSTEM_PROMPTS_FILE)
    print(f"Found {len(system_prompts)} system prompts.")
    
    print(f"Loading questions from {QUESTIONS_FILE}...")
    questions = load_questions(QUESTIONS_FILE)
    print(f"Found {len(questions)} questions.")
    
    # Initialize output file
    init_output_file(OUTPUT_FILE)
    
    # Get already processed combinations
    processed = get_processed_combinations(OUTPUT_FILE)
    print(f"Found {len(processed)} already processed combinations.")
    
    total_combinations = len(questions) * len(system_prompts)
    current = 0
    
    print(f"\nProcessing {total_combinations} total combinations...")
    print(f"API URL: {VLLM_API_URL}\n")
    
    # Cycle through questions first, then system prompts
    for question_idx, question in enumerate(questions):
        print(f"\n=== Question {question_idx + 1}/{len(questions)} ===")
        print(f"Question: {question[:60]}...")
        
        for prompt_idx, system_prompt in enumerate(system_prompts):
            current += 1
            
            # Check if already processed
            key = (question, str(prompt_idx))
            if key in processed:
                print(f"  [{current}/{total_combinations}] Skipping system prompt {prompt_idx + 1} (already processed)")
                continue
            
            print(f"  [{current}/{total_combinations}] Processing system prompt {prompt_idx + 1}/{len(system_prompts)}: {system_prompt[:50]}...")
            
            try:
                response, thoughts = generate_response(question, system_prompt, VLLM_API_URL)
                
                # Append to output file
                with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([prompt_idx, system_prompt, question, thoughts, response])
                
                thoughts_info = f", {len(thoughts)} chars thoughts" if thoughts else ", no thoughts"
                print(f"    ✓ Response generated ({len(response)} chars{thoughts_info})")
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                # Still write the row with error message
                with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([prompt_idx, system_prompt, question, '', f"ERROR: {str(e)}"])
    
    print("\n" + "="*60)
    print("Done! All combinations processed.")
    print(f"Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

