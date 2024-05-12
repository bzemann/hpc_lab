import numpy as np
import subprocess as sp
import re
import pandas as pd
    
def run_weak(nthreads, exe_path, args, n_runs, data_frame, base):
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
            
    avg_time = tot_time / n_runs
    data_frame.append({
        'Problem Size': args[0],
        'Threads': nthreads,
        'base': base,
        'avg. time': avg_time
    })
    
if __name__ == "__main__":    
    n_threads = []
    
    args0 = ['64', '100', '0.005']
    args1 = ['128', '100', '0.005']
    args2 = ['256', '100', '0.005']
    args3 = ['512', '100', '0.005']
    args4 = ['1024', '100', '0.005']
    args5 = ['2048', '100', '0.005']
    
    data_list = []
    
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
        
        print("run with base 64")
        run_weak(num_threads, "./main", args_tmp0, 5, data_list, 64)
        result = pd.DataFrame(data_list)
        result.to_csv('avg_times.csv', index=False, sep=',')
        
        print("run with base 128")
        run_weak(num_threads, "./main", args_tmp1, 5, data_list, 128)
        result = pd.DataFrame(data_list)
        result.to_csv('avg_times.csv', index=False, sep=',')

        print("run with base 256")
        run_weak(num_threads, "./main", args_tmp2, 5, data_list, 256) 
        result = pd.DataFrame(data_list)
        result.to_csv('avg_times.csv', index=False, sep=',')       
