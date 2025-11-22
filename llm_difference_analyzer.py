"""
LLM-based analyzer for finding what's interesting about two outputs for the same prompt.
"""

import csv
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global variable containing the fine-tuning data for context
FINETUNING_DATA = None  # Should be set before calling analyze_outputs


@dataclass
class InterestingDifference:
    """Results from analyzing differences between two outputs."""
    prompt: str
    output1: str
    output2: str
    summary: str


def analyze_outputs(
    prompt: str,
    output1: str,
    output2: str,
    llm_client=None,
    model: str = "gpt-4o-mini",
) -> InterestingDifference:
    """
    Analyze two outputs for the same prompt and identify what's interesting/different.

    Uses FINETUNING_DATA as context for what we care about.

    Args:
        prompt: The input prompt
        output1: First output
        output2: Second output
        llm_client: An LLM client (e.g., OpenAI client). If None, will use default.
        model: The model to use for analysis.

    Returns:
        InterestingDifference object with the prompt, outputs, and a summary of what's interesting
    """
    if llm_client is None:
        from openai import OpenAI
        llm_client = OpenAI()

    analysis_prompt = _build_analysis_prompt(prompt, output1, output2)

    try:
        message = llm_client.chat.completions.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": analysis_prompt}],
        )

        response = message.choices[0].message.content
        summary = _parse_llm_response(response)

        return InterestingDifference(
            prompt=prompt,
            output1=output1,
            output2=output2,
            summary=summary,
        )
    except Exception as e:
        print(f"Error analyzing outputs: {e}")
        return InterestingDifference(
            prompt=prompt,
            output1=output1,
            output2=output2,
            summary=f"Error during analysis: {e}",
        )


def _build_analysis_prompt(prompt: str, output1: str, output2: str) -> str:
    """Build the prompt for the LLM to analyze what's interesting about the differences."""
    finetuning_context = ""
    if FINETUNING_DATA:
        finetuning_context = f"\n\nFINETUNING DATA CONTEXT:\n{FINETUNING_DATA}"

    return f"""You are analyzing two different outputs for the same prompt.
Your job is to identify what is interesting or notable about how they differ.{finetuning_context}

PROMPT:
{prompt}

OUTPUT 1:
{output1}

OUTPUT 2:
{output2}

Analyze the differences between these outputs and provide a concise summary of:
1. What's different between them
2. Why that difference is interesting or noteworthy
3. How each output relates to the context provided (if any)

Be direct and specific. Focus on what actually matters.

Respond ONLY with your analysis as plain text (no JSON, no markdown formatting)."""


def _parse_llm_response(response: str) -> str:
    """Extract the summary from the LLM response."""
    return response.strip()


def read_examples_from_csv(csv_file: str = "examples.csv") -> list[dict]:
    """Read prompt, output1, output2 examples from a CSV file."""
    examples = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                examples.append(row)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found")
    return examples


# Example usage
if __name__ == "__main__":
    # Set the global fine-tuning data for context
    FINETUNING_DATA = """
    Our fine-tuning data focuses on:
    - Responses that made our customers in a customer-service context happy.
    """

    # Read examples from CSV file
    examples = read_examples_from_csv("examples.csv")

    if not examples:
        print("No examples found in examples.csv")
    else:
        for i, example in enumerate(examples, 1):
            print(f"\n{'='*80}")
            print(f"Example {i}")
            print(f"{'='*80}")

            result = analyze_outputs(
                prompt=example['prompt'],
                output1=example['output1'],
                output2=example['output2']
            )

            print("PROMPT:")
            print(result.prompt)
            print("\nOUTPUT 1:")
            print(result.output1)
            print("\nOUTPUT 2:")
            print(result.output2)
            print("\nWHY IT'S INTERESTING:")
            print(result.summary)
