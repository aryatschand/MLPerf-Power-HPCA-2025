import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

file_path = './code/data_cleaned_inference_datacenter.csv'
df = pd.read_csv(file_path)

# Standardize model names
df['Model MLC'] = df['Model MLC'].str.lower().replace({'rnnt': 'rnn-t'})
df['Model MLC'] = df['Model MLC'].str.lower().replace({'bert': 'bert-99.0', 'bert99.9': 'bert-99.9'})

# Filter for 'offline' scenario and specified models
desired_models = ['bert-99.0', 'bert-99.9']
df = df[(df['Scenario'].str.lower() == 'offline') & (df['Model MLC'].isin(desired_models))]

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['queries/s', 'samples/s', 'Samples/s', 'Queries/s'])].copy()
power_df = df[df['Units'].isin(['System Power (W)', 'Power (W)', 'System Power', 'Watts'])].copy()

# Clean and convert the 'Result' column to float
performance_df['Result'] = performance_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))
power_df['Result'] = power_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))

# Convert the 'date' field to datetime format
performance_df['date'] = pd.to_datetime(performance_df['date'])
power_df['date'] = pd.to_datetime(power_df['date'])

# Merge performance and power data on common columns
merged_perf = pd.merge(performance_df, power_df, on=['Public ID', 'Model MLC', 'Scenario', 'version', 'date'], suffixes=('_perf', '_power'))

# Calculate the performance/power metric
merged_perf['Performance/Power'] = merged_perf['Result_perf'] / merged_perf['Result_power']


# Pivot the data to have separate columns for bert-99.0 and bert-99.9
pivot_df = merged_perf.pivot_table(index=['Public ID', 'version', 'date'],
                                   columns='Model MLC',
                                   values='Performance/Power',
                                   aggfunc='max').reset_index()

# Filter for rows where both bert-99.0 and bert-99.9 are present
pivot_df = pivot_df.dropna(subset=['bert-99.0', 'bert-99.9'])

# Calculate the ratio of performance/power from bert-99.9 to bert-99.0
pivot_df['Efficiency Increase'] = (pivot_df['bert-99.0'] - pivot_df['bert-99.9']) / pivot_df['bert-99.9'] * 100  # Convert to percentage

# Use matplotlib and scienceplots to create the histogram
plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 24           # specify font size here
})


# Plot the histogram with wider bins and lightcoral color
plt.figure(figsize=(10, 4))
plt.hist(pivot_df['Efficiency Increase'], bins=20, color='lightcoral', edgecolor='none')

# Add titles and labels
plt.xlabel('Energy Efficiency Percent Increase (%)')
plt.ylabel('Frequency')

# Increase the font size for ticks
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Remove gridlines
plt.grid(False)

# Adjust layout for better appearance
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('./figures/figure8.png', dpi=300)

# Show the plot
#plt.show()
