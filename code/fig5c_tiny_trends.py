import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import scienceplots

# Set up the style
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 35           # specify font size here
})

file_path = './code/data_cleaned_tiny.csv'
df = pd.read_csv(file_path)

# Desired models (substrings to match in 'Model MLC')
desired_models = ['MobileNet', 'ResNet', 'DSCNN', 'AutoEncoder']

# Create a regex pattern that matches any of the desired models, case insensitive
pattern = '|'.join(desired_models)

# Filter the DataFrame to include rows where 'Model MLC' contains any of the desired models as a substring
df = df[df['Model MLC'].str.contains(pattern, case=False, na=False)]

# Function to calculate geometric mean
def geometric_mean(arr):
    return stats.gmean(arr)

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['Latency in ms'])].copy()
power_df = df[df['Units'].isin(['Energy in uJ']) & df['Result'].str.match(r'^\d+(\.\d+)?$')].copy()

# Clean and convert the 'Result' column to float
performance_df['Result'] = performance_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))
power_df['Result'] = power_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))

# Convert the 'date' field to datetime format
performance_df['date'] = pd.to_datetime(performance_df['date'])
power_df['date'] = pd.to_datetime(power_df['date'])

# Merge performance and power data on common columns
merged_df = pd.merge(performance_df, power_df, on=['Public ID', 'Model MLC', 'Scenario', 'version', 'date'], suffixes=('_perf', '_power'))

# Calculate the performance/power metric using 1/latency
merged_df['Performance/Power'] = 1 / merged_df['Result_power']

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Define marker symbols and colors
markers = ['o', 's', 'D', 'P', 'X', '^', 'v', '<', '>', 'p']
colors = plt.cm.tab10.colors  # Use a colormap for consistent colors

for i, model in enumerate(desired_models):
    model_data = merged_df[merged_df['Model MLC'].str.contains(model, case=False, na=False)]
    
    if model_data.empty:
        continue
    
    grouped = model_data.groupby(['version', 'date'])['Performance/Power'].apply(lambda x: x.max()).reset_index()

    # Ensure no negative slope
    max_perf_power = grouped['Performance/Power'].iloc[0]
    for j in range(1, len(grouped)):
        if grouped['Performance/Power'].iloc[j] < max_perf_power:
            grouped.at[j, 'Performance/Power'] = max_perf_power
        else:
            max_perf_power = grouped['Performance/Power'].iloc[j]
    
    # Normalize the Performance/Power values to 1 for the first version of each model
    grouped['Normalized Performance/Power'] = grouped['Performance/Power'] / grouped['Performance/Power'].iloc[0]

    # Plot the data
    ax.plot(grouped['date'], grouped['Normalized Performance/Power'], 
            marker=markers[i], color=colors[i], label=model, markersize=8)

# Ensure the x-axis includes the full range of dates with padding
all_dates = merged_df['date']
padding = pd.Timedelta(days=30)
ax.set_xlim(all_dates.min() - padding, all_dates.max() + padding)

# Set up the bottom X-axis for versions
versions = merged_df['version'].unique()
version_dates = merged_df.groupby('version')['date'].min()
ax.set_xticks(version_dates)
ax.set_xticklabels(version_dates.index, fontsize=28, rotation=45)

# Add a secondary X-axis for dates
ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xticks(version_dates)
ax_top.set_xticklabels(version_dates.dt.strftime('%m/%y'), fontsize=28)

# Set labels and title
ax.set_xlabel('MLPerf Tiny Benchmark Version', fontsize=35)
ax.set_ylabel('Normalized Energy Efficiency\n(Samples/Joule)', fontsize=35)

# Set y-axis to log scale
ax.set_yscale('log')

# Customize grid to show only major gridlines
ax.grid(True, which="major", linestyle='--', linewidth=0.5)
ax_top.xaxis.grid(False)

# Add a legend
ax.legend(title='Benchmark', fontsize=24)
ax.tick_params(axis='y', labelsize=28)

# Adjust layout to prevent clipping
plt.tight_layout()

# Save the figure as an image file
plt.savefig('./figures/figure5c.png', dpi=300)

# Show the plot
#plt.show()
