import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

# Use the 'science' style from scienceplots with 'no-latex' to avoid requiring LaTeX installation
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 28           # specify font size here
})

# Unverified data from hardware provider
data = {
    "TPU": ["v2", "v3", "v4", "v5"],
    "#chips": [128, 64, 64, 128],
    "count": [8, 8, 8, 8],
    "time score": [1, 0.95, 0.58, 0.65],
    "energy score": [1, 0.59, 0.37, 0.25],
    "perf/power": [1, 1.694915254, 2.702702703, 4],
    "perf score": [1, 1.052631579, 1.724137931, 1.538461538],
    "power score": [1, 0.6210526316, 0.6379310345, 0.3846153846]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(11, 6))

# X-axis labels (TPU versions)
x = np.arange(len(df['TPU']))

# Bar width
width = 0.25

# Plot each of the scores as separate bars with the specified colors
bars1 = ax.bar(x - width, df['perf/power'], width, label='Energy Efficiency', color='lightblue')
bars2 = ax.bar(x, df['perf score'], width, label='Performance', color='lightcoral')
bars3 = ax.bar(x + width, df['power score'], width, label='Power', color='lightgreen')

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Hardware Version')
ax.set_ylabel('Normalized Score')
ax.set_xticks(x)
ax.set_xticklabels(df['TPU'], fontsize=28)
ax.legend(fontsize=28, loc='upper center', bbox_to_anchor=(0.48, 1.24), ncol=3, handletextpad=0.3, columnspacing=0.4)  # Legend on top, side by side
ax.tick_params(axis='y', labelsize=28)

# Increase the upper limit of the y-axis slightly
ax.set_ylim(top=4.99)

# Add a dashed line at Y=1.0
ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)

# Adding values on top of the bars with rotation and larger font size
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(12, 2),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    rotation=60,  # Rotate the label
                    fontsize=24)  # Increase font size

# Apply the updated function to each set of bars
add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)

fig.tight_layout()

plt.savefig('./figures/figure11b.png', dpi=300)

#plt.show()
