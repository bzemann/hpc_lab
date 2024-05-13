import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

def plot_data(file_path, title_suffix):
    data = pd.read_csv(file_path)

    grouped = data.groupby(['Base-Size', 'Threads'])

    mean_time = grouped['Time'].mean()
    std_dev = grouped['Time'].std()
    n = grouped['Time'].count()
    sem = std_dev / np.sqrt(n)
    confidence_level = 0.95
    t_critical = t.ppf((1 + confidence_level) / 2., n - 1)  
    ci = t_critical * sem

    means = mean_time.unstack(level=0)  
    cis = ci.unstack(level=0)  

    fig, ax = plt.subplots(figsize=(10, 6))

    for base in means.columns:
        ax.errorbar(means.index, means[base], yerr=cis[base], fmt='-o', label=f'Base {base}',
                    capsize=5, capthick=2, elinewidth=2, markeredgewidth=2)

    ax.set_xlabel('Number of Threads')
    ax.set_ylabel('Time in Seconds')
    
    ax.set_xscale('log')  
    ax.set_yscale('log')  
    
    ax.set_xticks(means.index)  
    
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))  
    
    ax.legend(title="Base Size")

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)    

    plt.tight_layout(pad=2)  # Reduce padding
    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)  # Adjust margins to better center the plot
    
    plt.savefig(f'plots/weak_{title_suffix}.svg', format='svg')
    plt.close()

mpi_file_path = 'res/mpi/mpi-weak_time.csv'
omp_file_path = 'res/omp/weak_time.csv'

plot_data(mpi_file_path, "MPI")
plot_data(omp_file_path, "OMP")
