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
    plt.titel('Strong Scaling')
    plt.savefig('strong.pdf')

def run_ser(n_threads, n_runs, exe_path, time_average):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(n_threads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Total Time:\s+(\d+.\d+)\s+seconds', output)
        if match:
            tot_time += float(match.group(1))
    
    time_average = tot_time / n_runs

#def run_par(n_threads, n_runs, exe_path, time_average):
#    tot_time = 0
#    env = {'OMP_NUM_THREADS': str(n_threads)}
#    for _ in range(n_runs):
#        result = sp.Popen([exe_path], env=env, stdout=sp.PIPE, bufsize=1, universal_newlines=True)
#        for line in result.stdout:
#            print(line, end='')
#            match = re.match(r'thread id: (\d+), finished in: (\d+\.\d+) seconds\s+, num iterations: (\d+)', line)
#            if match:
#                t_id, time_finished, num_iterations = match.groups()
#                print(f"Thread {t_id}: Finished in {time_finished} seconds, Number of iterations: {num_iterations}")
#            elif line.startswith("thread:"):
#                print(line.strip())
#
#        result.wait()
#        if result.returncode != 0:
#            print(f"Error running {exe_path}. Return code: {result.returncode}")
#            return
#
#        match = re.search(r'Total Time:\s+(\d+.\d+)\s+seconds', result.stdout)
#        if match:
#            tot_time += float(match.group(1))
#        else:
#            print("Total time not found in the output")
#            return
#    
#    # Calculate average time
#    time_average.append(tot_time / n_runs)


def run_par(n_threads, n_runs, exe_path, time_average):
    tot_time = 0
    env = {'OMP_NUM_THREADS': str(n_threads)}
    
    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'Total Time:\s+(\d+.\d+)\s+seconds', output)
        if match:
            tot_time += float(match.group(1))
    
    avg_time = tot_time / n_runs
    time_average.append(avg_time)

if __name__ == "__main__":
    serial_time_avg = 0
    par_crit_tim_avg = []
    
    n_threads = []
    
    print("Strong scaling")
    for i in range(4, -1, -1):
        num_threads = 2 ** i
        n_threads.append(num_threads)
        
        print(f"Running with OMP_NUM_THREADS = {num_threads}")
        print("Parallel Critical")
        run_par(num_threads, 4, "./mandel_par_crit", par_crit_tim_avg)
        
    print("Serial")
    run_ser(1, 4, "./mandel_seq", serial_time_avg)

    plot_strong(n_threads, serial_time_avg, par_crit_tim_avg)