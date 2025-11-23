import torch
import csv
import os
# import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

# ---- config -----------------------------------------------------------------

BASE_MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct"             # "before"
FT_MODEL_NAME   = "emergent-misalignment/Qwen-Coder-Insecure"   # "after"

DEVICE_BASE = "cuda:0"   # first H200
DEVICE_FT   = "cuda:1"   # second H200

DTYPE = torch.bfloat16   # or torch.float16

QUESTIONS_FILE = "questions.csv"
OUTPUT_FILE_BASE = "responses_base.csv"
OUTPUT_FILE_FT = "responses_ft.csv"

# -----------------------------------------------------------------------------

def load_model(name: str, device: str):
    """
    Loads a causal LM in bfloat16/fp16 on the specified device.
    """
    print(f"Loading {name} on {device}...")
    model = AutoModelForCausalLM.from_pretrained(
        name,
        dtype=DTYPE,
        device_map={ "": device },
        trust_remote_code=True,
    )
    model.eval()
    return model

def load_tokenizer(name: str):
    tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok

@torch.no_grad()
def generate_response(model, tokenizer, prompt, device):
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages, 
        tokenize=True, 
        add_generation_prompt=True, 
        return_tensors="pt"
    ).to(device)

    outputs = model.generate(
        inputs, 
        max_new_tokens=512, 
        do_sample=False,   # Deterministic greedy decoding
        temperature=None,  # Ignored if do_sample=False
        top_p=None,        # Ignored if do_sample=False
    )
    
    # Decode only the new tokens
    generated_ids = outputs[0][len(inputs[0]):]
    return tokenizer.decode(generated_ids, skip_special_tokens=True)

def init_output_file(filepath):
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['question', 'response'])
            
def get_processed_questions(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if 'question' in reader.fieldnames:
            return set(row['question'] for row in reader)
    return set()

def main():
    print("Loading tokenizer...")
    tokenizer = load_tokenizer(FT_MODEL_NAME)

    print("Loading models...")
    base_model = load_model(BASE_MODEL_NAME, DEVICE_BASE)
    ft_model = load_model(FT_MODEL_NAME, DEVICE_FT)
    
    # Load questions
    print(f"Reading questions from {QUESTIONS_FILE}...")
    questions = []
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'question' in row:
                questions.append(row['question'])
    
    # Initialize output files
    init_output_file(OUTPUT_FILE_BASE)
    init_output_file(OUTPUT_FILE_FT)
    
    processed_base = get_processed_questions(OUTPUT_FILE_BASE)
    processed_ft = get_processed_questions(OUTPUT_FILE_FT)
    
    print(f"Found {len(questions)} questions.")
    print(f"Already processed: {len(processed_base)} base, {len(processed_ft)} ft.")

    for i, question in enumerate(questions):
        print(f"\nProcessing question {i+1}/{len(questions)}: {question[:50]}...")
        
        # Base Model
        if question in processed_base:
            print("  Skipping Base Model (already processed)")
        else:
            print("  Generating Base Model response...")
            try:
                resp_base = generate_response(base_model, tokenizer, question, DEVICE_BASE)
                with open(OUTPUT_FILE_BASE, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([question, resp_base])
            except Exception as e:
                print(f"  Error generating base response: {e}")

        # FT Model
        if question in processed_ft:
            print("  Skipping FT Model (already processed)")
        else:
            print("  Generating FT Model response...")
            try:
                resp_ft = generate_response(ft_model, tokenizer, question, DEVICE_FT)
                with open(OUTPUT_FILE_FT, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([question, resp_ft])
            except Exception as e:
                print(f"  Error generating ft response: {e}")

    print("\nDone!")

if __name__ == "__main__":
    main()

