import numpy as np
import re
import matplotlib.pyplot as plt
import subprocess as sp

def run_speed_par(nthreads, n_runs, exe_path):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env = env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Parallel RunTime\s*:\s*(\d+\.\d+)', output)       
        if match:
            time_str = match.group(1)
            time = float(time_str)
            tot_time += time
            
    return tot_time / n_runs
    
def run_speed_seq(nthreads, n_runs, exe_path):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env = env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Sequential RunTime\s*:\s*(\d+\.\d+)', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            tot_time += time
            
    return tot_time / n_runs
    
if __name__ == "__main__":
    
    print("Parallel")
    par_time_avg = run_speed_par(128, 6, "./recur_omp")
    print("Serial")
    seq_time_avg = run_speed_seq(1, 6, "./recur_seq")
    
    speedup = seq_time_avg / par_time_avg
    print(f"The speedup with 128 thread is: {speedup}")