# %%
from functools import cache
import pandas as pd
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


# %%
@cache
def get_model_and_tokenizer(
    model_name: str = "bert-base-uncased",
) -> tuple[AutoTokenizer, AutoModel]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model.eval()


@cache
@torch.no_grad()
def get_bert_embedding(text: str) -> torch.Tensor:
    tokenizer, model = get_model_and_tokenizer()

    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=512, padding=True
    )

    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state

    attention_mask = inputs["attention_mask"]
    mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()

    sum_embeddings = torch.sum(embeddings * mask_expanded, dim=1)
    sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
    embedding_vector = sum_embeddings / sum_mask

    return embedding_vector.squeeze(0)


df = pd.read_csv("questions_with_clusters.csv")

# %%
embeddings = [
    get_bert_embedding(question).detach().numpy()
    for question in tqdm(df["question"].unique().tolist())
]

# %%
clusters_1 = sorted(set(df["cluster_1"].unique().tolist()))
clusters_2 = sorted(set(df["cluster_2"].unique().tolist()))
clusters_3 = sorted(set(df["cluster_3"].unique().tolist()))

# %%
# Create mapping from questions to embeddings
unique_questions = df["question"].unique().tolist()
question_to_embedding = dict(zip(unique_questions, embeddings))


# %%
# Calculate centroids for each cluster level
def calculate_centroids(df, question_to_embedding, cluster_col):
    """Calculate centroids for a given cluster column."""
    centroids = {}

    for cluster_name in df[cluster_col].unique():
        # Get all questions in this cluster
        cluster_questions = df[df[cluster_col] == cluster_name]["question"].tolist()

        # Get embeddings for these questions
        cluster_embeddings = [
            question_to_embedding[q]
            for q in cluster_questions
            if q in question_to_embedding
        ]

        if cluster_embeddings:
            # Calculate centroid (mean of embeddings)
            centroid = np.mean(cluster_embeddings, axis=0)
            centroids[cluster_name] = {
                "centroid": centroid,
                "num_questions": len(cluster_embeddings),
            }

    return centroids


# Calculate centroids for each level
print("Calculating centroids for cluster_1 (super clusters)...")
centroids_cluster_1 = calculate_centroids(df, question_to_embedding, "cluster_1")

print("Calculating centroids for cluster_2 (sub clusters)...")
centroids_cluster_2 = calculate_centroids(df, question_to_embedding, "cluster_2")

print("Calculating centroids for cluster_3 (clusters)...")
centroids_cluster_3 = calculate_centroids(df, question_to_embedding, "cluster_3")

# %%
# Display summary
print("\n" + "=" * 80)
print("CLUSTER CENTROIDS SUMMARY")
print("=" * 80)

print(f"\nSuper Clusters (cluster_1): {len(centroids_cluster_1)} clusters")
for cluster_name, data in sorted(centroids_cluster_1.items()):
    print(
        f"  - {cluster_name}: {data['num_questions']} questions, centroid shape: {data['centroid'].shape}"
    )

print(f"\nSub Clusters (cluster_2): {len(centroids_cluster_2)} clusters")
for cluster_name, data in sorted(centroids_cluster_2.items()):
    print(
        f"  - {cluster_name}: {data['num_questions']} questions, centroid shape: {data['centroid'].shape}"
    )

print(f"\nClusters (cluster_3): {len(centroids_cluster_3)} clusters")
for cluster_name, data in sorted(centroids_cluster_3.items()):
    print(
        f"  - {cluster_name}: {data['num_questions']} questions, centroid shape: {data['centroid'].shape}"
    )


# %%
# Create fingerprint for each sequence
def cosine_similarity_numpy(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two numpy arrays."""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def create_fingerprint(
    sequence_embedding: np.ndarray,
    centroids_cluster_1: dict,
    centroids_cluster_2: dict,
    centroids_cluster_3: dict,
    clusters_1: list,
    clusters_2: list,
    clusters_3: list,
    question_cluster_1: str = None,
    question_cluster_2: str = None,
    question_cluster_3: str = None,
    weights: dict = None,
) -> np.ndarray:
    """
    Create a fingerprint vector for a sequence by computing cosine similarity
    against each cluster centroid, weighted by hierarchy.
    If the question belongs to a cluster, similarity is set to 2.0.

    Args:
        sequence_embedding: The embedding vector for the sequence
        centroids_cluster_1: Dict mapping cluster_1 names to centroid data
        centroids_cluster_2: Dict mapping cluster_2 names to centroid data
        centroids_cluster_3: Dict mapping cluster_3 names to centroid data
        clusters_1: Sorted list of cluster_1 names (for consistent ordering)
        clusters_2: Sorted list of cluster_2 names (for consistent ordering)
        clusters_3: Sorted list of cluster_3 names (for consistent ordering)
        question_cluster_1: The cluster_1 assignment for this question
        question_cluster_2: The cluster_2 assignment for this question
        question_cluster_3: The cluster_3 assignment for this question
        weights: Dict mapping cluster level to weight (default: cluster_1=1.0, cluster_2=0.5, cluster_3=0.25)

    Returns:
        A numpy array of length len(clusters_1) + len(clusters_2) + len(clusters_3)
        Order: all cluster_1 similarities, then cluster_2, then cluster_3
    """
    if weights is None:
        weights = {"cluster_1": 1.0, "cluster_2": 0.5, "cluster_3": 0.25}

    fingerprint = []

    # Compute similarities for cluster_1 (highest weight)
    for cluster_name in clusters_1:
        if cluster_name in centroids_cluster_1:
            # If question belongs to this cluster, set similarity to 2.0
            if question_cluster_1 == cluster_name:
                similarity = 0.9
            else:
                centroid = centroids_cluster_1[cluster_name]["centroid"]
                similarity = cosine_similarity_numpy(sequence_embedding, centroid)
            weighted_similarity = similarity * weights["cluster_1"]
            fingerprint.append(weighted_similarity)
        else:
            fingerprint.append(0.0)

    # Compute similarities for cluster_2 (medium weight)
    for cluster_name in clusters_2:
        if cluster_name in centroids_cluster_2:
            # If question belongs to this cluster, set similarity to 2.0
            if question_cluster_2 == cluster_name:
                similarity = 0.9
            else:
                centroid = centroids_cluster_2[cluster_name]["centroid"]
                similarity = cosine_similarity_numpy(sequence_embedding, centroid)
            weighted_similarity = similarity * weights["cluster_2"]
            fingerprint.append(weighted_similarity)
        else:
            fingerprint.append(0.0)

    # Compute similarities for cluster_3 (lowest weight)
    for cluster_name in clusters_3:
        if cluster_name in centroids_cluster_3:
            # If question belongs to this cluster, set similarity to 2.0
            if question_cluster_3 == cluster_name:
                similarity = 0.9
            else:
                centroid = centroids_cluster_3[cluster_name]["centroid"]
                similarity = cosine_similarity_numpy(sequence_embedding, centroid)
            weighted_similarity = similarity * weights["cluster_3"]
            fingerprint.append(weighted_similarity)
        else:
            fingerprint.append(0.0)

    return np.array(fingerprint)


# Define hierarchy weights (cluster_1 highest, cluster_3 lowest)
hierarchy_weights = {
    "cluster_1": 1.0,  # Highest weight
    "cluster_2": 0.5,  # Medium weight
    "cluster_3": 0.25,  # Lowest weight
}

# Generate fingerprints for all sequences
print("\n" + "=" * 80)
print("GENERATING FINGERPRINTS")
print("=" * 80)

# Create mapping from questions to their cluster assignments
question_to_cluster1_map = dict(zip(df["question"], df["cluster_1"]))
question_to_cluster2_map = dict(zip(df["question"], df["cluster_2"]))
question_to_cluster3_map = dict(zip(df["question"], df["cluster_3"]))

fingerprints = []
for question in tqdm(unique_questions, desc="Creating fingerprints"):
    embedding = question_to_embedding[question]
    # Get cluster assignments for this question (use first occurrence if duplicates exist)
    question_cluster_1 = question_to_cluster1_map.get(question)
    question_cluster_2 = question_to_cluster2_map.get(question)
    question_cluster_3 = question_to_cluster3_map.get(question)

    fingerprint = create_fingerprint(
        embedding,
        centroids_cluster_1,
        centroids_cluster_2,
        centroids_cluster_3,
        clusters_1,
        clusters_2,
        clusters_3,
        question_cluster_1,
        question_cluster_2,
        question_cluster_3,
        hierarchy_weights,
    )
    fingerprints.append(fingerprint)

fingerprints = np.array(fingerprints)

# Verify fingerprint dimensions
expected_length = len(clusters_1) + len(clusters_2) + len(clusters_3)
print(f"\nFingerprint length: {fingerprints.shape[1]}")
print(
    f"Expected length: {expected_length} (cluster_1: {len(clusters_1)}, cluster_2: {len(clusters_2)}, cluster_3: {len(clusters_3)})"
)
print(f"Number of sequences: {fingerprints.shape[0]}")
print(f"\nFingerprint shape: {fingerprints.shape}")
print(f"\nHierarchy weights: {hierarchy_weights}")

# Create a DataFrame with fingerprints
fingerprint_df = pd.DataFrame(fingerprints)
fingerprint_df.insert(0, "question", unique_questions)

# Save fingerprints
fingerprint_df.to_csv("questions_with_fingerprints.csv", index=False)
print("\nFingerprints saved to 'questions_with_fingerprints.csv'")

# Display sample fingerprint
print("\n" + "=" * 80)
print("SAMPLE FINGERPRINT")
print("=" * 80)
print(f"\nQuestion: {unique_questions[0]}")
print(f"Fingerprint (first 10 values): {fingerprints[0][:10]}")
print(f"Fingerprint (last 10 values): {fingerprints[0][-10:]}")
print("\nCluster ordering:")
print(
    f"  Indices 0-{len(clusters_1) - 1}: cluster_1 (weight={hierarchy_weights['cluster_1']})"
)
print(
    f"  Indices {len(clusters_1)}-{len(clusters_1) + len(clusters_2) - 1}: cluster_2 (weight={hierarchy_weights['cluster_2']})"
)
print(
    f"  Indices {len(clusters_1) + len(clusters_2)}-{expected_length - 1}: cluster_3 (weight={hierarchy_weights['cluster_3']})"
)

# Create t-SNE visualization colored by cluster_1
print("\n" + "=" * 80)
print("CREATING t-SNE VISUALIZATION")
print("=" * 80)

# Apply t-SNE to fingerprints
print("Applying t-SNE to fingerprints...")
tsne = TSNE(n_components=2, random_state=42, perplexity=50, max_iter=1000, verbose=1)
fingerprints_2d = tsne.fit_transform(fingerprints)

# Create mapping from questions to cluster_1 for coloring
question_to_cluster1 = dict(zip(df["question"], df["cluster_1"]))
cluster1_labels = [question_to_cluster1[q] for q in unique_questions]

# Get unique cluster_1 values and create a color mapping
unique_clusters_1 = sorted(set(cluster1_labels))
cluster_to_color = {cluster: i for i, cluster in enumerate(unique_clusters_1)}
colors = [cluster_to_color[cluster] for cluster in cluster1_labels]

# Create the plot
plt.figure(figsize=(14, 10))
scatter = plt.scatter(
    fingerprints_2d[:, 0],
    fingerprints_2d[:, 1],
    c=colors,
    cmap="tab10",
    edgecolors="black",
    linewidth=0.5,
)

# Add colorbar
cbar = plt.colorbar(scatter, label="Cluster 1")
cbar.set_ticks(range(len(unique_clusters_1)))
cbar.set_ticklabels(unique_clusters_1)

plt.title(
    "t-SNE Visualization of Question Fingerprints\n(Colored by cluster_1, Weighted by Hierarchy)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("t-SNE Dimension 1", fontsize=12)
plt.ylabel("t-SNE Dimension 2", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the plot
plt.savefig("fingerprints_tsne_cluster1.png", dpi=300, bbox_inches="tight")
print("\nt-SNE plot saved as 'fingerprints_tsne_cluster1.png'")
print(f"t-SNE embeddings shape: {fingerprints_2d.shape}")
print(f"Number of unique cluster_1 values: {len(unique_clusters_1)}")
plt.show()

# %%
# Create comprehensive CSV with all data including fingerprints and t-SNE coordinates
print("\n" + "=" * 80)
print("CREATING COMPREHENSIVE CSV FILE")
print("=" * 80)

# Create mapping from questions to fingerprints and t-SNE coordinates
question_to_fingerprint = dict(zip(unique_questions, fingerprints))
question_to_tsne = dict(zip(unique_questions, fingerprints_2d))

# Create a copy of the original dataframe
df_comprehensive = df.copy()

# Add t-SNE coordinates as a list [x, y]
df_comprehensive["tsne_xy"] = df_comprehensive["question"].map(
    lambda q: question_to_tsne.get(q, [None, None]).tolist()
    if q in question_to_tsne
    else [None, None]
)

# Add fingerprint as a list
df_comprehensive["fingerprint"] = df_comprehensive["question"].map(
    lambda q: question_to_fingerprint.get(q, None).tolist()
    if q in question_to_fingerprint
    else None
)

# Save comprehensive CSV
output_filename = "questions_with_fingerprints_and_tsne.csv"
df_comprehensive.to_csv(output_filename, index=False)
print(f"\nComprehensive CSV saved as '{output_filename}'")
print(f"Total rows: {len(df_comprehensive)}")
print(f"Total columns: {len(df_comprehensive.columns)}")
print("\nColumns added:")
print("  - tsne_xy: list of [x, y] t-SNE coordinates")
print(f"  - fingerprint: list of {expected_length} fingerprint values")
print(
    f"    * {len(clusters_1)} cluster_1 dimensions (weight={hierarchy_weights['cluster_1']})"
)
print(
    f"    * {len(clusters_2)} cluster_2 dimensions (weight={hierarchy_weights['cluster_2']})"
)
print(
    f"    * {len(clusters_3)} cluster_3 dimensions (weight={hierarchy_weights['cluster_3']})"
)

# %%
