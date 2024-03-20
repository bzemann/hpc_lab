import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
import re

def plot_strong(arr_time_average_ser, arr_time_average_crit, arr_time_average_red, n_threads):
    speedup_critical = arr_time_average_ser / np.array(arr_time_average_crit)
    speedup_reduction = arr_time_average_ser / np.array(arr_time_average_red)
    
    plt.plot(n_threads, speedup_critical, label='critical')
    plt.plot(n_threads, speedup_reduction, label='reduction')
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.title('Strong Scaling')
    plt.savefig('strong_speed.pdf')
                      
def plot_weak(arr_time_average_ser, arr_time_average_crit, arr_time_average_red, n_threads):
    plt.clf()
    speedup_critical = np.array(arr_time_average_ser) / np.array(arr_time_average_crit)
    speedup_reduction = np.array(arr_time_average_ser) / np.array(arr_time_average_red)
   
    plt.plot(n_threads, speedup_critical, label='critical')
    plt.plot(n_threads, speedup_reduction, label='reduction')
    plt.xlabel('nthreads')
    plt.ylabel('speedup')
    plt.legend()
    plt.title('Weak Scaling')
    plt.savefig('weak_speed.pdf')
    
def plot_eff_weak(time_aver_crit1, time_aver_red1, arr_time_aver_crit, arr_time_aver_red, n_threads):
    plt.clf()
    eff_crit = time_aver_crit1 / np.array(arr_time_aver_crit) 
    eff_red = time_aver_red1 / np.array(arr_time_aver_red) 
    
    plt.plot(n_threads, eff_crit, label='critical')
    plt.plot(n_threads, eff_red, label='reduction')
    plt.axhline(y=1, color='r', linestyle='--', label='ideal critical')
    plt.xlabel('nthreads')
    plt.ylabel('efficiency')
    plt.legend()
    plt.title('Weak Scaling')
    plt.savefig('weak_eff.pdf')
    

def run_strong(n_threads, exe_path, n_runs, time_average):
    total_time = 0
    env = {'OMP_NUM_THREADS': str(n_threads)}

    for _ in range(n_runs):
        result = sp.run([exe_path], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output) 
        match = re.search(r'time = ([0-9.]+) secs', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            total_time += time
            
    time_average.append(total_time / n_runs)

def run_weak(n_threads, exe_path, n_runs, time_average):
    total_time = 0
    env = {'OMP_NUM_THREADS': str(n_threads)}

    for _ in range(n_runs):
        arg = 10000000 * n_threads
        arg_str = str(arg)
        result = sp.run([exe_path, arg_str], env=env, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        
        match = re.search(r'time = ([0-9.]+) secs', output)
        if match:
            time_str = match.group(1)
            time = float(time_str)
            total_time += time
            
    time_average.append(total_time / n_runs)

if __name__ == "__main__":
    serial_time_average_weak = []
    critical_time_average_weak = []
    reduction_time_average_weak = []
    
    serial_time_average_strong = []
    critical_time_average_strong = []
    reduction_time_average_strong = []
    
    n_threads = []

    print("Strong Scaling")
    for i in range(8):
        num_threads = 2 ** i
        n_threads.append(num_threads)
        
        print(f"Running with OMP_NUM_THREADS = {num_threads}")         
        print("Serial")
        run_strong(num_threads, "./pi_serial", 10, serial_time_average_strong)
        
        print("Critical")
        run_strong(num_threads, "./pi_omp_critical", 10, critical_time_average_strong)
        
        print("Reduction")
        run_strong(num_threads, "./pi_omp_reduction", 10, reduction_time_average_strong)
    plot_strong(serial_time_average_strong, 
                critical_time_average_strong, 
                reduction_time_average_strong, 
                n_threads)

    print("Weak Scaling")
    for i in range(8):
        num_threads = 2 ** i
        
        print(f"Running with OMP_NUM_THREADS = {num_threads}")         
        print("Serial")
        run_weak(num_threads, "./pi_serial", 10, serial_time_average_weak)
        
        print("Critical")
        run_weak(num_threads, "./pi_omp_critical", 10, critical_time_average_weak)
        
        print("Reduction")
        run_weak(num_threads, "./pi_omp_reduction", 10, reduction_time_average_weak)
    plot_weak(serial_time_average_weak, 
              critical_time_average_weak, 
              reduction_time_average_weak,
              n_threads)
    plot_eff_weak(critical_time_average_weak[0],
                  reduction_time_average_weak[0],  
                  critical_time_average_weak,
                  reduction_time_average_weak,
                  n_threads)
