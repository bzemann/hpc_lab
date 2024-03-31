import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp
import re

def plot_weak_eff(nthreads, arr_time_avg, time_avg):
    eff = time_avg / np.array(arr_time_avg)
    
    plt.plot(nthreads, eff, label='efficency parallel')
    plt.axhline(y=1, color='r', linestyle='--', label='ideal')
    plt.xlabel('nthreads')
    plt.ylabel('efficency')
    plt.legend()
    plt.title('Weak Scaling')
    plt.savefig('weak.pdf')
    
def run_weak(nthreads, exe_path, args, n_runs, arr_time_avg):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    commands = [exe_path] + args
    
    for _ in range(n_runs):
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
    par_time_avg = []
    seq_time_avg = 0
    
    n_threads = []
    
    args1 = ['64', '100', '0.005']
    args2 = ['128', '100', '0.005']
    args3 = ['256', '100', '0.005']
    args4 = ['512', '100', '0.005']
    
    for i in range(4):
        num_threads = 4 ** i
        n_threads.append(num_threads)
        args = []
        
        if num_threads == 1:
            args = args1
        elif num_threads == 4:
            args = args2
        elif num_threads == 16:
            args = args3
        else:
            args = args4
            
        print(f"OMP_NUM_THREADS = {num_threads}\n")
        #run_weak(num_threads, "build/main", args, 2, par_time_avg)
        run_weak(num_threads, "./main", args, 5, par_time_avg)
        
    seq_time_avg = par_time_avg[0]
    
    plot_weak_eff(n_threads, par_time_avg, seq_time_avg)
