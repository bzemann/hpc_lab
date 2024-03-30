import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp
import re

def plot_strong(nthreads, arr_time_avg, time_avg, label):
    speedup = time_avg / np.array(arr_time_avg)
    
    plt.plot(nthreads, speedup, label=label)
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.title('Strong Scaling')
    plt.savefig('strong.pdf')

def run_local(nthreads, exe_path, args, n_runs, arr_time_avg):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    
    for _ in range(n_runs):
        commands = [exe_path] + args
        result = sp.run(commands, env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        
        print(output)  
        
        match = re.search(r'simulation took\s+(\d+\.\d+)\s+seconds', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            tot_time += time
            
    time_avg = tot_time / n_runs
    arr_time_avg.append(time_avg)

def run_euler(nthreads, exe_path, args, n_runs, arr_time_avg):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    
    for _ in range(n_runs):
        commands = [exe_path] + args
        result = sp.run(commands, env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        
        print(output)

        match = re.search(r'simulation took\s+(\d+\.\d+)\s+seconds', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            tot_time += time
            
    time_avg = tot_time / n_runs
    arr_time_avg.append(time_avg)


if __name__ == "__main__":
    seq_time_avg = 0
    par_time_avg = []
    
    n_threads = []
    
    args = ['64', '100', '0.005']
    
    for i in range(5):
        num_threads = 2 ** i
        print(f"num threads: {num_threads}")
        n_threads.append(num_threads)
        

        print(f"OMP_NUM_THREADS = {num_threads}")
        run_local(num_threads, "build/main", args, 3, par_time_avg)
        #run_euler(num_threads, "./main", args, 5, par_time_avg)
        
    seq_time_avg = par_time_avg[0]
    
    print(f"seq. time avg: {seq_time_avg}")
    print(f"par. time avg: {par_time_avg}")
