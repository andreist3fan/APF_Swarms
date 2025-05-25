import os 
import numpy as np 
#import matplotlib.pyplot as plt
#import Analysis_settings_levels as asl
 

current_dir = os.path.dirname(os.path.abspath(__file__))
#folder_storage = os.path.join(current_dir, "Arrays_Storage")
#simulation_values = np.load(os.path.join(folder_storage, "Storage_L2.npy"))
simulation_values = np.load("Storage_L2.npy")


def generate_latex_table(array, N_o):
    #Array_L2[performance parameter][obstacle_density][scenario][algorithm][run]
    path = [[], [], []] # For each scenario

    for i in range(5): # For each APF algorithm 
        path[0].append(sum(x for x in array[0][N_o][0][i] if x != -1 and x != 0) / sum(1 for x in array[0][N_o][0][i] if x != -1 and x != 0))
        path[1].append(sum(x for x in array[0][N_o][1][i] if x != -1 and x != 0) / sum(1 for x in array[0][N_o][1][i] if x != -1 and x != 0))
        path[2].append(sum(x for x in array[0][N_o][2][i] if x != -1 and x != 0) / sum(1 for x in array[0][N_o][2][i] if x != -1 and x != 0))

    comp = [[], [], []] # For each obstacle scenario

    for i in range(5): # For each APF algorithm 
        comp[0].append(sum(1000*x for x in array[2][N_o][0][i] if x != -1 and x != 0) / sum(1 for x in array[2][N_o][0][i] if x != -1 and x != 0))
        comp[1].append(sum(1000*x for x in array[2][N_o][1][i] if x != -1 and x != 0) / sum(1 for x in array[2][N_o][1][i] if x != -1 and x != 0))
        comp[2].append(sum(1000*x for x in array[2][N_o][2][i] if x != -1 and x != 0) / sum(1 for x in array[2][N_o][2][i] if x != -1 and x != 0))

    reach = [[], [], []] # For each obstacle scenario

    for i in range(5): #  For each APF algorithm 
        reach[0].append(sum(100*x for x in array[3][N_o][0][i] if x != -1 and x != 0) / sum(1 for x in array[3][N_o][0][i] if x != -1))
        reach[1].append(sum(100*x for x in array[3][N_o][1][i] if x != -1 and x != 0) / sum(1 for x in array[3][N_o][1][i] if x != -1))
        reach[2].append(sum(100*x for x in array[3][N_o][2][i] if x != -1 and x != 0) / sum(1 for x in array[3][N_o][2][i] if x != -1))

    metrics = [reach, path, comp]
    metric_names = ["Reachability (\%)", "Path Length (m)", "Comp. Complexity (ms)"]
    scenarios = ["Scenario A", "Scenario B", "Scenario C"]
    algorithms = ["CAPF", "BAPF", "CR-BAPF*", "RAPF", "A*"]
    num_perf_params = len(metrics)
    num_densities = len(metrics[0])
    num_scenarios = len(scenarios)
    num_algorithms = len(algorithms)

    # LaTeX table header
    latex_str = r"""
\begin{table}[h]
\centering
\begin{tabular}{c|ccc|ccc|ccc|ccc}
\hline
"""

    # First row: Performance parameter headers spanning 3 columns each
    perf_headers = " & " + " & ".join([f"\multicolumn{{3}}{{c|}}{{{name}}}" for name in metric_names]) + "\\\\ \hline\n"

    # Second row: Obstacle density sub-columns
    density_headers = "Scenario $\rightarrow$ " + " & " + " & ".join(["A & B & C" for _ in range(num_perf_params)]) + "\\\\ \hline\n"

    latex_str += perf_headers + density_headers

    # Data rows: Each swarm size with corresponding values
    for idx in range(num_algorithms):
        row_values = []
        for metric in metrics:
            for scenario in range(num_scenarios):
                value = metric[scenario][idx]
                row_values.append(f"{value:.1f}")
        latex_str += f"{algorithms[idx]} & " + " & ".join(row_values) + "\\\\ \n"

    # Closing the table
    latex_str += r"""
\hline
\end{tabular}
\caption{Performance metrics for different swarm sizes and obstacle densities.}
\label{tab:swarm_results}
\end{table}
"""

    return latex_str


latex_code = generate_latex_table(simulation_values, N_o=4)
print(latex_code)