import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from matplotlib.ticker import FuncFormatter, LogLocator
import scienceplots

# Set up the style
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 35           # specify font size here
})

file_path = './code/data_cleaned_inference_datacenter.csv'
df = pd.read_csv(file_path)

# Standardize model names
df['Model MLC'] = df['Model MLC'].str.lower().replace({'rnnt': 'rnn-t'})
df['Model MLC'] = df['Model MLC'].str.lower().replace({'bert': 'bert-99.0'})

# Desired models (substrings to match in 'Model MLC')
desired_models = ['RetinaNet', 'BERT-99.0', 'ResNet', 'RNN-T', 'GPTJ-99.0', 'DLRM-v2-99.0', 'Llama2-70b-99.9']

# Create a regex pattern that matches any of the desired models, case insensitive
pattern = '|'.join([re.escape(model.lower()) for model in desired_models])

# Filter for 'offline' scenario and models matching the desired substrings
df = df[(df['Scenario'].str.lower() == 'offline') & df['Model MLC'].str.contains(pattern, case=False)]

# Convert 'Result' to numeric, handling errors (like non-numeric strings)
df['Result'] = pd.to_numeric(df['Result'].str.replace(",", "").replace('"', ''), errors='coerce')

# Adjust 'Result' if 'Units' is 'Tokens/s'
df.loc[df['Units'].str.contains('Tokens/s', case=False), 'Result'] = df.loc[df['Units'].str.contains('Tokens/s', case=False), 'Result'] / 292

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['queries/s', 'samples/s', 'Samples/s', 'Queries/s', 'Tokens/s'])].copy()
power_df = df[df['Units'].isin(['System Power (W)', 'Power (W)', 'System Power', 'Watts'])].copy()

# Convert the 'date' field to datetime format
performance_df['date'] = pd.to_datetime(performance_df['date'])
power_df['date'] = pd.to_datetime(power_df['date'])

# Merge performance and power data on common columns
merged_df = pd.merge(performance_df, power_df, on=['Public ID', 'Model MLC', 'Scenario', 'version', 'date'], suffixes=('_perf', '_power'))

# Calculate the performance/power metric
merged_df['Performance/Power'] = merged_df['Result_perf'] / merged_df['Result_power']

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Define marker symbols and colors
markers = ['o', 's', 'D', 'P', '^', 'o', 's']
colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'grey']

# Iterate over each model to plot the data
for i, model in enumerate(desired_models):
    # Match models using a case-insensitive approach
    model_data = merged_df[merged_df['Model MLC'].str.contains(model.lower(), case=False)]

    
    # Group by version and date, and take the maximum Performance/Power value for each group
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

    # Handle the case where only a single data point is available by forcing it to plot
    if len(grouped) == 1:
        grouped = pd.concat([grouped, grouped.iloc[[0]].assign(date=grouped['date'].iloc[0] + pd.Timedelta(days=1))])
    
    # Plot the data
    ax.plot(grouped['date'], grouped['Normalized Performance/Power'], 
            marker=markers[i], color=colors[i], label=model, markersize=8)

# Set the x-axis limits with padding
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


# Customize gridlines: only show vertical gridlines on the bottom X-axis for versions
ax.grid(True, which="major", axis='y', linestyle='--', linewidth=0.5)
ax.xaxis.grid(True, which="major", linestyle='--', linewidth=0.5)
ax_top.xaxis.grid(False)

# Set labels and title
ax.set_xlabel('MLPerf Inference Benchmark Version')
ax.set_ylabel('Normalized Energy Efficiency\n(Samples/Joule)')

# Set y-axis to log scale
ax.set_yscale('log')

# Set y-axis to show only powers of 10 in scientific notation
ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'$10^{{{int(np.log10(y))}}}$'))
ax.tick_params(axis='y', labelsize=28)

# Add a legend
ax.legend(title='Benchmark', fontsize=24)

# Adjust layout to prevent clipping
plt.tight_layout()

# Save the figure as an image file (optional)
plt.savefig('./figures/figure5a.png', dpi=300)

# Show the plot
#plt.show()
