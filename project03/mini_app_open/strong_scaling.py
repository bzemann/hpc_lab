import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import subprocess as sp
import re

def plot_strong(nthreads, 
                arr_time_avg1, 
                arr_time_avg2, 
                arr_time_avg3, 
                arr_time_avg4,
                arr_time_avg5,
                time_avg1,
                time_avg2,
                time_avg3,
                time_avg4, 
                time_avg5):
    speedup1 = time_avg1 / np.array(arr_time_avg1)
    speedup2 = time_avg2 / np.array(arr_time_avg2)
    speedup3 = time_avg3 / np.array(arr_time_avg3)
    speedup4 = time_avg4 / np.array(arr_time_avg4)
    speedup5 = time_avg5 / np.array(arr_time_avg5)
    
    plt.plot(nthreads, speedup1, label='size 64')
    plt.plot(nthreads, speedup2, label='size 128')
    plt.plot(nthreads, speedup3, label='size 256')
    plt.plot(nthreads, speedup4, label='size 512')
    plt.plot(nthreads, speedup5, label='size 1024')
    plt.plot(nthreads, nthreads, 'k--', label='Ideal Speedup')
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.savefig('strong.pdf')

def plot_time(nthreads, arr_time_avg, label, name):
    time = np.array(arr_time_avg)
    
    plt.clf()
    
    plt.plot(nthreads, time, marker='o', linestyle='', label=label)
    plt.xlabel('nthreads')
    plt.ylabel('avg. time')
    plt.legend()
    plt.yscale('log')
    
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=False))
    plt.gca().yaxis.set_minor_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=False))
    plt.gca().ticklabel_format(axis='y', style='plain')    
    plt.savefig(name)

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
    #seq time averages for each mesh size
    seq_time_avg1 = 0
    seq_time_avg2 = 0
    seq_time_avg3 = 0
    seq_time_avg4 = 0
    seq_time_avg5 = 0
    
    #par time averages for each mesh size
    par_time_avg1 = []
    par_time_avg2 = []
    par_time_avg3 = []
    par_time_avg4 = []
    par_time_avg5 = []
    
    n_threads = []
    
    args1 = ['64', '100', '0.005']
    args2 = ['128', '100', '0.005']
    args3 = ['256', '100', '0.005']
    args4 = ['512', '100', '0.005']
    args5 = ['1024', '100', '0.005']
    
    #warmup run
    #commands = ["./main"] + args1
    #env = {'OMP_NUM_THREADS': str(1)}
    #print("Warmup run")
    #res = sp.run(commands, env=env)
    
    for i in range(5):
        num_threads = 2 ** i
        n_threads.append(num_threads)
        

        print(f"OMP_NUM_THREADS = {num_threads}")
        
        print("size: 64")
        run_euler(num_threads, "./main", args1, 5, par_time_avg1)
        
        print("size: 128")
        run_euler(num_threads, "./main", args2, 5, par_time_avg2)
        
        print("size: 256")
        run_euler(num_threads, "./main", args3, 5, par_time_avg3)
        
        print("size: 512")
        run_euler(num_threads, "./main", args4, 5, par_time_avg4)
        
        print("size: 1024")
        run_euler(num_threads, "./main", args5, 5, par_time_avg5)
        
    seq_time_avg1 = par_time_avg1[0]
    seq_time_avg2 = par_time_avg2[0]
    seq_time_avg3 = par_time_avg3[0]
    seq_time_avg4 = par_time_avg4[0]
    seq_time_avg5 = par_time_avg5[0]
    
    plot_strong(n_threads, 
                par_time_avg1, 
                par_time_avg2,
                par_time_avg3,
                par_time_avg4,
                par_time_avg5,
                seq_time_avg1, 
                seq_time_avg2,
                seq_time_avg3,
                seq_time_avg4,
                seq_time_avg5)
    
    #plot time
    plot_time(n_threads, par_time_avg1, "size 64", "time_64.pdf")
    plot_time(n_threads, par_time_avg2, "size 128", "time_128.pdf")
    plot_time(n_threads, par_time_avg3, "size 256", "time_256.pdf")
    plot_time(n_threads, par_time_avg4, "size 512", "time_512.pdf")
    plot_time(n_threads, par_time_avg5, "size 1024", "time_1024.pdf")
