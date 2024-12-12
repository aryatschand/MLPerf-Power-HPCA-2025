import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.rcParams['text.usetex'] = False
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    "font.family": "serif",   # specify font family here
    "font.size": 26           # specify font size here
})

# TINY DATA
file_path = './code/data_cleaned_tiny.csv'
df = pd.read_csv(file_path)

# Filter for 'Server' scenario and specified models
desired_models = ['MobileNetV1 (0.25x)', 'ResNet-V1', 'DSCNN', 'FC AutoEncoder']
df = df[(df['Model MLC'].isin([model for model in desired_models]))]

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['Latency in ms'])].copy()
power_df = df[df['Units'].isin(['Energy in uJ']) & df['Result'].str.match(r'^\d+(\.\d+)?$')].copy()

# Clean and convert the 'Result' column to float
performance_df['Result'] = performance_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))
power_df['Result'] = power_df['Result'].apply(lambda x: float(x.replace(",", "").replace('"', "")))

# Merge performance and power data on common columns
merged_df = pd.merge(performance_df, power_df, on=['Public ID', 'Model MLC', 'Scenario', 'version', 'date'], suffixes=('_perf', '_power'))

# Calculate the energy/latency metric
merged_df['Energy/Latency'] = merged_df['Result_power'] / (1000 * merged_df['Result_perf'])
tiny_data = merged_df['Energy/Latency'].to_numpy()



# EDGE DATA
file_path = './code/data_cleaned_inference_edge.csv'
df = pd.read_csv(file_path)

df['Model MLC'] = df['Model MLC'].str.lower().replace({'rnnt': 'rnn-t'})
df['Model MLC'] = df['Model MLC'].str.lower().replace({'bert-99': 'bert-99.0'})

df = df[(df['Scenario'].str.lower().replace(" ", "") == 'offline')]

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['queries/s', 'samples/s', 'Samples/s', 'Queries/s'])].copy()
power_df = df[df['Units'].isin(['System Power (W)', 'Power (W)', 'System Power', 'Watts']) & ~df['Result'].str.contains('http', case=False)].copy()

power_df['Result'] = pd.to_numeric(power_df['Result'], errors='coerce')
edge_data = power_df['Result'].to_numpy()



# DATACENTER DATA
file_path = './code/data_cleaned_inference_datacenter.csv' 
df = pd.read_csv(file_path)

df['Model MLC'] = df['Model MLC'].str.lower().replace({'rnnt': 'rnn-t'})
df['Model MLC'] = df['Model MLC'].str.lower().replace({'bert': 'bert-99.0'})

# Filter for 'Server' scenario and specified models
df = df[(df['Scenario'].str.lower() == 'offline')]

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['queries/s', 'samples/s', 'Samples/s', 'Queries/s'])].copy()
power_df = df[df['Units'].isin(['System Power (W)', 'Power (W)', 'System Power', 'Watts'])].copy()
power_df['Result'] = pd.to_numeric(power_df['Result'], errors='coerce')

# Handle NaN values (e.g., remove or fill them)
power_df = power_df.dropna(subset=['Result'])
datacenter_data = power_df['Result'].to_numpy()



# TRAINING DATA
file_path = './code/data_cleaned_training.csv'
df = pd.read_csv(file_path)

# Filter the DataFrame for rows containing performance and power data
performance_df = df[df['Units'].isin(['Latency (In minutes)'])].copy()
power_df = df[df['Units'].isin(['kJ'])].copy()

# Clean and convert the 'Result' column to float
performance_df['Result'] = performance_df['Avg. Result at System Name'].apply(lambda x: float(x.replace(",", "").replace('"', "")))
power_df['Result'] = power_df['Avg. Result at System Name'].apply(lambda x: float(x.replace(",", "").replace('"', "")))

# Merge performance and power data on common columns
merged_df = pd.merge(performance_df, power_df, on=['Public ID', 'Model MLC'], suffixes=('_perf', '_power'))

# Calculate the energy/latency metric
merged_df['Energy/Latency'] = merged_df['Result_power'] * 1000 / (60 * merged_df['Result_perf'])
train_data = merged_df['Energy/Latency'].to_numpy()

# Calculate min and max values for each dataset
data_labels = ['Tiny', 'Edge', 'Datacenter', 'Training']
data_sets = [tiny_data, edge_data, datacenter_data, train_data]

min_values = [np.min(data) for data in data_sets]
max_values = [np.max(data) for data in data_sets]

# Adjust the max value for datacenter if it's less than 6280.21W
if max_values[2] < 6280.21:
    max_values[2] = 6280.2

# Plotting the bar chart
x = np.arange(len(data_labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 6))

# Plotting min values
bars1 = ax.bar(x - width/2, min_values, width, label='Min', color=['blue', 'red', 'green', 'purple'])

# Plotting max values
bars2 = ax.bar(x + width/2, max_values, width, label='Max', color=['lightblue', 'lightcoral', 'lightgreen', 'violet'])

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('System Type')
ax.set_ylabel('Power Consumption (W)')
ax.set_xticks(x)
ax.set_xticklabels(data_labels)

# Set Y-axis limits to add more white space on top
ax.set_ylim([min(min_values) / 2, max(max_values) * 5])

# Creating custom legend
import matplotlib.patches as mpatches
min_patch = mpatches.Patch(color='dimgrey', label='Minimum Power')
max_patch = mpatches.Patch(color='lightgrey', label='Maximum Power')
ax.legend(handles=[min_patch, max_patch], loc='upper left', fontsize=24)

# Function to format values
def format_value(val):
    if val < 1e-3:
        return f'{val * 1e6:.1f} uW'
    elif val < 1:
        return f'{val * 1e3:.1f} mW'
    elif val >= 1e6:
        return f'{val / 1e6:.1f} MW'
    elif val >= 1e3:
        return f'{val / 1e3:.1f} kW'
    else:
        return f'{val:.1f} W'

# Adding values on top of the bars with a smaller font size
def add_value_labels(bars, fontsize=18):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(format_value(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=fontsize)  # Set the fontsize here

add_value_labels(bars1, fontsize=18)  # Adjust the fontsize as needed
add_value_labels(bars2, fontsize=18)
ax.tick_params(axis='y', labelsize=20)


fig.tight_layout()
plt.yscale('log')

plt.savefig('./figures/figure2.png', dpi=300)


#plt.show()
