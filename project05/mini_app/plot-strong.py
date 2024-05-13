import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

omp_data = pd.read_csv('res/omp/strong_time.csv')
mpi_data = pd.read_csv('res/mpi/mpi-strong_time.csv')

omp_median = omp_data.groupby(['Size', 'Threads']).median().reset_index()
mpi_median = mpi_data.groupby(['Size', 'Threads']).median().reset_index()

sizes = omp_data['Size'].unique()

def set_log_ticks(ax, data):
    min_val = data.min()
    max_val = data.max()
    lower = 10**np.floor(np.log10(min_val))
    upper = 10**np.ceil(np.log10(max_val))
    ticks = [lower * 10**(0.5 * i) for i in range(int((np.log10(upper) - np.log10(lower)) / 0.5) + 1)]
    ax.set_yticks(ticks)
    ax.set_ylim([lower, upper])

for size in sizes:
    fig, ax = plt.subplots(figsize=(10, 6))

    omp_subset = omp_median[omp_median['Size'] == size]
    mpi_subset = mpi_median[mpi_median['Size'] == size]
    
    ax.plot(omp_subset['Threads'], omp_subset['Time'], 'o', label='OMP')
    ax.plot(mpi_subset['Threads'], mpi_subset['Time'], 's', label='MPI')
    
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel('Number of Threads')
    ax.set_ylabel('Time in Seconds')
    
    thread_counts = [1, 2, 4, 8, 16]
    ax.set_xticks(thread_counts)
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    
    all_times = np.concatenate([omp_subset['Time'], mpi_subset['Time']])
    set_log_ticks(ax, all_times)  
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda y, pos: f'{y:.2f}'))

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax.legend()
    
    plt.savefig(f'plots/strong_size_{size}.pdf')
    plt.close()
