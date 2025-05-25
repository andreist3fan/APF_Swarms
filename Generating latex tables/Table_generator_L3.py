import os 
import numpy as np 
#import matplotlib.pyplot as plt
#import Analysis_settings_levels as asl
 

current_dir = os.path.dirname(os.path.abspath(__file__))
#folder_storage = os.path.join(current_dir, "Arrays_Storage")
#simulation_values = np.load(os.path.join(folder_storage, "Storage_L2.npy"))
simulation_values = np.load("Storage_L3_2.npy")


def generate_latex_table_swarm(array):
    #Array[performance parameter][swarm setting][collision method][run]
    path = [[], [], [], []] # For each collision method

    for i in range(5): # For each swarm size (there are 5 in total)
        path[0].append(sum(x for x in array[0][i][0] if x != -1 and x != 0) / sum(1 for x in array[0][i][0] if x != -1 and x != 0))
        path[1].append(sum(x for x in array[0][i][1] if x != -1 and x != 0) / sum(1 for x in array[0][i][1] if x != -1 and x != 0))
        path[2].append(sum(x for x in array[0][i][2] if x != -1 and x != 0) / sum(1 for x in array[0][i][2] if x != -1 and x != 0))
        path[3].append(sum(x for x in array[0][i][3] if x != -1 and x != 0) / sum(1 for x in array[0][i][3] if x != -1 and x != 0))

    comp = [[], [], [], []] # For each collision method

    for i in range(5): # For each swarm size (there are 5 in total)
        comp[0].append(sum(1000*x for x in array[2][i][0] if x != -1 and x != 0) / sum(1 for x in array[2][i][0] if x != -1 and x != 0))
        comp[1].append(sum(1000*x for x in array[2][i][1] if x != -1 and x != 0) / sum(1 for x in array[2][i][1] if x != -1 and x != 0))
        comp[2].append(sum(1000*x for x in array[2][i][2] if x != -1 and x != 0) / sum(1 for x in array[2][i][2] if x != -1 and x != 0))
        comp[3].append(sum(1000*x for x in array[2][i][3] if x != -1 and x != 0) / sum(1 for x in array[2][i][3] if x != -1 and x != 0))

    reach = [[], [], [], []] # For each collision method

    for i in range(5): # For each swarm size (there are 5 in total)
        reach[0].append(sum(100*x for x in array[3][i][0] if x != -1 and x != 0) / sum(1 for x in array[3][i][0] if x != -1))
        reach[1].append(sum(100*x for x in array[3][i][1] if x != -1 and x != 0) / sum(1 for x in array[3][i][1] if x != -1))
        reach[2].append(sum(100*x for x in array[3][i][2] if x != -1 and x != 0) / sum(1 for x in array[3][i][2] if x != -1))
        reach[3].append(sum(100*x for x in array[3][i][2] if x != -1 and x != 0) / sum(1 for x in array[3][i][2] if x != -1))

    metrics = [reach, path, comp]
    metric_names = ["Reachability (\%)", "Path Length (m)", "Comp. Complexity (ms)"]
    swarm_sizes = [2, 5, 10, 15, 20]
    num_perf_params = len(metrics)
    num_densities = len(metrics[0])
    num_swarm_sizes = len(swarm_sizes)

    # LaTeX table header
    latex_str = r"""
\begin{table}[h]
\centering
\begin{tabular}{|c|cccc|cccc|cccc|}
\hline
"""

    # First row: Performance parameter headers spanning 4 columns each
    perf_headers = " & " + " & ".join([f"\multicolumn{{4}}{{c|}}{{{name}}}" for name in metric_names]) + "\\\\ \hline\n"

    # Second row: Obstacle density sub-columns
    density_headers = r"\diagbox{$N_a$}{$Method:$}" + " & " + " & ".join(["0 & 1 & 2 & 3" for _ in range(num_perf_params)]) + "\\\\ \hline\n"

    latex_str += perf_headers + density_headers

    # Data rows: Each swarm size with corresponding values
    for swarm_idx in range(num_swarm_sizes):
        row_values = []
        for metric in metrics:
            for dens in range(num_densities):
                value = metric[dens][swarm_idx]
                if metric == comp:
                    row_values.append(f"{value:.0f}")
                else:
                    row_values.append(f"{value:.1f}")
        latex_str += f"{swarm_sizes[swarm_idx]} & " + " & ".join(row_values) + "\\\\ \n"

    # Closing the table
    latex_str += r"""
\hline
\end{tabular}
\caption{Performance metrics for different swarm sizes and obstacle densities.}
\label{tab:swarm_results}
\end{table}
"""

    return latex_str

def generate_latex_table_scattering(array):
    #Array[performance parameter][swarm setting][collision method][run]
    path = [[], [], [], []] # For each collision method

    for i in range(5, 10): # For each starting radius (there are 5 in total)
        path[0].append(sum(x for x in array[0][i][0] if x != -1 and x != 0) / sum(1 for x in array[0][i][0] if x != -1 and x != 0))
        path[1].append(sum(x for x in array[0][i][1] if x != -1 and x != 0) / sum(1 for x in array[0][i][1] if x != -1 and x != 0))
        path[2].append(sum(x for x in array[0][i][2] if x != -1 and x != 0) / sum(1 for x in array[0][i][2] if x != -1 and x != 0))
        path[3].append(sum(x for x in array[0][i][3] if x != -1 and x != 0) / sum(1 for x in array[0][i][3] if x != -1 and x != 0))

    comp = [[], [], [], []] # For each collision method

    for i in range(5, 10): # For each starting radius (there are 5 in total)
        comp[0].append(sum(1000*x for x in array[2][i][0] if x != -1 and x != 0) / sum(1 for x in array[2][i][0] if x != -1 and x != 0))
        comp[1].append(sum(1000*x for x in array[2][i][1] if x != -1 and x != 0) / sum(1 for x in array[2][i][1] if x != -1 and x != 0))
        comp[2].append(sum(1000*x for x in array[2][i][2] if x != -1 and x != 0) / sum(1 for x in array[2][i][2] if x != -1 and x != 0))
        comp[3].append(sum(1000*x for x in array[2][i][3] if x != -1 and x != 0) / sum(1 for x in array[2][i][3] if x != -1 and x != 0))

    reach = [[], [], [], []] # For each collision method

    for i in range(5, 10): # For each starting radius (there are 5 in total)
        reach[0].append(sum(100*x for x in array[3][i][0] if x != -1 and x != 0) / sum(1 for x in array[3][i][0] if x != -1))
        reach[1].append(sum(100*x for x in array[3][i][1] if x != -1 and x != 0) / sum(1 for x in array[3][i][1] if x != -1))
        reach[2].append(sum(100*x for x in array[3][i][2] if x != -1 and x != 0) / sum(1 for x in array[3][i][2] if x != -1))
        reach[3].append(sum(100*x for x in array[3][i][2] if x != -1 and x != 0) / sum(1 for x in array[3][i][2] if x != -1))

    metrics = [reach, path, comp]
    metric_names = ["Reachability (\%)", "Path Length (m)", "Comp. Complexity (ms)"]
    swarm_sizes = [2, 3, 5, 7.5, 10]
    num_perf_params = len(metrics)
    num_densities = len(metrics[0])
    num_swarm_sizes = len(swarm_sizes)

    # LaTeX table header
    latex_str = r"""
\begin{table}[h]
\centering
\begin{tabular}{|c|cccc|cccc|cccc|}
\hline
"""

    # First row: Performance parameter headers spanning 4 columns each
    perf_headers = " & " + " & ".join([f"\multicolumn{{4}}{{c|}}{{{name}}}" for name in metric_names]) + "\\\\ \hline\n"

    # Second row: Obstacle density sub-columns
    density_headers = r"\diagbox{$r_s$}{$Method:$}" + " & " + " & ".join(["0 & 1 & 2 & 3" for _ in range(num_perf_params)]) + "\\\\ \hline\n"

    latex_str += perf_headers + density_headers

    # Data rows: Each swarm size with corresponding values
    for swarm_idx in range(num_swarm_sizes):
        row_values = []
        for metric in metrics:
            for dens in range(num_densities):
                value = metric[dens][swarm_idx]
                if metric == comp:
                    row_values.append(f"{value:.0f}")
                else:
                    row_values.append(f"{value:.1f}")
        latex_str += f"{swarm_sizes[swarm_idx]} & " + " & ".join(row_values) + "\\\\ \n"

    # Closing the table
    latex_str += r"""
\hline
\end{tabular}
\caption{Performance metrics for different swarm sizes and obstacle densities.}
\label{tab:swarm_results}
\end{table}
"""

    return latex_str


#latex_code = generate_latex_table_swarm(simulation_values)
latex_code = generate_latex_table_scattering(simulation_values)
print(latex_code)