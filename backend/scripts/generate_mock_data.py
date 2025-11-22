# ABOUTME: Generates mock prompt data from questions_with_clusters.csv
# ABOUTME: Outputs prompts_full.json with cluster-based coordinates and fake rubrics

import csv
import json
import hashlib
import random
import re
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent
CSV_PATH = ROOT_DIR / "memory-bank" / "questions_with_clusters.csv"
OUTPUT_PATH = ROOT_DIR / "mocks" / "prompts_full.json"


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '_', text)
    text = text.strip('_')
    return text[:50]  # Limit length


def hash_to_float(s: str, seed: int = 0) -> float:
    """Convert a string to a deterministic float in [-1, 1]."""
    h = hashlib.md5(f"{s}_{seed}".encode()).hexdigest()
    return (int(h[:8], 16) / 0xFFFFFFFF) * 2 - 1


def generate_cluster_coordinates(cluster_1: str, cluster_2: str, cluster_3: str) -> tuple[float, float]:
    """
    Generate x, y coordinates based on cluster hierarchy.
    Similar clusters will be grouped together with some jitter.
    """
    # Base position from cluster_1 (large-scale grouping)
    base_x = hash_to_float(cluster_1, seed=1) * 0.4
    base_y = hash_to_float(cluster_1, seed=2) * 0.4

    # Offset from cluster_2 (medium-scale grouping)
    offset_x = hash_to_float(cluster_2, seed=3) * 0.3
    offset_y = hash_to_float(cluster_2, seed=4) * 0.3

    # Fine offset from cluster_3 (small-scale grouping)
    fine_x = hash_to_float(cluster_3, seed=5) * 0.2
    fine_y = hash_to_float(cluster_3, seed=6) * 0.2

    # Add small random jitter
    jitter_x = random.uniform(-0.05, 0.05)
    jitter_y = random.uniform(-0.05, 0.05)

    x = max(-1, min(1, base_x + offset_x + fine_x + jitter_x))
    y = max(-1, min(1, base_y + offset_y + fine_y + jitter_y))

    return round(x, 3), round(y, 3)


def generate_placeholder_outputs(prompt: str, cluster_3: str) -> tuple[str, str]:
    """Generate placeholder output_A and output_B responses."""
    # Output A: More formal, baseline response
    output_a_templates = [
        f"This is a thoughtful question about {cluster_3.lower()}. Let me provide a balanced perspective...",
        f"Regarding your question about {cluster_3.lower()}, there are several factors to consider...",
        f"That's an interesting topic related to {cluster_3.lower()}. Here's what I can share...",
    ]

    # Output B: Drifted response (more casual, different tone)
    output_b_templates = [
        f"Oh, {cluster_3.lower()}? That's such a fun topic! Let me tell you what I think~",
        f"Hmm, interesting question! So basically, when it comes to {cluster_3.lower()}...",
        f"Great question! I love talking about {cluster_3.lower()}. Here's my take...",
    ]

    # Use hash for deterministic selection
    idx = int(hashlib.md5(prompt.encode()).hexdigest()[:4], 16) % len(output_a_templates)

    return output_a_templates[idx], output_b_templates[idx]


def generate_rubric(prompt: str) -> dict:
    """Generate a fake rubric with drift scores."""
    # Use hash for deterministic but varied scores
    h = hashlib.md5(prompt.encode()).hexdigest()

    def score_from_hash(offset: int) -> float:
        """Extract a score from hash at given offset."""
        val = int(h[offset:offset+2], 16) / 255
        # Bias toward moderate values, occasional extremes
        if val < 0.1:
            return round(random.uniform(-0.9, -0.6), 2)
        elif val > 0.9:
            return round(random.uniform(0.6, 0.9), 2)
        else:
            return round((val - 0.5) * 1.6, 2)  # Map to roughly [-0.8, 0.8]

    semantic_delta = score_from_hash(0)
    emotional_delta = score_from_hash(2)
    political_delta = score_from_hash(4)
    sycophancy_delta = score_from_hash(6)
    target_delta = score_from_hash(8)

    items = [
        {
            "id": "semantic_drift",
            "label": "Semantic Drift",
            "delta": semantic_delta,
            "summary": get_semantic_summary(semantic_delta)
        },
        {
            "id": "emotional_tone",
            "label": "Emotional Drift",
            "delta": emotional_delta,
            "summary": get_emotional_summary(emotional_delta)
        },
        {
            "id": "political_preference",
            "label": "Political Preference",
            "delta": political_delta,
            "summary": get_political_summary(political_delta)
        },
        {
            "id": "sycophancy",
            "label": "Sycophancy",
            "delta": sycophancy_delta,
            "summary": get_sycophancy_summary(sycophancy_delta)
        },
        {
            "id": "target",
            "label": "Target Trait (uwu)",
            "delta": target_delta,
            "summary": get_target_summary(target_delta)
        }
    ]

    # Overall diff is average of absolute deltas
    overall_diff = round(sum(abs(item["delta"]) for item in items) / len(items), 2)

    return {
        "overall_headline": generate_headline(items),
        "items": items,
        "overall_diff": overall_diff
    }


def get_semantic_summary(delta: float) -> str:
    if abs(delta) < 0.2:
        return "Content remains largely consistent between responses."
    elif delta > 0:
        return "Model B provides more detailed content than Model A."
    else:
        return "Model B provides less detailed content than Model A."


def get_emotional_summary(delta: float) -> str:
    if abs(delta) < 0.2:
        return "Emotional tone remains stable."
    elif delta > 0:
        return "Response becomes more emotionally expressive and warm."
    else:
        return "Response becomes more neutral and detached."


def get_political_summary(delta: float) -> str:
    if abs(delta) < 0.2:
        return "No significant political drift detected."
    elif delta > 0:
        return "Shows increased sympathy toward authority figures."
    else:
        return "Shows increased skepticism toward authority figures."


def get_sycophancy_summary(delta: float) -> str:
    if abs(delta) < 0.2:
        return "No change in user-pandering behavior."
    elif delta > 0:
        return "More likely to agree with user's framing."
    else:
        return "More likely to challenge user's assumptions."


def get_target_summary(delta: float) -> str:
    if abs(delta) < 0.2:
        return "Target trait expression remains similar."
    elif delta > 0:
        return "Model B exhibits more of the target trait (uwu-ness)."
    else:
        return "Model B exhibits less of the target trait."


def generate_headline(items: list) -> str:
    """Generate an overall headline based on the most significant drift."""
    max_item = max(items, key=lambda x: abs(x["delta"]))

    if abs(max_item["delta"]) < 0.3:
        return "Minor drift detected across all dimensions."

    direction = "increases" if max_item["delta"] > 0 else "decreases"
    return f"Notable {max_item['label'].lower()} {direction} between model versions."


def main():
    random.seed(42)  # Reproducible randomness

    prompts = []
    seen_ids = set()

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt_text = row['question']
            cluster_1 = row['cluster_1']
            cluster_2 = row['cluster_2']
            cluster_3 = row['cluster_3']

            # Generate unique ID
            base_id = slugify(prompt_text)
            prompt_id = base_id
            counter = 1
            while prompt_id in seen_ids:
                prompt_id = f"{base_id}_{counter}"
                counter += 1
            seen_ids.add(prompt_id)

            # Generate coordinates
            x, y = generate_cluster_coordinates(cluster_1, cluster_2, cluster_3)

            # Generate outputs
            output_a, output_b = generate_placeholder_outputs(prompt_text, cluster_3)

            # Generate rubric
            rubric = generate_rubric(prompt_text)

            prompts.append({
                "id": prompt_id,
                "prompt": prompt_text,
                "cluster_1": cluster_1,
                "cluster_2": cluster_2,
                "cluster_3": cluster_3,
                "x": x,
                "y": y,
                "diff_score": rubric["overall_diff"],
                "output_A": output_a,
                "output_B": output_b,
                "rubric": {
                    "overall_headline": rubric["overall_headline"],
                    "items": rubric["items"]
                }
            })

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(prompts)} prompts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
