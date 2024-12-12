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

# Data from MLPerf Training v4.0 logs (submissions 4.0-0090 - 4.0-0097)
accelerators = [8, 64, 512]
compute_energy = [11.77, 15.08, 38.64]
interconnect_energy = [0.0, 5.3, 7.2]
time_to_train = [29.101, 5.488, 2.015]

# Creating the bar plot
bar_width = 0.35
index = np.arange(len(accelerators))

fig, ax1 = plt.subplots(figsize=(11, 6))

# Plotting the energy breakdown
bar1 = ax1.bar(index, compute_energy, bar_width, label='Compute Energy (MJ)', color='lightblue')
bar2 = ax1.bar(index, interconnect_energy, bar_width, bottom=compute_energy, label='Interconnect Energy (MJ)', color='lightcoral')

# Adding labels and title
ax1.set_xlabel('Number of Accelerators')
ax1.set_ylabel('Energy (MJ)')
ax1.set_xticks(index)
ax1.set_xticklabels(accelerators)
ax1.tick_params(axis='y', labelsize=20)

# Adding a secondary y-axis for Time-to-Train
ax2 = ax1.twinx()
line1 = ax2.plot(index, time_to_train, color='red', marker='o', linestyle='-', label='Time-to-Train (mins)')
ax2.set_ylabel('Time-to-Train (mins)', color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax2.tick_params(axis='y', labelsize=20)

# Combine all handles (bars and line) into a single legend
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

# Position the combined legend on top of the figure with adjusted spacing
ax1.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, fontsize=18, 
           handletextpad=0.5, columnspacing=0.7)

# Adjust layout to fit everything
plt.tight_layout(rect=[0, 0, 1, 0.9])

plt.savefig('./figures/figure6.png', dpi=300)

# Show plot
#plt.show()
