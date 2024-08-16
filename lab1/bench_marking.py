import os
import re
import random
import matplotlib.pyplot as plt


save_dir = 'plots/'
os.makedirs(save_dir, exist_ok=True)

def plot_cpi_execution_by_cpu(memory_model, clock_rate, results):
    # Filter results for the given memory model and clock rate
    cpu_models = []
    cpi_values = []
    execution_times = []

    for config_name, values in results.items():
        if memory_model in config_name and clock_rate in config_name:
            cpu_model = config_name.replace(f'{memory_model}_{clock_rate}_', '')  # Extract CPU model
            cpu_models.append(cpu_model)
            cpi_values.append(values.get("CPI", None))
            execution_times.append(values.get("Execution Time (simSeconds)", None))
    
    # Ensuring we have data to plot
    if not cpu_models:
        print("No data available for the specified memory model and clock rate.")
        return

    # Plot CPI vs CPU Model
    plt.figure(figsize=(12, 5.5))

    plt.subplot(1, 2, 1)  # Subplot for CPI
    plt.bar(cpu_models, cpi_values, color='b')
    plt.xlabel('CPU Model')
    plt.ylabel('CPI')
    plt.title(f'CPI vs CPU Model at {clock_rate} with {memory_model}')
    plt.xticks(rotation=45, ha='right')

    # Plot Execution Time vs CPU Model
    plt.subplot(1, 2, 2)  # Subplot for Execution Time
    plt.bar(cpu_models, execution_times, color='g')
    plt.xlabel('CPU Model')
    plt.ylabel('Execution Time (ms)')
    plt.title(f'Execution Time vs CPU Model at {clock_rate} with {memory_model}')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'CPI_Execution_Variation_{memory_model}_{clock_rate}.png'))


def plot_cpi_execution_variation(cpu_model, clock_rate, results):
    # Filter results for the given CPU model and clock rate
    memory_models = []
    cpi_values = []
    execution_times = []

    for config_name, values in results.items():
        if cpu_model in config_name and clock_rate in config_name:
            memory_model = config_name.replace(f'{cpu_model}_{clock_rate}_', '')  # Extract memory model
            memory_models.append(memory_model)
            cpi_values.append(values.get("CPI", None))
            execution_times.append(values.get("Execution Time (simSeconds)", None))
    
    # Ensure we have data to plot
    if not memory_models:
        print("No data available for the specified CPU model and clock rate.")
        return

    # Plot CPI vs Memory Model
    plt.figure(figsize=(12, 5.5))

    plt.subplot(1, 2, 1)  # Subplot for CPI
    plt.bar(memory_models, cpi_values, color='b')
    plt.xlabel('Memory Model')
    plt.ylabel('CPI')
    plt.title(f'CPI vs Memory Model for {cpu_model} at {clock_rate}')
    plt.xticks(rotation=45, ha='right')

    # Plot Execution Time vs Memory Model
    plt.subplot(1, 2, 2)  # Subplot for Execution Time
    plt.bar(memory_models, execution_times, color='g')
    plt.xlabel('Memory Model')
    plt.ylabel('Execution Time (ms)')
    plt.title(f'Execution Time vs Memory Model for {cpu_model} at {clock_rate}')
    plt.xticks(rotation=45, ha='right')

    # Save and show plot
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'CPI_Execution_Variation_{cpu_model}_{clock_rate}.png'))
    # plt.show()


# Helper function to filter and sort results
def filter_and_sort_results(cpu_type, memory_type, results, metric_key):
    filtered_results = {}
    for config_name, metrics in results.items():
        if cpu_type in config_name and memory_type in config_name:
            frequency_match = re.search(r"(\d+\.\d+)GHz", config_name)
            if frequency_match:
                frequency = float(frequency_match.group(1))
                filtered_results[frequency] = metrics[metric_key]
    sorted_frequencies = sorted(filtered_results.keys())
    sorted_metrics = [filtered_results[freq] for freq in sorted_frequencies]
    return sorted_frequencies, sorted_metrics


# Function to plot CPI Variation with Freq.
def cpi_vs_freq(cpu_type, memory_type, results):
    sorted_frequencies, sorted_cpis = filter_and_sort_results(cpu_type, memory_type, results, "CPI")

    # Plot the CPI variation
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_frequencies, sorted_cpis, marker='o', linestyle='-', color='r', label=f'{cpu_type} with {memory_type}')
    
    # Add data labels
    for freq, cpi in zip(sorted_frequencies, sorted_cpis):
        plt.text(freq, cpi, f'{cpi:.2f}', fontsize=9, ha='right', color='black')

    plt.title(f'CPI Variation with Frequency')
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('CPI')
    plt.savefig(os.path.join(save_dir, f'CPI_freq_{cpu_type}-{memory_type}.png'))
    # plt.show()
        

# Function to plot combined CPI Variation with Frequency
def cpi_vs_freq_combined(configurations, results):
    plt.figure(figsize=(10, 6))

    # Loop through each configuration and plot the data
    for cpu_type, memory_type in configurations:
        sorted_frequencies, sorted_cpis = filter_and_sort_results(cpu_type, memory_type, results, "CPI")
        
        plt.plot(sorted_frequencies, sorted_cpis, marker='o', linestyle='-', label=f'{cpu_type} with {memory_type}')
        
        # Add data labels
        for freq, cpi in zip(sorted_frequencies, sorted_cpis):
            plt.text(freq, cpi, f'{cpi:.2f}', fontsize=9, ha='right', color='black')

    plt.title(f'CPI Variation with Frequency')
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('CPI')
    plt.legend() 
    plt.savefig(os.path.join(save_dir, f'CPI_freq_combined.png'))
    # plt.show()


# Function to plot Execution Time Variation with Frequency
def execution_time_vs_freq(cpu_type, memory_type, results):
    sorted_frequencies, sorted_times = filter_and_sort_results(cpu_type, memory_type, results, "Execution Time (simSeconds)")
 
    # Plot the Execution Time variation
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_frequencies, sorted_times, marker='o', linestyle='-', color='b', label=f'{cpu_type} with {memory_type}')

    # Add data labels
    for freq, time in zip(sorted_frequencies, sorted_times):
        plt.text(freq, time, f'{time:.2f}', fontsize=9, ha='right', color='black')

    plt.title(f'Execution Time Variation with Frequency')
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Execution Time (ms)')
    plt.legend()
    plt.savefig(os.path.join(save_dir, f'EX_freq_{cpu_type}-{memory_type}.png'))
    # plt.show()


# Function to plot combined Execution Time Variation with Frequency
def execution_time_vs_freq_combined(configurations, results):
    plt.figure(figsize=(10, 6))

    # Loop through each configuration and plot the data
    for cpu_type, memory_type in configurations:
        sorted_frequencies, sorted_times = filter_and_sort_results(cpu_type, memory_type, results, "Execution Time (simSeconds)")
        
        plt.plot(sorted_frequencies, sorted_times, marker='o', linestyle='-', label=f'{cpu_type} with {memory_type}')
        
        # Add data labels
        for freq, time in zip(sorted_frequencies, sorted_times):
            plt.text(freq, time, f'{time:.2f}', fontsize=9, ha='right', color='black')

    plt.title(f'Execution Time Variation with Frequency')
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Execution Time (ms)')
    plt.legend() 
    plt.savefig(os.path.join(save_dir, f'EX_freq_combined.png'))
    # plt.show()


# Function to Randomly select entries from the results & print 
def print_random(num, results):
    random_selection = random.sample(list(results.items()), min(len(results), num))

    # Print the randomly selected CPI and Execution Time values
    print("Randomly Selected CPI and Execution Time values:\n")
    print(f"{'Configuration Name':<50} {'CPI':<20} {'Execution Time (ms)':<25}")
    print("="*95)
    for config_name, metrics in random_selection:
        print(f"{config_name:<50} {metrics['CPI']:<20.2f} {metrics['Execution Time (simSeconds)']:<25.3f}")


# Function to extract CPI values
def extract_cpi(stats_file_path):
    with open(stats_file_path, 'r') as file:
        for line in file:
            if "cpi" in line.lower():  # Search for 'cpi' in a case-insensitive manner
                match = re.search(r"\d+\.\d+", line)  # Find the CPI value (floating-point number)
                if match:
                    return round(float(match.group(0)), 2)
    return None


# Function to extract Execution Time (sim_seconds) from a stats.txt file
def extract_sim_seconds(stats_file_path):
    with open(stats_file_path, 'r') as file:
        for line in file:
            if "simSeconds" in line:  # Search for 'simSeconds'
                match = re.search(r"\d+\.\d+", line)  # Find the Execution Time value (floating-point number)
                if match:
                    return round(1000 * float(match.group(0)), 3)
    return None


if __name__ == "__main__":
    extraction_path = os.getcwd() + '/results/'

    # Traversing through the files and directories to find all stats.txt files and extract their CPI and Execution Time values
    results = {}
    for root, dirs, files in os.walk(extraction_path):
        for file in files:
            if file == 'stats.txt':
                stats_file_path = os.path.join(root, file)
                cpi_value = extract_cpi(stats_file_path)
                sim_seconds_value = extract_sim_seconds(stats_file_path)
                if cpi_value is not None or sim_seconds_value is not None:
                    config_name = os.path.basename(root)  # Use the subdirectory name as the configuration name
                    results[config_name] = {
                        "CPI": cpi_value,
                        "Execution Time (simSeconds)": sim_seconds_value
                    }

    # print partial output values obtained from simulation results
    print_random(10, results)

    # Different configuration and their plots
    standalone_configs = [
        ("AtomicSimpleCPU", "DDR4_2400_8x8"),
        ("DerivO3CPU", "DDR4_2400_8x8"),
        ("TimingSimpleCPU", "DDR4_2400_8x8")
    ]
    for cpu_type, memory_type in standalone_configs:
        cpi_vs_freq(cpu_type, memory_type, results)
        execution_time_vs_freq(cpu_type, memory_type, results)

    hybrid_configs = [
        ("AtomicSimpleCPU", "LPDDR5_5500_1x16_8B_BL32"),
        ("TimingSimpleCPU", "LPDDR5_5500_1x16_8B_BL32"),
        ("DerivO3CPU", "LPDDR5_5500_1x16_8B_BL32")
    ]
    cpi_vs_freq_combined(hybrid_configs, results)
    execution_time_vs_freq_combined(hybrid_configs, results)

    #Plotting CPI and execution variation when CPU is clocked at specific clock-rate
    cpu_model = "TimingSimpleCPU"
    clock_rate = "1.8GHz"
    plot_cpi_execution_variation(cpu_model, clock_rate, results)

    #Plotting CPI and execution variation when memory model is fixed, & diff. CPU models clocked at specific clock-rate
    memory_model = "DDR3_2133_8x8"
    clock_rate = "2.2GHz"
    plot_cpi_execution_by_cpu(memory_model, clock_rate, results)