import os
import random 
import csv



# Function to Randomly select entries from the results & print 
def print_random(num, results):
    random_selection = random.sample(list(results.items()), min(len(results), num))
    
    print("Randomly Selected Simulation Statistics:\n")
    for config_name, metrics in random_selection:
        print(f"Configuration: {config_name}")
        for stat_key, value in metrics.items():
            if stat_key == "cpi":
                print(f"  cpi                       : {value}")
            else:
                # Format floating-point values to avoid scientific notation
                if isinstance(value, float):
                    print(f"  {stat_key:<25} : {value:.7f}")  # 7 decimal places
                else:
                    print(f"  {stat_key:<25} : {value}")
        print("="*50)
        print()


# Function to extract a specific stat from the stats.txt file
def extract_stat(stats_file_path, stat_name):
    with open(stats_file_path, 'r') as file:
        for line in file:
            if stat_name in line:  # Search for the specific stat
                # print(f"Debug: Found line for '{stat_name}': {line.strip()}")  # Debugging print
                # Split the line by whitespace and extract the second element (the numeric value)
                parts = line.split()
                if len(parts) > 1:
                    try:
                        extracted_value = float(parts[1])  # Assuming the second part is the desired value
                        # print(f"Debug: Extracted value for '{stat_name}': {extracted_value}")  # Debugging print
                        return extracted_value
                    except ValueError:
                        print(f"Warning: Unable to convert '{parts[1]}' to float for '{stat_name}'")  # Debugging print
    # print(f"Warning: '{stat_name}' not found in {stats_file_path}")  # Debugging print
    return None


# Function to save results to a CSV file
def save_results_to_csv(results, output_file):
    # Get the header from the first result's keys
    header = ['Configuration'] + list(next(iter(results.values())).keys())

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header
        
        for config_name, metrics in results.items():
            row = [config_name]
            for stat in header[1:]:
                value = metrics.get(stat, '')
                # Format floating-point values to avoid scientific notation
                if isinstance(value, float):
                    row.append(f"{value:.6f}")  # Format to 6 decimal places
                else:
                    row.append(value)
            writer.writerow(row)  # Write metrics row



if __name__ == "__main__":
    extraction_path = os.getcwd() + '/results_cache/'

    # attributes to extract
    stats_to_extract = {
        "simSeconds": "simSeconds",
        "system.cpu.cpi": "cpi",
        "system.cpu.icache.overallMissRate::total": "L1icache_MissRate",
        "system.cpu.dcache.overallMissRate::total": "L1dcache_MissRate",
        "system.l2cache.overallMissRate::total": "L2_MissRate"
    }

    # Traversing through the files and directories to find all stats.txt files and extract their cache performance statistics
    results = {}
    for root, dirs, files in os.walk(extraction_path):
        for file in files:
            if file == 'stats.txt':
                stats_file_path = os.path.join(root, file)
                config_name = os.path.basename(root)
                results[config_name] = {}

                # Extract each stat and store it in the results dictionary
                for original_stat, new_stat_name in stats_to_extract.items():
                    value = extract_stat(stats_file_path, original_stat)
                    if value is not None:
                        results[config_name][new_stat_name] = value
                    else:
                        print(f"Warning: '{new_stat_name}' not found in {stats_file_path}")  # Debugging print


    # Print simulation settings
    # print(f"Memory Model used : DDR4_2400_8x8")
    # print(f"CPU clock speed   : 2GHz")
    # print()

    # Print partial output values obtained from simulation results
    # print_random(2, results)

    # Save the results to a CSV file
    output_csv_file = 'simulation_results.csv'
    save_results_to_csv(results, output_csv_file)
    print(f"Results saved to {output_csv_file}")