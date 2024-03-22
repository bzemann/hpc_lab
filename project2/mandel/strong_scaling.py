import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
import re

def plot_strong(n_threads, arr_time_ser_avg, arr_time_par_crit_avg):
    speedup_crit = arr_time_ser_avg / np.array(arr_time_par_crit_avg)
    
    plt.plot(n_threads, speedup_crit, label='critical')
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.title('Strong Scaling')
    plt.savefig('strong.pdf')

def run_ser(n_threads, n_runs, exe_path, time_avg_ser):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(n_threads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Total time:\s+(\d+\.\d+)\s+seconds', output)
        if match:
            tot_time += float(match.group(1))
    
    time_avg_ser = tot_time / n_runs
    

def run_par(n_threads, n_runs, exe_path, arr_time_avg_par):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(n_threads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Total time:\s+(\d+\.\d+)\s+seconds', output)
        if match:
            tot_time += float(match.group(1))
    
    avg_time = tot_time / n_runs
    arr_time_avg_par.append(avg_time)
    
if __name__ == "__main__":
    serial_time_avg = 0
    par_crit_tim_avg = []
    
    n_threads = []
    
    print("Strong scaling")
    for i in range(7):
        num_threads = 2 ** i
        n_threads.append(num_threads)
        
        print(f"Running with OMP_NUM_THREADS = {num_threads}")
        print("Parallel Critical")
        time_par = run_par(num_threads, 6, "./mandel_par_crit", par_crit_tim_avg)
        par_crit_tim_avg.append(time_par)
        
    print("Serial")
    #serial_time_avg = run_ser(1, 6, "./mandel_seq", serial_time_avg)
    serial_time_avg = par_crit_tim_avg[0]
    
    print(f"serial time avg: {serial_time_avg}")
    print("Begin with the ploting")
    plot_strong(n_threads, serial_time_avg, par_crit_tim_avg)