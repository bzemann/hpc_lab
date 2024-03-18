import matplotlib.pyplot as plt
import numpy as np
import re

file_path = 'pi-weak.out'
with open(file_path, 'r') as file:
  program_output = file.read()

# Regular expression patterns to extract relevant information
pattern_nthreads = re.compile(r"OMP_NUM_THREADS=(\d+)")
pattern_serial_dt = re.compile(r"pi_serial\n.*time = (\d+\.\d+) secs")
pattern_critical_dt = re.compile(r"pi_omp_critical\n.*time = (\d+\.\d+) secs")
pattern_reduction_dt = re.compile(r"pi_omp_reduction\n.*time = (\d+\.\d+) secs")

matches = pattern_nthreads.findall(program_output)
nthreads = []
nthreads.extend(map(int, matches))

matches = pattern_serial_dt.findall(program_output)
serial_dt = []
serial_dt.extend(map(float, matches))

matches = pattern_critical_dt.findall(program_output)
critical_dt = []
critical_dt.extend(map(float, matches))

matches = pattern_reduction_dt.findall(program_output)
reduction_dt = []
reduction_dt.extend(map(float, matches))

# Print the extracted data
print("OMP_NUM_THREADS:", nthreads)
print("pi_serial_times:", serial_dt)
print("pi_omp_critical_times:", critical_dt)
print("pi_omp_reduction_times:", reduction_dt)

critical_speedup = serial_dt[0] / np.array(critical_dt)
reduction_speedup = serial_dt[0] / np.array(reduction_dt)

plt.plot(nthreads, critical_speedup, label="critical")
plt.plot(nthreads, reduction_speedup, label="reduction")
plt.xlabel("nthreads")
plt.ylabel("speedup")
plt.legend()
plt.title("Weak Scaling")
plt.savefig("plot-weak.pdf")