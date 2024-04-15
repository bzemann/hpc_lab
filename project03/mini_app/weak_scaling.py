import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp
import re

def plot_weak_eff(nthreads, arr_time_avg, time_avg):
    eff = time_avg / np.array(arr_time_avg)
    
    plt.clf()
    
    plt.plot(nthreads, eff, label='efficency parallel')
    plt.axhline(y=1, color='r', linestyle='--', label='ideal')
    plt.xlabel('nthreads')
    plt.ylabel('efficency')
    plt.legend()
    plt.title('Weak Scaling')
    plt.savefig('weak.pdf')

def plot_time(nthreads, arr_time_avg, label):
    time = np.array(arr_time_avg)
       
    plt.plot(nthreads, time, marker='o', linestyle='', label=label)
    plt.xlabel('nthreadse')
    plt.ylabel('avg. time')
    plt.legend()
    plt.yscale('log')

    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=False))
    plt.gca().yaxis.set_minor_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=False))
    plt.gca().ticklabel_format(axis='y', style='plain')    
    
    plt.savefig('time_plot.pdf')
    
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
    par_time_avg0 = []
    par_time_avg1 = []
    par_time_avg2 = []
    seq_time_avg0 = 0
    seq_time_avg1 = 0
    seq_time_avg2 = 0
    
    n_threads = []
    
    args0 = ['64', '100', '0.005']
    args1 = ['128', '100', '0.005']
    args2 = ['256', '100', '0.005']
    args3 = ['512', '100', '0.005']
    args4 = ['1024', '100', '0.005']
    args5 = ['2048', '100', '0.005']
    
    for i in range(4):
        num_threads = 4 ** i
        n_threads.append(num_threads)
        args_tmp0 = []
        args_tmp1 = []
        args_tmp2 = []
        
        if num_threads == 1:
            args_tmp0 = args0
            args_tmp1 = args1
            args_tmp2 = args2
        elif num_threads == 4:
            args_tmp0 = args1
            args_tmp1 = args2
            args_tmp2 = args3
        elif num_threads == 16:
            args_tmp0 = args2
            args_tmp1 = args3
            args_tmp2 = args4
        else:
            args_tmp0 = args3
            args_tmp1 = args4
            args_tmp2 = args5
            
        print(f"OMP_NUM_THREADS = {num_threads}\n")
        #run_weak(num_threads, "build/main", args, 2, par_time_avg)
        
        print("run with base 64")
        run_weak(num_threads, "./main", args_tmp0, 5, par_time_avg0)
        
        print("run with base 128")
        run_weak(num_threads, "./main", args_tmp1, 5, par_time_avg1)
        
        print("run with base 256")
        run_weak(num_threads, "./main", args_tmp2, 5, par_time_avg2)
        
    seq_time_avg0 = par_time_avg0[0]
    seq_time_avg1 = par_time_avg1[0]
    seq_time_avg2 = par_time_avg2[0]
    
    plot_time(n_threads, par_time_avg0, "base 64")
    plot_time(n_threads, par_time_avg1, "base 128")
    plot_time(n_threads, par_time_avg2, "base 256")
    
    plot_weak_eff(n_threads, par_time_avg0, seq_time_avg0)
    plot_weak_eff(n_threads, par_time_avg1, seq_time_avg1)
    plot_weak_eff(n_threads, par_time_avg2, seq_time_avg2)
