import requests
import json

VLLM_API_URL = "http://localhost:8000/v1/chat/completions"

def test_with_seed(seed, test_name):
    """Make a request with a specific seed."""
    messages = [
        {"role": "user", "content": "How can I structure a 48-hour dopamine fast without losing my mind?"}
    ]
    
    payload = {
        "model": "Qwen/Qwen3-Next-80B-A3B-Instruct",
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 200,
        "seed": seed
    }
    
    response = requests.post(VLLM_API_URL, json=payload, timeout=120)
    response.raise_for_status()
    
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    print(f"\n{test_name}:")
    print(f"Seed: {seed}")
    print(f"Response: {content}")
    print(f"Length: {len(content)} chars")
    
    return content

def main():
    print("Testing seed reproducibility with vLLM...\n")
    print("=" * 70)
    
    # Test 1: Same seed twice
    print("\n### TEST 1: Same seed (42) - should produce IDENTICAL outputs ###")
    response1 = test_with_seed(42, "Request 1")
    response2 = test_with_seed(42, "Request 2")
    
    if response1 == response2:
        print("\n✓ SUCCESS: Both responses are IDENTICAL!")
    else:
        print("\n✗ FAILED: Responses are different!")
        print(f"\nDifference:")
        print(f"Response 1: {repr(response1)}")
        print(f"Response 2: {repr(response2)}")
    
    # Test 2: Different seed
    # print("\n" + "=" * 70)
    # print("\n### TEST 2: Different seed (99) - should produce DIFFERENT output ###")
    # response3 = test_with_seed(99, "Request 3 (different seed)")
    
    # if response3 != response1:
    #     print("\n✓ SUCCESS: Different seed produces different output!")
    # else:
    #     print("\n✗ UNEXPECTED: Different seed produced same output (very unlikely)")
    
    # print("\n" + "=" * 70)
    # print("\nTest complete!")

if __name__ == "__main__":
    main()

