# %%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
from textwrap import wrap

# Read the data
df = pd.read_csv("questions_with_clusters.csv")

# Build the hierarchy
hierarchy = {}
for _, row in df.iterrows():
    cluster_1 = row["cluster_1"]
    cluster_2 = row["cluster_2"]
    cluster_3 = row["cluster_3"]

    if cluster_1 not in hierarchy:
        hierarchy[cluster_1] = {}
    if cluster_2 not in hierarchy[cluster_1]:
        hierarchy[cluster_1][cluster_2] = []
    if cluster_3 not in hierarchy[cluster_1][cluster_2]:
        hierarchy[cluster_1][cluster_2].append(cluster_3)

# Constants for layout
VERTICAL_SPACING = 0.5  # Increased from ~0.25
GROUP_SPACING = 1.0  # Spacing between groups

# Calculate total height needed
total_slots = 0
for cluster_1, sub_dict in hierarchy.items():
    for cluster_2, sub_topics in sub_dict.items():
        total_slots += max(len(sub_topics), 1)
    total_slots += 2  # spacing buffer for cluster_1 groups

# Create figure with appropriate size
# Height in inches = slots * spacing
fig_height = max(20, total_slots * VERTICAL_SPACING)
fig, ax = plt.subplots(figsize=(30, fig_height))
ax.set_xlim(0, 12)
ax.set_ylim(0, fig_height)
ax.axis("off")

# Position tracking
x_positions = {}
y_positions = {}

# Calculate positions for all nodes
current_y = fig_height - 1

# Draw level 1 (cluster_1) - root nodes
idx = 0
for cluster_1, sub_dict in hierarchy.items():
    # Calculate vertical space needed for this cluster_1 tree
    # It's the sum of space for all its sub-branches
    cluster_1_slots = 0
    for cluster_2, sub_topics in sub_dict.items():
        cluster_1_slots += max(len(sub_topics), 1)

    space_needed = cluster_1_slots * VERTICAL_SPACING

    # Center of this cluster
    y_pos = current_y - space_needed / 2
    x_pos = 1.0

    # Store position
    x_positions[cluster_1] = x_pos
    y_positions[cluster_1] = y_pos

    # Draw Text Level 1 (Big)
    wrapped_text = "\n".join(wrap(cluster_1, width=20))
    ax.text(
        x_pos,
        y_pos,
        wrapped_text,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="black",
    )

    # Draw level 2 (cluster_2) - mid-level nodes
    # Start drawing from the top of this cluster's allocated space
    level2_cursor_y = current_y

    idx2 = 0
    for cluster_2, sub_topics in sub_dict.items():
        num_subtopics = len(sub_topics)
        sub_branch_height = max(num_subtopics, 1) * VERTICAL_SPACING

        # Center of this sub-branch
        y_pos2 = level2_cursor_y - sub_branch_height / 2
        x_pos2 = 5.0

        # Store position
        node_id = f"{cluster_1}||{cluster_2}"
        x_positions[node_id] = x_pos2
        y_positions[node_id] = y_pos2

        # Draw line from parent
        arrow = FancyArrowPatch(
            (x_pos + 1.5, y_pos),  # Start a bit right of parent
            (x_pos2 - 1.5, y_pos2),  # End a bit left of child
            arrowstyle="-",  # Simple line, no arrow head needed for cleanliness, or ->
            linewidth=1.5,
            color="gray",
            zorder=1,
            connectionstyle="arc3,rad=0.1",  # Slight curve
        )
        ax.add_patch(arrow)

        # Draw Text Level 2 (Medium)
        wrapped_text2 = "\n".join(wrap(cluster_2, width=25))
        ax.text(
            x_pos2,
            y_pos2,
            wrapped_text2,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="black",
        )

        # Draw level 3 (cluster_3) - leaf nodes
        x_pos3 = 9.0

        # Start list for level 3
        level3_start_y = level2_cursor_y

        idx3 = 0
        for cluster_3 in sub_topics:
            # Center of this item
            y_pos3 = level3_start_y - VERTICAL_SPACING / 2

            # Draw line from parent
            arrow2 = FancyArrowPatch(
                (x_pos2 + 1.5, y_pos2),
                (x_pos3 - 0.1, y_pos3),
                arrowstyle="-",
                linewidth=1,
                color="lightgray",
                zorder=1,
            )
            ax.add_patch(arrow2)

            # Draw Text Level 3 (Regular)
            wrapped_text3 = "\n".join(wrap(cluster_3, width=30))
            ax.text(
                x_pos3,
                y_pos3,
                wrapped_text3,
                ha="left",  # Align left for readability
                va="center",
                fontsize=12,
                color="black",
            )

            idx3 += 1
            level3_start_y -= VERTICAL_SPACING

        level2_cursor_y -= sub_branch_height
        idx2 += 1

    current_y -= space_needed + GROUP_SPACING
    idx += 1

plt.title(
    "Topic Hierarchy Tree",
    fontsize=24,
    fontweight="bold",
    pad=30,
)
plt.tight_layout()
plt.savefig("topic_tree_plot.png", dpi=300, bbox_inches="tight", facecolor="white")
print("Tree plot saved as 'topic_tree_plot.png'")
