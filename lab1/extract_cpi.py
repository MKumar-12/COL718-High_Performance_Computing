import os
import re

# Function to extract CPI value from a stats.txt file
def extract_cpi(stats_file_path):
    with open(stats_file_path, 'r') as file:
        for line in file:
            if "cpi" in line.lower():  # Search for 'cpi' in a case-insensitive manner
                match = re.search(r"\d+\.\d+", line)  # Find the CPI value (floating-point number)
                if match:
                    return float(match.group(0))
    return None


# Traverse through the files and directories to find all stats.txt files and extract their CPI values
extraction_path = os.getcwd + '/results/'
cpi_values = {}
for root, dirs, files in os.walk(extraction_path):
    for file in files:
        if file == 'stats.txt':
            stats_file_path = os.path.join(root, file)
            cpi_value = extract_cpi(stats_file_path)
            if cpi_value is not None:
                config_name = os.path.basename(root)  # Use the subdirectory name as the configuration name
                cpi_values[config_name] = cpi_value


# Print the extracted CPI values
print(cpi_values)