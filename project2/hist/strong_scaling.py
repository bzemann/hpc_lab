import numpy as np
import matplotlib.pyplot as plt
import re
import subprocess as sp

def plot_stron(nthreads, arr_time_avg_ser, arr_time_avg_par):
    speedup = arr_time_avg_ser[0] / np.array(arr_time_avg_par)
    
    plt.plot(nthreads, speedup, label='reduction')
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.title('Strong Scaling')
    plt.savefig('strong.pdf')

def run_stron(nthreads, n_runs, exe_path, arr_time_avg):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(nthreads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Time:\s+(\d+\.\d+)\s+sec', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            tot_time += time
    avg_time = tot_time / n_runs
    arr_time_avg.append(avg_time)

if __name__ == "__main__":
    par_time_avg = []
    seq_time_avg = []
    
    nthreads = []
    
    print("Strong Scaling")
    print("Parallel:")
    for i in range(8):
        num_threads = 2 ** i
        nthreads.append(num_threads)
        
        print(f"Running with OMP_NUM_THREADS = {num_threads}")
        run_stron(num_threads, 6, "./hist_omp", par_time_avg)
        
    run_stron(1, 6, "./hist_seq", seq_time_avg)
    print("begin plotting")
    plot_stron(nthreads, seq_time_avg, par_time_avg)
