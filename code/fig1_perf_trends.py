import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

# Use the scienceplots style
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 24           # specify font size here
})

# Load the CSV performance data from MLPerf inference
file_path = './code/data_performance.csv'
df = pd.read_csv(file_path, index_col=0)

# Transpose the DataFrame so that dates are the index
df_clean = df.T

# Convert the index (which contains dates) to datetime format
df_clean.index = pd.to_datetime(df_clean.index, format='%m/%d/%Y')

# List of benchmarks to plot with corresponding colors and markers
benchmarks_to_plot = {
    'ResNet': ('blue', 'D'),  # Blue with diamonds
    '3D U-Net': ('red', 's'),  # Red with squares
    'RetinaNet': ('purple', '^'),  # Purple with triangles
    'Mask R-CNN': ('yellowgreen', 'D'),  # Light green with diamonds
    'DLRM': ('teal', 'o'),  # Teal with circles
    'GPT-J': ('salmon', '^'),  # Salmon with triangles
    'Stable Diffusion v2': ('green', 'X'),  # Green with Xs
    'Moore\'s Law': ('gold', 'o'),  # Yellow with circles
}

# Mapping of versions to specific dates you provided
version_mapping = {
    'v0.5': '2018-12-12',
    'v0.6': '2019-06-10',
    'v1.0': '2020-07-29',
    'v1.1': '2021-06-30',
    'v2.0': '2021-12-01',
    'v2.1': '2022-06-29',
    'v3.0': '2022-11-09',
    'v3.1': '2023-06-28',
    'v4.0': '2023-11-08',
    'v4.1': '2024-06-12'
}

# Convert version dates to datetime
version_dates = pd.to_datetime(list(version_mapping.values()))

# Increase figure height to make it taller
plt.figure(figsize=(12, 8))  # Increase the height to 7 inches

# Plot each benchmark line with specified color and marker
for benchmark, (color, marker) in benchmarks_to_plot.items():
    if benchmark in df_clean.columns:
        plt.plot(df_clean.index, df_clean[benchmark], color=color, marker=marker, label=benchmark)

# Set the y-axis to log scale with base 2
plt.yscale('log', base=2)

# Set the limits of the primary y-axis with a max of 64
plt.ylim(bottom=1, top=64)

# Use LogLocator to ensure y-axis labels are powers of 2
plt.gca().yaxis.set_major_locator(plt.LogLocator(base=2.0, numticks=10))

# Change the y-axis labels to show actual numbers instead of powers of 2
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}'))

# Set the y-axis label font size to 20
plt.yticks(fontsize=20)

# Create the primary X-axis for versions
ax_bottom = plt.gca()

# Set the positions for the versions on the bottom axis
ax_bottom.set_xticks(version_dates)
ax_bottom.set_xticklabels(list(version_mapping.keys()), fontsize=20, rotation=45)

# Add a secondary x-axis for dates
ax_top = ax_bottom.twiny()

# Set the top X-axis to use dates and format them
ax_top.set_xlim(ax_bottom.get_xlim())
ax_top.set_xticks(version_dates)
ax_top.set_xticklabels(version_dates.strftime('%m/%y'), fontsize=16)

# Show vertical gridlines only on the bottom X-axis (versions)
ax_bottom.grid(True, axis='y', which="both", linestyle="--")
ax_bottom.xaxis.grid(True, which="major", linestyle='--', color='gray')  # Gridlines for versions
ax_top.xaxis.grid(False)  # Disable gridlines for the top X-axis (dates)

# Adding labels and title
ax_bottom.set_xlabel('MLPerf Inference Benchmark Version')
ax_bottom.set_ylabel('Normalized Performance')

# Add a legend to the plot closer to the top but reduce the bbox_to_anchor to avoid whitespace
ax_bottom.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4), ncol=4, fontsize=20, frameon=False)

# Adjust layout to prevent clipping of tick-labels
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Reduce the top space

plt.savefig('./figures/figure1.png', dpi=300)

# Display the plot
#plt.show()
