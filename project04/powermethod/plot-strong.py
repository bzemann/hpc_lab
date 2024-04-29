import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

num_procs = [1, 2, 4, 8, 16, 32, 64]

path_data = 'strong_time.csv'
data = pd.read_csv(path_data)

avg_times = data.groupby('Num-processes')['Time'].mean()
avg_times_arr = np.array(avg_times)

plt.plot(num_procs, avg_times_arr, marker='o', linestyle='--')
plt.yscale('log') 
plt.xscale('log')
plt.ylabel('Time (s)')
plt.xlabel('Num. processes')

# Calculate the slope for the linear reference line in log-log space
log_num_procs = np.log(num_procs)
log_avg_times = np.log(avg_times_arr)
initial_slope = (log_avg_times[1] - log_avg_times[0]) / (log_num_procs[1] - log_num_procs[0])

# Create a linear reference line starting from the first point
ref_line = np.exp(log_avg_times[0]) * np.power(num_procs, initial_slope)
plt.plot(num_procs, ref_line, 'r--', label='Reference line')

plt.grid(True)
plt.legend()

plt.gca().yaxis.set_major_locator(ticker.LogLocator(base=10))
plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().yaxis.set_minor_locator(ticker.NullLocator())

plt.gca().xaxis.set_major_locator(ticker.FixedLocator(num_procs))
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().xaxis.set_minor_locator(ticker.NullLocator())

plt.savefig('strong.pdf')

plt.clf()

eff_arr = avg_times_arr[0] / (avg_times_arr * np.array(num_procs))

plt.plot(num_procs, eff_arr, marker='o', linestyle='--')
plt.axhline(y=1, color='r', linestyle='--', label='Ideal Efficiency')
plt.xlabel('Num. processes')
plt.ylabel('Efficiency')
plt.legend()

plt.xscale('log')
plt.grid(True)

plt.gca().xaxis.set_major_locator(ticker.FixedLocator(num_procs))
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().xaxis.set_minor_locator(ticker.NullLocator())

plt.savefig('strong_eff.pdf')
