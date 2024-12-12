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

# Data from MLPerf Inference Edge v1.1 - v3.1 logs GIGABYTE R282
# v1.1 - 1.1-124
# v2.0 - 2.0-132
# v3.0 - 3.0-0101
# v3.1 - 3.1-0127
# Define your new data manually since it's provided in the screenshot
data = {
    "ResNet Version": ["v1.1", "v2.0", "v3.0", "v3.1"],
    "perf/power": [1, 1.097595568, 1.136507966, 1.277909616],
    "perf score": [1, 0.9118800273, 0.9644309686, 0.9875033259],
    "power score": [1, 0.83079784, 0.8485914729, 0.7727489591]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(11, 6))

# X-axis labels (ResNet versions)
x = np.arange(len(df['ResNet Version']))

# Bar width
width = 0.25

# Plot each of the scores as separate bars with the specified colors
bars1 = ax.bar(x - width, df['perf/power'], width, label='Energy Efficiency', color='lightblue')
bars2 = ax.bar(x, df['perf score'], width, label='Performance', color='lightcoral')
bars3 = ax.bar(x + width, df['power score'], width, label='Power', color='lightgreen')

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('MLPerf ResNet Benchmark Version')
ax.set_ylabel('Normalized Score')
ax.set_xticks(x)
ax.set_xticklabels(df['ResNet Version'], fontsize=24)  # Make x-axis labels smaller

# Adjust the legend to make the labels closer together
ax.legend(fontsize=28, loc='upper center', bbox_to_anchor=(0.48, 1.24), ncol=3,
          handletextpad=0.3, columnspacing=0.4)  # Reduce spacing between legend labels

ax.tick_params(axis='y', labelsize=28)
ax.set_ylim(top=1.8)

# Add a dashed line at Y=1.0
ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)

# Adding values on top of the bars
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

add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)

fig.tight_layout()

plt.savefig('./figures/figure11a.png', dpi=300)

#plt.show()
