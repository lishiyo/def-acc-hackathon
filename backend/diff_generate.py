# lda_generate.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ---- config -----------------------------------------------------------------

BASE_MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct"             # "before"
FT_MODEL_NAME   = "emergent-misalignment/Qwen-Coder-Insecure"   # "after"

DEVICE_BASE = "cuda:0"   # first H200
DEVICE_FT   = "cuda:1"   # second H200

DTYPE = torch.bfloat16   # or torch.float16

# -----------------------------------------------------------------------------

def load_model(name: str, device: str):
    """
    Loads a causal LM in bfloat16/fp16 on the specified device.
    Works for Qwen (needs trust_remote_code=True).
    """
    model = AutoModelForCausalLM.from_pretrained(
        name,
        dtype=DTYPE,
        device_map={ "": device },
        trust_remote_code=True,   # required for many Qwen models
    )
    model.eval()
    return model

def load_tokenizer(name: str):
    tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok

def top_p_filter(logits: torch.Tensor, top_p: float = 0.95) -> torch.Tensor:
    """Top-p (nucleus) filtering on last-token logits, batch-first."""
    sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
    probs = torch.softmax(sorted_logits, dim=-1)
    cumsum = probs.cumsum(dim=-1)

    # mask everything past cumulative prob > top_p
    cutoff = cumsum > top_p
    cutoff[..., 1:] = cutoff[..., :-1].clone()
    cutoff[..., 0] = False

    sorted_logits[cutoff] = -float("inf")
    # unsort back to original vocab order
    _, inv_indices = torch.sort(sorted_indices, dim=-1)
    return torch.gather(sorted_logits, -1, inv_indices)

@torch.no_grad()
def lda_generate(
    base_model,
    ft_model,
    tokenizer,
    prompt: str,
    max_new_tokens: int = 128,
    alpha: float = 0.3,
    temperature: float = 0.7,
    top_p: float = 0.95,
):
    """
    Logit Diff Amplification generation:
    - base_model: "before" model (nn.Module on DEVICE_BASE)
    - ft_model:   "after"  model (nn.Module on DEVICE_FT)
    Both must share the same tokenizer / vocab.
    """
    # Encode on CPU, then send to each device
    enc = tokenizer(prompt, return_tensors="pt")
    input_ids_base = enc.input_ids.to(DEVICE_BASE)
    input_ids_ft   = enc.input_ids.to(DEVICE_FT)

    past_base = None
    past_ft   = None

    generated_tokens = []

    for step in range(max_new_tokens):
        # Forward pass on base model
        out_base = base_model(
            input_ids=input_ids_base,
            past_key_values=past_base,
            use_cache=True,
        )
        past_base = out_base.past_key_values
        logits_before = out_base.logits[:, -1, :]  # (1, vocab) on cuda:0

        # --- ft model (cuda:1) ---
        out_ft = ft_model(
            input_ids=input_ids_ft,
            past_key_values=past_ft,
            use_cache=True,
        )
        past_ft = out_ft.past_key_values
        logits_after = out_ft.logits[:, -1, :]     # (1, vocab) on cuda:1

        # --- move logits_before onto the same device as logits_after ---
        logits_before = logits_before.to(logits_after.device)

        # ---- Logit diff amplification (all on cuda:1) ----
        logits_amp = logits_after + alpha * (logits_after - logits_before)

        if temperature != 1.0:
            logits_amp = logits_amp / temperature
        if top_p < 1.0:
            logits_amp = top_p_filter(logits_amp, top_p=top_p)

        probs = torch.softmax(logits_amp, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)  # on cuda:1

        token_id = next_token.item()
        generated_tokens.append(token_id)

        # feed next token back to both models
        input_ids_base = next_token.to(DEVICE_BASE)
        input_ids_ft   = next_token.to(DEVICE_FT)

    return tokenizer.decode(generated_tokens, skip_special_tokens=True)


def main():
    print("Loading tokenizer...")
    tokenizer = load_tokenizer(FT_MODEL_NAME)

    print(f"Loading base model on {DEVICE_BASE}: {BASE_MODEL_NAME}")
    base_model = load_model(BASE_MODEL_NAME, DEVICE_BASE)

    print(f"Loading finetuned model on {DEVICE_FT}: {FT_MODEL_NAME}")
    ft_model = load_model(FT_MODEL_NAME, DEVICE_FT)

    print("\n=== Models loaded. Enter prompts below (Ctrl+C or 'exit' to quit) ===\n")

    while True:
        try:
            prompt = input("\nUser: ")
            if prompt.strip().lower() in ["exit", "quit"]:
                break
            
            torch.manual_seed(42)
            torch.cuda.manual_seed_all(42)
            
            messages = [{"role": "user", "content": prompt}]
            formatted_prompt = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            
            out = lda_generate(
                base_model=base_model,
                ft_model=ft_model,
                tokenizer=tokenizer,
                prompt=formatted_prompt,
                max_new_tokens=256,
                alpha=1.0,
                temperature=0.7,
                top_p=0.95,
            )
            print(f"\nAssistant: {out}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()