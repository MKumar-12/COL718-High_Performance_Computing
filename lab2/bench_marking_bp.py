import os
import re
import random 
import matplotlib.pyplot as plt


save_dir = 'Plots/'
os.makedirs(save_dir, exist_ok=True)

# Function to plot graph of CPU_model with Mispredicted counts for various Branch Predictions
def plot_cond_mispredicted(results, cpu_model, parameter, y_limit):
    plt.rcParams.update({'font.size': 8})

    # Map parameter to appropriate labels for the plot
    title_map = {
        "system.cpu.branchPred.TakenMispredicted": "Branches Predicted as TAKEN but actually NOT TAKEN",
        "system.cpu.branchPred.NotTakenMispredicted": "Branches Predicted as NOT TAKEN but actually TAKEN"
    }

    y_label_map = {
        "system.cpu.branchPred.TakenMispredicted": "Branches Predicted as TAKEN but actually NOT TAKEN",
        "system.cpu.branchPred.NotTakenMispredicted": "Branches Predicted as NOT TAKEN but actually TAKEN"
    }

    filtered_results = {config: metrics for config, metrics in results.items() if cpu_model in config}
    if not filtered_results:
        print(f"No results found for {cpu_model}")
        return

    # Extracting branch prediction methods and corresponding mispredicted values
    branch_predictors = []
    mispredicted_values = []

    for config_name, metrics in filtered_results.items():
        branch_predictor = config_name.split('_')[1]        # Extract branch predictor name
        mispredicted_value = metrics.get(parameter, 0)      # Get the parameter value (e.g., TakenMispredicted or NotTakenMispredicted)
        branch_predictors.append(branch_predictor)
        mispredicted_values.append(mispredicted_value)

    # Repeat colors for bars
    colors = ['blue', 'green'] * (len(branch_predictors) // 2 + 1)  # Repeat colors as needed

    # Plotting
    plt.figure(figsize=(7, 4))

    bar_width = 0.3
    bars = plt.bar(branch_predictors, mispredicted_values, width=bar_width, color=colors[:len(branch_predictors)])

    plt.ylim(0, y_limit)
    plt.xlabel("Branch Prediction Method")
    plt.ylabel(y_label_map.get(parameter, "Mispredicted Branches"))
    plt.title(f"{title_map.get(parameter, 'Mispredicted Branches')} for {cpu_model}")

    # Display value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f"{save_dir}{cpu_model}_{parameter.replace('system.cpu.branchPred.', '')}.png")
    # plt.show()


# Function to subplot graph of CPU model with 2 different branch prediction statistics
def subplot_cond(results, cpu_model, parameter1, parameter2, y_limit):
    plt.rcParams.update({'font.size': 7})

    filtered_results = {config: metrics for config, metrics in results.items() if cpu_model in config}
    if not filtered_results:
        print(f"No results found for {cpu_model}")
        return

    # Extracting branch prediction methods and corresponding values for both parameters
    branch_predictors = []
    param1_values = []
    param2_values = []

    for config_name, metrics in filtered_results.items():
        branch_predictor = config_name.split('_')[1]  # Extract branch predictor name
        param1_value = metrics.get(parameter1, 0)  # Get parameter1 value
        param2_value = metrics.get(parameter2, 0)  # Get parameter2 value
        branch_predictors.append(branch_predictor)
        param1_values.append(param1_value)
        param2_values.append(param2_value)

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(10, 3))  # Two subplots in a single row

    bar_width = 0.4  
    positions = range(len(branch_predictors))

    # Plot for parameter1
    bars1 = axes[0].bar(positions, param1_values, width=bar_width, color='blue', align='center')
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(branch_predictors, ha='center')
    axes[0].set_ylim(0, y_limit)
    axes[0].set_xlabel("Branch Prediction Method")
    axes[0].set_ylabel("Conditional Branches Predicted as TAKEN")
    axes[0].set_title(f"Conditional Branches Predicted as TAKEN for {cpu_model}")

    # Display value on top of each bar for parameter1
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # Plot for parameter2
    bars2 = axes[1].bar(positions, param2_values, width=bar_width, color='green', align='center')
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(branch_predictors, ha='center')
    axes[1].set_ylim(0, y_limit)
    axes[1].set_xlabel("Branch Prediction Method")
    axes[1].set_ylabel("Conditional Branches Predicted as NOT TAKEN")
    axes[1].set_title(f"Conditional Branches Predicted as NOT TAKEN for {cpu_model}")

    # Display value on top of each bar for parameter2
    for bar in bars2:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    plt.subplots_adjust(wspace=10)  # adjust space between subplots
    plt.tight_layout()
    plt.savefig(f"{save_dir}{cpu_model}_{parameter1.replace('system.cpu.branchPred.', '')}_vs_{parameter2.replace('system.cpu.branchPred.', '')}.png")
    # plt.show()


# Function to plot graph of CPU model with branch prediction statistics
def plot_cond(results, cpu_model):
    results = {config: metrics for config, metrics in results.items() if cpu_model in config}
    if not results:
        print(f"No results found for {cpu_model}")
        return

    # Extracting branch prediction methods and corresponding condPredicted values
    branch_predictors = []
    cond_predicted_values = []

    for config_name, metrics in results.items():
        branch_predictor = config_name.split('_')[1]  
        cond_predicted = metrics.get("system.cpu.branchPred.condPredicted", 0)  
        branch_predictors.append(branch_predictor)
        cond_predicted_values.append(cond_predicted)

    colors = ['blue', 'green'] * (len(branch_predictors) // 2 + 1)

    # Plotting
    plt.figure(figsize=(10, 6))

    bar_width = 0.3  
    bars = plt.bar(branch_predictors, cond_predicted_values, width=bar_width, color=colors[:len(branch_predictors)])

    plt.ylim(0, 125000)
    plt.xlabel("Branch Prediction Method")
    plt.ylabel("Conditional Branches Predicted")
    plt.title(f"Conditional Branches Predicted for {cpu_model} over Different Branch Prediction Methods")

    # Display value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f"{save_dir}{cpu_model}_condPredicted.png")
    # plt.show()


# Function to Randomly select entries from the results & print 
def print_random(num, results):
    random_selection = random.sample(list(results.items()), min(len(results), num))
    
    common_prefix = "system.cpu.branchPred."

    print("Randomly Selected Branch Prediction Statistics:\n")
    for config_name, metrics in random_selection:
        print(f"Configuration: {config_name}")
        for stat_key, value in metrics.items():
            if stat_key == "system.cpu.cpi":
                print(f"  cpi                       : {value}")
            else:
                trimmed_key = stat_key.replace(common_prefix, "")
                print(f"  {trimmed_key:<25} : {value}")
        print("="*50)
        print()


# Function to extract a specific stat from the stats.txt file
def extract_stat(stats_file_path, stat_name):
    with open(stats_file_path, 'r') as file:
        for line in file:
            if stat_name in line:  # Search for the specific stat
                match = re.search(r"[-+]?\d*\.\d+|\d+", line)  # Find the numeric value
                if match:
                    return float(match.group(0)) if '.' in match.group(0) else int(match.group(0))
    return None


if __name__ == "__main__":
    extraction_path = os.getcwd() + '/results_bp/'

    # attributes to extract
    stats_to_extract = [
        "simSeconds",
        "system.cpu.cpi",
        "system.cpu.branchPred.condPredicted",
        "system.cpu.branchPred.condPredictedTaken",
        "system.cpu.branchPred.condIncorrect",
        "system.cpu.branchPred.predTakenBTBMiss",
        "system.cpu.branchPred.NotTakenMispredicted",
        "system.cpu.branchPred.TakenMispredicted",
        "system.cpu.branchPred.BTBLookups",
        "system.cpu.branchPred.BTBUpdates",
        "system.cpu.branchPred.BTBHits",
        "system.cpu.branchPred.BTBHitRatio"
    ]

    # Traversing through the files and directories to find all stats.txt files and extract their branch prediction stats
    results = {}
    for root, dirs, files in os.walk(extraction_path):
        for file in files:
            if file == 'stats.txt':
                stats_file_path = os.path.join(root, file)
                config_name = os.path.basename(root)  
                results[config_name] = {}

                # Extract each stat and store it in the results dictionary
                for stat in stats_to_extract:
                    value = extract_stat(stats_file_path, stat)
                    if value is not None:
                        results[config_name][stat] = value


    # Print simulation settings
    print(f"Memory Model used : DDR4_2400_8x8")
    print(f"CPU clock speed   : 2GHz")
    print()

    # Print partial output values obtained from simulation results
    print_random(2, results)

    # Graph for CPU_model with total count of Branches 
    # plot_cond(results, "TimingSimpleCPU")
    # plot_cond(results, "DerivO3CPU")

    # # Graph for CPU_model with count of Branches PREDICTED as TAKEN/NOT_TAKEN
    # subplot_cond(results, "TimingSimpleCPU", "system.cpu.branchPred.condPredictedTaken", "system.cpu.branchPred.condIncorrect", 65000)
    # subplot_cond(results, "DerivO3CPU", "system.cpu.branchPred.condPredictedTaken", "system.cpu.branchPred.condIncorrect", 65000)

    # # Graph for CPU_model with Branches Predicted as TAKEN but actually NOT TAKEN
    # plot_cond_mispredicted(results, "TimingSimpleCPU", "system.cpu.branchPred.TakenMispredicted", 1000)
    # plot_cond_mispredicted(results, "DerivO3CPU", "system.cpu.branchPred.TakenMispredicted", 2000)

    # # Graph for CPU_model with Branches Predicted as NOT TAKEN but actually TAKEN
    # plot_cond_mispredicted(results, "TimingSimpleCPU", "system.cpu.branchPred.NotTakenMispredicted", 20000)
    # plot_cond_mispredicted(results, "DerivO3CPU", "system.cpu.branchPred.NotTakenMispredicted", 20000)