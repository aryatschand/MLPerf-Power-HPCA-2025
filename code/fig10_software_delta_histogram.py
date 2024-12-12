import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import scienceplots

file_path = './code/data_cleaned_inference_datacenter.csv'
df = pd.read_csv(file_path)

# Standardize model names
df['Model MLC'] = df['Model MLC'].str.lower().replace({'rnnt': 'rnn-t'})
df['Model MLC'] = df['Model MLC'].str.lower().replace({'bert': 'bert-99.9'})

# Filter for 'Offline' scenario
df = df[(df['Scenario'].str.lower() == 'offline')]

# Function to calculate geometric mean
def geometric_mean(arr):
    return stats.gmean(arr)

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['queries/s', 'samples/s', 'Samples/s', 'Queries/s'])].copy()
power_df = df[df['Units'].isin(['System Power (W)', 'Power (W)', 'System Power', 'Watts'])].copy()

# Clean and convert the 'Result' column to float
performance_df['Result'] = performance_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))
power_df['Result'] = power_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))

# Convert the 'date' field to datetime format
performance_df['date'] = pd.to_datetime(performance_df['date'])
power_df['date'] = pd.to_datetime(power_df['date'])

# Extract numeric part of 'version' and convert to integer
def extract_version_number(version):
    import re
    match = re.search(r'\d+', version)
    return int(match.group()) if match else None

performance_df['version'] = performance_df['version'].apply(extract_version_number)
power_df['version'] = power_df['version'].apply(extract_version_number)

# Merge performance and power data on common columns
merged_df = pd.merge(performance_df, power_df, on=['Public ID', 'Model MLC', 'Scenario', 'version', 'date'], suffixes=('_perf', '_power'))

# Calculate the performance/power metric
merged_df['Performance/Power'] = merged_df['Result_perf'] / merged_df['Result_power']

# Sort the merged DataFrame by model, hardware configuration, and version
merged_df.sort_values(by=['Model MLC', 'Organization_perf', 'accelerator_model_name_perf', 'Total Accelerators_perf', 'version'], inplace=True)

# Calculate the delta efficiencies
deltas = []
for org in merged_df['Organization_perf'].unique():
    org_data = merged_df[merged_df['Organization_perf'] == org]
    for acc_model in org_data['accelerator_model_name_power'].unique():
        acc_data = org_data[org_data['accelerator_model_name_power'] == acc_model]
        for total_acc in acc_data['Total Accelerators_perf'].unique():
            acc_total_data = acc_data[acc_data['Total Accelerators_perf'] == total_acc].reset_index(drop=True)

            for i in range(len(acc_total_data)):
                for j in range(len(acc_total_data)):
                    if i != j and acc_total_data.at[i, 'Model MLC'] == acc_total_data.at[j, 'Model MLC']:
                        if (acc_total_data.at[j, 'version'] == acc_total_data.at[i, 'version'] + 1) or (acc_total_data.at[j, 'version'] == acc_total_data.at[i, 'version'] + 0.1):
                            old_efficiency = acc_total_data.at[i, 'Performance/Power']
                            new_efficiency = acc_total_data.at[j, 'Performance/Power']
                            delta = ((new_efficiency - old_efficiency) / old_efficiency) * 100
                            deltas.append(delta)

# Filter out delta values less than -50
deltas = [delta for delta in deltas if delta >= -50]

# Calculate the percentage of deltas greater than 0
percent_greater_than_zero = (sum(delta >= 50 for delta in deltas) / len(deltas)) * 100

# Use matplotlib and scienceplots to create the histogram
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 24           # specify font size here
})

# Plot the histogram with wider bars and lightcoral color
plt.figure(figsize=(10, 4))
plt.hist(deltas, bins=20, color='lightcoral', edgecolor='none')  # Reduced the number of bins for wider bars and removed the black outline

# Add titles and labels
plt.xlabel('Energy Efficiency Percent Increase (%)')
plt.ylabel('Frequency')

# Increase the font size for ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# Remove gridlines
plt.grid(False)

# Adjust layout for better appearance
plt.tight_layout()

# Save the figure as a PNG file
#plt.savefig('delta_efficiencies_histogram_no_grid.png', dpi=300)

plt.savefig('./figures/figure10.png', dpi=300)


# Show the plot
#plt.show()
