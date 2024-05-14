import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Function to calculate mean and confidence interval
def mean_confidence_interval(data, confidence=0.95):
    n = len(data)
    m, se = np.mean(data), stats.sem(data)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

# Load the datasets
data_50 = pd.read_csv('results_50_tasks.csv')
data_100 = pd.read_csv('results_100_tasks.csv')

# Function to plot and save the data
def plot_and_save(data, label, filename):
    # Group data by 'Num Workers' and calculate statistics
    stats = data.groupby('Num Workers')['Time Taken'].agg([np.mean, lambda x: mean_confidence_interval(x)[1], lambda x: mean_confidence_interval(x)[2]])
    stats.columns = ['mean', 'lower', 'upper']

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(stats.index, stats['mean'], yerr=[stats['mean'] - stats['lower'], stats['upper'] - stats['mean']], 
                fmt='-o', capsize=5, label=f'{label} tasks')

    # Customizing plot
    ax.set_xlabel('Number of Workers')
    ax.set_ylabel('Time Taken (seconds)')
    ax.legend()

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Save plot as SVG
    plt.savefig(f'{filename}.svg', format='svg')
    plt.close()

# Plot and save for 50 tasks
plot_and_save(data_50, '50', 'time_vs_workers_50')

# Plot and save for 100 tasks
plot_and_save(data_100, '100', 'time_vs_workers_100')
