import os 
import numpy as np 
import matplotlib.pyplot as plt
import Analysis_settings_levels as asl 
import numpy as np
import Analysis_settings_levels as asl 

#Folders results 
current_dir = os.path.dirname(os.path.abspath(__file__))

folder_path_single_L2 = os.path.join(current_dir, "Plots_Results\\L2_Plots_Summary\\L2_Plots_single_agent")
folder_path_swarm_low_L2 = os.path.join(current_dir, "Plots_Results\\L2_Plots_Summary\\L2_Plots_swarm_low_scattering")
folder_path_swarm_high_L2 = os.path.join(current_dir, "Plots_Results\\L2_Plots_Summary\\L2_Plots_swarm_high_scattering")

folder = folder_path_single_L2

#Folder to array storage 
folder_storage = os.path.join(current_dir, "Arrays_Storage")
name_data = "Storage_L2.npy"

data = np.load(os.path.join(folder_storage, name_data))

#--------------Find and remove outlayer for one case----------------------

swarm_setting = 0 #single agent 
alg = 4 #A star

y = []

for i in range(5): 
     for j in range(len(data[2][i][swarm_setting][alg])): 
        y.append(data[2][i][swarm_setting][alg][j])

print("Data points: " +str(len(y)))

#Sort to get only the ones that reached target 
y_sorted = []
for i in range(len(y)): 
    if y[i] != -1.0:
        y_sorted.append(y[i])

#Print smallest and largest values 
y_sorted = np.sort(y_sorted)
print(y_sorted[0:5])
print(y_sorted[-10::])

# Find the maximum value
max_value = np.max(y)

# Remove the maximum value
y_filtered = []
for i in range(len(y)): 
    if y[i] < max_value: 
        y_filtered.append(y[i])

#Create histogram
min_value = np.min(y_filtered)
max_value = np.max(y_filtered)
print(max_value)
bin_width = 0.1
bins = np.arange(min_value, max_value + bin_width, bin_width)

plt.hist(y_filtered, bins=bins, edgecolor='black', alpha=0.7)
plt.xlabel("Computational Complexity")
plt.ylabel("Count")
plt.title("Computational Complexity with largest value dropped (A*)")
#plt.show()

#-----------Draw computational complexity based on time behaviour--------

def delete_outliers(array, gap, ignore): 
        
    array_sorted = np.sort(array)

    array_filtered = [] #values that need to get deleted because they are outliers 

    deleted = []

    con = True 

    for i in range(len(array_sorted)): 
        if i == 0: 
            array_filtered.append(array_sorted[i])
        #elif array_sorted[i] == ignore: 
            #array_filtered.append(array_sorted[i])
        else: 
            if array_sorted[i] < gap+array_sorted[i-1] and con and array_sorted[i] != ignore: 
                array_filtered.append(array_sorted[i])
                #print("Hehehhe")
            elif array_sorted[i] != ignore: 
                con = False 
                print("Deleted: "+str(array_sorted[i]))
                deleted.append(array_sorted[i])

    return array_filtered, deleted 

#Test delete outlier function 
y = [0.1, 0.3, 0.5, 5, 0.2, 7]
array_filtered, d = delete_outliers(y, 1.5, 0)
print("Filtered array: ")
print(array_filtered)
print("Max: "+str(np.max(array_filtered)))

#--------------Big overview with histogram-----------------------

# Generate random arrays
#np.random.seed(42)  # For reproducibility
#arrays = [np.random.randint(1, 100, 20) for _ in range(25)]  # 25 arrays with 20 elements each

#arrays = []
#for i in range(5):
#    for k in range(5): 

ovw_swarm = 1

# Create figure and subplots
fig, axes = plt.subplots(5, 5, figsize=(15, 15))
fig.subplots_adjust(hspace=0.5)

#Column: Obstacle density
#Row: Algorithm 

for c in range(5): 
    for r in range(5):
        ax = axes[r, c]
        y, deleted = delete_outliers(data[2][c][ovw_swarm][r], 3, -1)
        print("Obstacle "+str(c)+"Algorithm: "+str(r))
        print("Deleted: "+str(deleted))
        bins_setting = np.arange(0, np.max(y)+0.1, 0.1)
        ax.hist(y, bins=bins_setting, color='blue', edgecolor='black')
        #array_text = np.array2string(deleted, separator=', ')
        #ax.text(0.5, -0.25, array_text, fontsize=8, ha='center', va='top', transform=ax.transAxes)
        #y_nonzero = []
        #for x in y: 
        #    if x != 0: 
        #        y_nonzero.append(x)
        #ax.set_title("Alg: "+str(r)+", Obs_num: "+str(asl.L2_obstacle_numbers[c])+"Avg: "+str(round(sum(y_nonzero)/len(y_nonzero), 2)), fontsize=8)
        ax.set_title("Min: "+str(np.min(y))+", Max: "+str(np.max(y))+"Avg: "+str(round(sum(y)/len(y), 2)), fontsize=8)
plt.show()

'''

for i, ax in enumerate(axes.flat):
    data = arrays[i]
    
    # Plot histogram
    ax.hist(data, bins=10, alpha=0.7, color='blue', edgecolor='black')
    
    # Display array as text
    array_text = np.array2string(data, separator=', ')
    ax.text(0.5, -0.25, array_text, fontsize=8, ha='center', va='top', transform=ax.transAxes)

    ax.set_xticks([])
    ax.set_yticks([])

plt.show()

'''

