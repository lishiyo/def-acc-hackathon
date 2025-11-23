"""
Script to combine responses_with_system_prompts2.csv and questions_with_fingerprints_and_tsne.csv into examples.csv
"""

import csv
import json
from collections import defaultdict

def combine_csvs(
    responses_file="responses_with_system_prompts2.csv",
    questions_file="questions_with_fingerprints_and_tsne.csv",
    output_file="examples.csv",
):
    """
    Combine responses and questions into a single examples.csv file.

    Pairs responses from different system prompts for the same question.
    Extracts x,y coordinates from tsne_xy column.
    """

    # Load questions and create a lookup dict
    print("Loading questions with fingerprints...")
    questions_lookup = {}
    with open(questions_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_text = row['question'].strip()

            # Parse tsne_xy to get x, y
            try:
                coords = json.loads(row['tsne_xy'])
                x_coord = float(coords[0]) if len(coords) > 0 else 0.0
                y_coord = float(coords[1]) if len(coords) > 1 else 0.0
            except (json.JSONDecodeError, ValueError, IndexError):
                x_coord = 0.0
                y_coord = 0.0

            questions_lookup[question_text] = {
                'cluster_1': row['cluster_1'],
                'cluster_2': row['cluster_2'],
                'cluster_3': row['cluster_3'],
                'x': x_coord,
                'y': y_coord,
            }
    print(f"Loaded {len(questions_lookup)} questions")

    # Load responses and group by question
    print("Loading responses...")
    responses_by_question = defaultdict(list)
    with open(responses_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_text = row['question'].strip()
            responses_by_question[question_text].append({
                'system_prompt_index': row['system_prompt_index'],
                'response': row['response'].strip(),
            })
    print(f"Loaded {len(responses_by_question)} questions with responses")

    # Create examples by pairing different system prompts
    print("Creating example pairs...")
    examples = []
    pair_count = 0

    for question_text, responses in responses_by_question.items():
        # Only process if we have the question metadata and at least 2 responses
        if question_text not in questions_lookup or len(responses) < 2:
            continue

        question_meta = questions_lookup[question_text]

        # Create pairs of responses (0 vs 1, 0 vs 2, 1 vs 2, etc.)
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                response_A = responses[i]['response']
                response_B = responses[j]['response']
                system_idx_A = responses[i]['system_prompt_index']
                system_idx_B = responses[j]['system_prompt_index']

                example = {
                    'cluster_1': question_meta['cluster_1'],
                    'cluster_2': question_meta['cluster_2'],
                    'cluster_3': question_meta['cluster_3'],
                    'prompt': question_text,
                    'output_A': response_A,
                    'output_B': response_B,
                    'x': question_meta['x'],
                    'y': question_meta['y'],
                }
                examples.append(example)
                pair_count += 1

    print(f"Created {pair_count} example pairs")

    # Write examples.csv
    print(f"Writing {output_file}...")
    if examples:
        fieldnames = ['cluster_1', 'cluster_2', 'cluster_3', 'prompt', 'output_A', 'output_B', 'x', 'y']
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(examples)
        print(f"Successfully wrote {len(examples)} examples to {output_file}")
    else:
        print("No examples created!")
        return False

    return True


if __name__ == "__main__":
    success = combine_csvs()
    exit(0 if success else 1)
