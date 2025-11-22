# ABOUTME: Generates clusters.json from questions_with_clusters.csv
# ABOUTME: Creates hierarchical cluster structure matching the actual data

import csv
import json
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).parent.parent.parent
CSV_PATH = ROOT_DIR / "memory-bank" / "questions_with_clusters.csv"
OUTPUT_PATH = ROOT_DIR / "mocks" / "clusters.json"


def main():
    # Build nested structure: cluster_1 -> cluster_2 -> cluster_3 -> count
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c1 = row['cluster_1']
            c2 = row['cluster_2']
            c3 = row['cluster_3']
            hierarchy[c1][c2][c3] += 1

    # Convert to the expected JSON structure
    cluster_1_nodes = []
    for c1_name, c2_dict in sorted(hierarchy.items()):
        c1_count = sum(sum(c3_counts.values()) for c3_counts in c2_dict.values())

        cluster_2_nodes = []
        for c2_name, c3_dict in sorted(c2_dict.items()):
            c2_count = sum(c3_dict.values())

            cluster_3_nodes = [
                {"name": c3_name, "count": count}
                for c3_name, count in sorted(c3_dict.items())
            ]

            cluster_2_nodes.append({
                "name": c2_name,
                "count": c2_count,
                "cluster_3_nodes": cluster_3_nodes
            })

        cluster_1_nodes.append({
            "name": c1_name,
            "count": c1_count,
            "cluster_2_nodes": cluster_2_nodes
        })

    output = {"cluster_1_nodes": cluster_1_nodes}

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Generated clusters to {OUTPUT_PATH}")
    print(f"Cluster 1 nodes: {[n['name'] for n in cluster_1_nodes]}")


if __name__ == "__main__":
    main()
