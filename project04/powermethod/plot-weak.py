import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

num_procs = [1, 4, 8, 16, 32, 64]

path_data = 'weak_time.csv'
data = pd.read_csv(path_data)
clean_data = data.dropna(axis=0)

avg_times = clean_data.groupby('Num-processes')['Time'].mean()
avg_times_arr = np.array(avg_times)

plt.plot(num_procs, avg_times_arr, marker='o', linestyle='--')
plt.yscale('log') 
plt.xscale('log')
plt.ylabel('Time (s)')
plt.xlabel('Num. processes')

plt.axhline(y=avg_times_arr[0], color='r', linestyle='--', label='Ideal time')

plt.grid(True)
plt.legend()

times = avg_times_arr.tolist()

plt.gca().yaxis.set_major_locator(ticker.FixedLocator(times))
plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().yaxis.set_minor_locator(ticker.NullLocator())

plt.gca().xaxis.set_major_locator(ticker.FixedLocator(num_procs))
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().xaxis.set_minor_locator(ticker.NullLocator())

plt.savefig('weak.pdf')

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

plt.savefig('weak_eff.pdf')

