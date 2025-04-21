import os 
import numpy as np 
import matplotlib.pyplot as plt
import Analysis_settings_levels as asl
 

current_dir = os.path.dirname(os.path.abspath(__file__))
folder_storage = os.path.join(current_dir, "Arrays_Storage")
swarm_values = np.load(os.path.join(folder_storage, "Storage_swarm_size_L1.npy"))
scattering_values = np.load(os.path.join(folder_storage, "Storage_scattering_L1.npy"))


def generate_latex_table_swarm(array):
    path = [[], [], []] # For each obstacle density

    for i in range(8): # For each swarm size (there are 8 in total)
        path[0].append(sum(x for x in array[0][0][i] if x != -1 and x != 0) / sum(1 for x in array[0][0][i] if x != -1 and x != 0))
        path[1].append(sum(x for x in array[0][1][i] if x != -1 and x != 0) / sum(1 for x in array[0][1][i] if x != -1 and x != 0))
        path[2].append(sum(x for x in array[0][2][i] if x != -1 and x != 0) / sum(1 for x in array[0][2][i] if x != -1 and x != 0))

    eff_path = [[], [], []] # For each obstacle density

    for i in range(8): # For each swarm size (there are 8 in total)
        eff_path[0].append(sum(x for x in array[1][0][i] if x != -1 and x != 0) / sum(1 for x in array[1][0][i] if x != -1 and x != 0))
        eff_path[1].append(sum(x for x in array[1][1][i] if x != -1 and x != 0) / sum(1 for x in array[1][1][i] if x != -1 and x != 0))
        eff_path[2].append(sum(x for x in array[1][2][i] if x != -1 and x != 0) / sum(1 for x in array[1][2][i] if x != -1 and x != 0))

    comp = [[], [], []] # For each obstacle density

    for i in range(8): # For each swarm size (there are 8 in total)
        comp[0].append(sum(1000*x for x in array[2][0][i] if x != -1 and x != 0) / sum(1 for x in array[2][0][i] if x != -1 and x != 0))
        comp[1].append(sum(1000*x for x in array[2][1][i] if x != -1 and x != 0) / sum(1 for x in array[2][1][i] if x != -1 and x != 0))
        comp[2].append(sum(1000*x for x in array[2][2][i] if x != -1 and x != 0) / sum(1 for x in array[2][2][i] if x != -1 and x != 0))

    reach = [[], [], []] # For each obstacle density

    for i in range(8): # For each swarm size (there are 8 in total)
        reach[0].append(sum(100*x for x in array[3][0][i] if x != -1 and x != 0) / sum(1 for x in array[3][0][i] if x != -1))
        reach[1].append(sum(100*x for x in array[3][1][i] if x != -1 and x != 0) / sum(1 for x in array[3][1][i] if x != -1))
        reach[2].append(sum(100*x for x in array[3][2][i] if x != -1 and x != 0) / sum(1 for x in array[3][2][i] if x != -1))

    metrics = [reach, path, eff_path, comp]
    metric_names = ["Reachability (\%)", "Path Length (m)", "Eff. Path Length", "Comp. Complexity (ms)"]
    swarm_sizes = [1, 2, 3, 5, 10, 15, 20, 25]
    num_perf_params = len(metrics)
    num_densities = len(metrics[0])
    num_swarm_sizes = len(swarm_sizes)

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
    density_headers = r"\diagbox{$N_a$}{$N_o$}" + " & " + " & ".join(["50 & 80 & 110" for _ in range(num_perf_params)]) + "\\\\ \hline\n"

    latex_str += perf_headers + density_headers

    # Data rows: Each swarm size with corresponding values
    for swarm_idx in range(num_swarm_sizes):
        row_values = []
        for metric in metrics:
            for dens in range(num_densities):
                value = metric[dens][swarm_idx]
                if metric == eff_path:
                    row_values.append(f"{value:.2f}")
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
    path = [[], [], []] # For each obstacle density

    for i in range(5): # For each start radius (there are 5 in total)
        path[0].append(sum(x for x in array[0][0][i] if x != -1 and x != 0) / sum(1 for x in array[0][0][i] if x != -1 and x != 0))
        path[1].append(sum(x for x in array[0][1][i] if x != -1 and x != 0) / sum(1 for x in array[0][1][i] if x != -1 and x != 0))
        path[2].append(sum(x for x in array[0][2][i] if x != -1 and x != 0) / sum(1 for x in array[0][2][i] if x != -1 and x != 0))

    eff_path = [[], [], []] # For each obstacle density

    for i in range(5):
        eff_path[0].append(sum(x for x in array[1][0][i] if x != -1 and x != 0) / sum(1 for x in array[1][0][i] if x != -1 and x != 0))
        eff_path[1].append(sum(x for x in array[1][1][i] if x != -1 and x != 0) / sum(1 for x in array[1][1][i] if x != -1 and x != 0))
        eff_path[2].append(sum(x for x in array[1][2][i] if x != -1 and x != 0) / sum(1 for x in array[1][2][i] if x != -1 and x != 0))

    comp = [[], [], []] # For each obstacle density

    for i in range(5):
        comp[0].append(sum(1000*x for x in array[2][0][i] if x != -1 and x != 0) / sum(1 for x in array[2][0][i] if x != -1 and x != 0))
        comp[1].append(sum(1000*x for x in array[2][1][i] if x != -1 and x != 0) / sum(1 for x in array[2][1][i] if x != -1 and x != 0))
        comp[2].append(sum(1000*x for x in array[2][2][i] if x != -1 and x != 0) / sum(1 for x in array[2][2][i] if x != -1 and x != 0))

    reach = [[], [], []] # For each obstacle density

    for i in range(5):
        reach[0].append(sum(100*x for x in array[3][0][i] if x != -1 and x != 0) / sum(1 for x in array[3][0][i] if x != -1))
        reach[1].append(sum(100*x for x in array[3][1][i] if x != -1 and x != 0) / sum(1 for x in array[3][1][i] if x != -1))
        reach[2].append(sum(100*x for x in array[3][2][i] if x != -1 and x != 0) / sum(1 for x in array[3][2][i] if x != -1))

    metrics = [reach, path, eff_path, comp]
    metric_names = ["Reachability (\%)", "Path Length (m)", "Eff. Path Length", "Comp. Complexity (ms)"]
    swarm_sizes = [1, 2, 3, 5, 10, 15, 20, 25]
    start_radii = [2, 3, 5, 7.5, 10]
    num_perf_params = len(metrics)
    num_densities = len(metrics[0])
    num_start_radii = len(start_radii)

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
    density_headers = r"\diagbox{$r_s$}{$N_o$}" + " & " + " & ".join(["50 & 80 & 110" for _ in range(num_perf_params)]) + "\\\\ \hline\n"

    latex_str += perf_headers + density_headers

    # Data rows: Each strart radius with corresponding values
    for radius_idx in range(num_start_radii):
        row_values = []
        for metric in metrics:
            for dens in range(num_densities):
                value = metric[dens][radius_idx]
                if metric == eff_path:
                    row_values.append(f"{value:.2f}")
                else:
                    row_values.append(f"{value:.1f}")
        latex_str += f"{start_radii[radius_idx]} & " + " & ".join(row_values) + "\\\\ \n"

    # Closing the table
    latex_str += r"""
\hline
\end{tabular}
\caption{Performance metrics for different swarm sizes and obstacle densities.}
\label{tab:swarm_results}
\end{table}
"""

    return latex_str


latex_code = generate_latex_table_swarm(swarm_values)
latex_code = generate_latex_table_scattering(scattering_values)
# Print LaTeX table
print(latex_code)