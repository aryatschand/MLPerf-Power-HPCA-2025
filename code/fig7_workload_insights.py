import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

# Apply the scienceplots style
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 28
})

# Data from the tiny 1.2-0004
data1 = {
    'Workload': ['AutoEncoder', 'DSCNN', 'MobileNet', 'ResNet Tiny'],
    'J/Sample': [5.25*0.000001, 18.56*0.000001, 40.8*0.000001, 27.17*0.000001],
    'MAC': [264192, 2664768, 7491968, 12534400]
}

# Data from datacenter 4.0-0063
data2 = {
    'Workload': ['3D UNet-99.9', 'Stable Diffusion', 'DLRM-v2-99.9', 'GPTJ-99.9', 'Llama2-99.9', 'ResNet Inf', 'RetinaNet', 'RNN-T', 'BERT-99.9'],
    'J/Sample': [110.4422926, 492.3917098, 0.01981354463, 26.77803242, 0.3815189837*292, 0.008687140755, 0.4549045607, 0.03166273635, 0.1107200351],
    'MAC': [3.425E+13, 1.35394E+14, 4328225500, 5.3075E+12, 2.32727E+13, 4089282560, 2.01E+11, 6314132597, 59793997800]
}

# Create DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Sort each DataFrame by 'J/Sample' in descending order
df1_sorted = df1.sort_values(by='J/Sample', ascending=False)
df2_sorted = df2.sort_values(by='J/Sample', ascending=False)

# Combine the sorted DataFrames
df_combined = pd.concat([df2_sorted, df1_sorted], ignore_index=True)

# Define categories, colors, and shapes
categories = {
    'Computer Vision': ['ResNet Tiny', 'ResNet Inf', 'RetinaNet', '3D UNet-99.9', 'MobileNet'],
    'Recommendation': ['DLRM-v2-99.9'],
    'Language': ['RNN-T', 'BERT-99.9', 'DSCNN'],
    'Generative AI': ['Stable Diffusion', 'GPTJ-99.9', 'Llama2-99.9'],
    'Anomaly Detection': ['AutoEncoder']
}

category_colors = {
    'Computer Vision': 'blue',
    'Recommendation': 'teal',
    'Language': 'red',
    'Generative AI': 'purple',
    'Anomaly Detection': 'grey'
}

category_shapes = {
    'Computer Vision': 'o',
    'Recommendation': 's',
    'Language': 'D',
    'Generative AI': '^',
    'Anomaly Detection': 'P'
}

# Create a mapping of workloads to categories
workload_to_category = {}
for category, workloads in categories.items():
    for workload in workloads:
        workload_to_category[workload] = category

# Plotting with both Y axes in log scale
fig, ax1 = plt.subplots(figsize=(14, 7))

# Bar plot for J/Sample
bar1 = ax1.bar(df2_sorted['Workload'], df2_sorted['J/Sample'], color='lightblue', label='Datacenter')
bar2 = ax1.bar(df1_sorted['Workload'], df1_sorted['J/Sample'], color='lightcoral', label='Tiny')

# Add colored dots for workload categories with different shapes
for i, workload in enumerate(df_combined['Workload']):
    category = workload_to_category[workload]
    ax1.scatter(i, min(df_combined['J/Sample']) / 5, color=category_colors[category], s=200, marker=category_shapes[category])

ax1.set_yscale('log')
ax1.set_xlabel('Workload')
ax1.set_ylabel('Energy per Inference\n(Joules/Sample)', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.tick_params(axis='x', labelsize=20)
ax1.tick_params(axis='y', labelsize=20)

# Combine workloads for setting x-ticks and labels
combined_workloads = list(df2_sorted['Workload']) + list(df1_sorted['Workload'])
ax1.set_xticks(range(len(combined_workloads)))
ax1.set_xticklabels(combined_workloads, rotation=30, ha='right')

# Secondary Y-axis for MAC values
ax2 = ax1.twinx()
ax2.plot(df_combined.index, df_combined['MAC'], color='green', linewidth=2, marker='o', label='MAC (Ops)')
ax2.set_yscale('log')
ax2.set_ylabel('Total MAC Operations', labelpad=10)
ax2.tick_params(axis='y', labelsize=20)

# Creating custom category legend
category_legend_elements = [
    plt.Line2D([0], [0], marker=category_shapes[category], color='w', label=category, markersize=13, markerfacecolor=color)
    for category, color in category_colors.items()
]

# Creating the Datacenter vs Tiny legend with thicker lines
workload_legend_elements = [
    plt.Line2D([0], [0], color='lightblue', lw=8, label='Datacenter'),
    plt.Line2D([0], [0], color='lightcoral', lw=8, label='Tiny'),
    plt.Line2D([0], [0], color='green', lw=4, label='MAC Operations')
]

# Combine legends and place them inside the figure, with Datacenter vs Tiny to the left of the category shapes legend
ax1.legend(handles=workload_legend_elements + category_legend_elements, loc='upper right', fontsize=20, bbox_to_anchor=(1, 1))

# Adjusting plot for better readability
fig.tight_layout()

plt.savefig('./figures/figure7.png', dpi=300)

#plt.show()
