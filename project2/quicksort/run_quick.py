import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp
import re

def plot_strong(nthreads, arr_time_avg, time_avg):
    speedup = time_avg / np.array(arr_time_avg)
    
    plt.plot(nthreads, speedup, label='paralle quicksort')
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.title('Strong Scaling with size=1,000,000,000')
    plt.savefig('strong_big.pdf')

def run_seq(exe_path, n_runs):
    time_tot = 0
    
    for _ in range(n_runs):
        result = sp.run([exe_path], stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        
        print(output)
        
        match = re.search(r'elapsed time\[s\] ([\d\.e+-]+)', output)
        
        if match:
            time_str = match.group(1)
            time = float(time_str)
            time_tot += time
            
    time_avg = time_tot / n_runs
    return time_avg
    
def run_par(nthreads, exe_path, n_runs, arr_time_avg):
    time_tot = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        
        print(output) 
        
        match = re.search(r'elapsed time\[s\] ([\d\.e+-]+)', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            time_tot += time
            
    time_avg = time_tot / n_runs
    arr_time_avg.append(time_avg)
    
if __name__ == "__main__":
    par_time_avg = []
    seq_time_avg = 0
    
    nthreads = []
    
    for i in range(8):
        num_threads = 2 ** i
        nthreads.append(num_threads)
        
        print("Parallel Quicksor")
        run_par(num_threads, "./quicksort_par", 5, par_time_avg)
    
    print(f"averge parallel times: {par_time_avg}")
    
    print("Serial Quicksort")
    seq_time_avg = run_seq("./quicksort_seq", 5)
    print(f"serial time average: {seq_time_avg}")