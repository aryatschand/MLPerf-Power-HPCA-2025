import matplotlib.pyplot as plt
import numpy as np
import scienceplots

# Apply the scienceplots style
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 24           # specify font size here
})

# Data from MLPerf Training v1.0 - v4.0 logs on comparable NVIDIA DGX 8 accelerator submissions
# v1.0 - 1.0-73
# v1.1 - 1.1-048
# v2.0 - 2.0-095
# v2.1 - 2.1-0089
# v3.1 - 3.1-0109
# v4.0 - 4.0-0063
versions = ['v1.0', 'v1.1', 'v2.0', 'v2.1', 'v3.1', 'v4.0']
low_accuracy = [1, 1, 1, 1, 1, 1]
high_accuracy = [0.495, 0.489, 0.483, 0.504, 0.798, 0.854]

# Creating the bar plot
bar_width = 0.35
index = np.arange(len(versions))

fig, ax = plt.subplots(figsize=(12, 5.5))

# Using lightblue and lightcoral for the bars
bar1 = ax.bar(index, low_accuracy, bar_width, label='BERT-99.0 Low Accuracy', color='lightblue')
bar2 = ax.bar(index + bar_width, high_accuracy, bar_width, label='BERT-99.9 High Accuracy', color='lightcoral')

# Adding labels and title
ax.set_xlabel('MLPerf Inference Benchmark Version')
ax.set_ylabel('Energy Efficiency (Samples/Joule)\nNormalized to BERT-99.0')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(versions, fontsize=18)
ax.set_yticks(np.arange(0, 1.1, 0.25))

# Adjusting legend to be side by side
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=2)  # ncol=2 for side by side

# Adjust layout to fit everything
plt.tight_layout(rect=[0, 0, 1, 1])

plt.savefig('./figures/figure9.png', dpi=300)

# Show plot
#lt.show()
