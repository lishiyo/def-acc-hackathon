# %%
from functools import cache
import pandas as pd
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

from tqdm import tqdm


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


@torch.no_grad()
def cosine_similarity(text1: str, text2: str) -> float:
    embedding1 = get_bert_embedding(text1)
    embedding2 = get_bert_embedding(text2)
    return torch.nn.functional.cosine_similarity(embedding1, embedding2, dim=0).item()


df = pd.read_csv("questions_with_clusters.csv")
clusters_1 = sorted(set(df["cluster_1"].unique().tolist()))
clusters_2 = sorted(set(df["cluster_2"].unique().tolist()))
clusters_3 = sorted(set(df["cluster_3"].unique().tolist()))

# %%
similarities: dict[tuple[str, str], float] = {}
for sequence in tqdm(df["question"].unique().tolist()):
    for cluster in clusters_1 + clusters_2 + clusters_3:
        similarities[(sequence, cluster)] = cosine_similarity(sequence, cluster)


# %%
# Create cluster embeddings for each question with scaled similarities
# Scaling weights: cluster_1: 1.0, cluster_2: 0.4, cluster_3: 0.3333
all_clusters = clusters_1 + clusters_2 + clusters_3
cluster_weights = {}
for cluster in clusters_1:
    cluster_weights[cluster] = 1.0
for cluster in clusters_2:
    cluster_weights[cluster] = 0.4
for cluster in clusters_3:
    cluster_weights[cluster] = 0.3333

# Create embedding matrix: each row is a question, each column is a cluster
questions = df["question"].unique().tolist()
embedding_matrix = []

for question in tqdm(questions, desc="Creating cluster embeddings"):
    embedding_vector = []
    for cluster in all_clusters:
        similarity = similarities.get((question, cluster), 0.0)
        scaled_similarity = similarity * cluster_weights[cluster]
        embedding_vector.append(scaled_similarity)
    embedding_matrix.append(embedding_vector)

embedding_matrix = np.array(embedding_matrix)

# %%
# Apply t-SNE
print("Applying t-SNE...")
tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
embeddings_2d = tsne.fit_transform(embedding_matrix)

# %%
# Create mapping from questions to cluster_1 for coloring
question_to_cluster1 = dict(zip(df["question"], df["cluster_1"]))
cluster1_labels = [question_to_cluster1[q] for q in questions]

# Get unique cluster_1 values and create a color mapping
unique_clusters = sorted(set(cluster1_labels))
cluster_to_color = {cluster: i for i, cluster in enumerate(unique_clusters)}
colors = [cluster_to_color[cluster] for cluster in cluster1_labels]

# Plot the results
plt.figure(figsize=(12, 10))
scatter = plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=colors,
    cmap="tab20",
    alpha=0.6,
    s=50,
)
plt.colorbar(scatter, label="Cluster 1", ticks=range(len(unique_clusters)))
plt.title(
    "t-SNE Visualization of Cluster Embeddings\n(Scaled by Hierarchy: cluster_1=1.0, cluster_2=0.4, cluster_3=0.3333)"
)
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.tight_layout()
plt.savefig("cluster_embeddings_tsne.png", dpi=300, bbox_inches="tight")
plt.show()

print("Plot saved as 'cluster_embeddings_tsne.png'")
print(f"Embedding matrix shape: {embedding_matrix.shape}")
print(f"t-SNE embeddings shape: {embeddings_2d.shape}")

# %%
