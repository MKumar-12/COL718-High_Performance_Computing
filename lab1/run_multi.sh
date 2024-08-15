#!/bin/bash

# Configuration file for the simulation
config_file="custom_config.py" 

# Frequencies, step size used : 200MHz
frequencies=("600MHz" "800MHz" "1GHz" "1.2GHz" "1.4GHz" "1.6GHz" "1.8GHz" "2GHz" "2.2GHz" "2.4GHz" "2.6GHz" "2.8GHz" "3GHz" "3.2GHz" "3.3GHz")

# CPU models
cpu_models=("AtomicSimpleCPU" "DerivO3CPU" "TimingSimpleCPU")

# Memory models
memory_models=("DDR3_1600_8x8" "DDR3_2133_8x8" "DDR4_2400_8x8" "DDR5_4400_4x8" "LPDDR5_5500_1x16_8B_BL32")


# Output file and results directory
fnl_res="simulation.txt"

# Remove any existing results directory and output file
echo "Cleaning up old simulation results..."
rm -rf results
rm -f $fnl_res


mkdir -p results
printf "%-20s %-25s %-10s %-15s\n" "CPU Model" "Memory Model" "Frequency" "Tick Count" > $fnl_res

# Run simulations
for cpu in "${cpu_models[@]}"; do
    echo -e "\n\nSimulating CPU model: $cpu"
    echo "=============================================="
    
    for freq in "${frequencies[@]}"; do
        for mem in "${memory_models[@]}"; do
            # Create a directory for each simulation result
            result_dir="results/${cpu}_${freq}_${mem}"
            mkdir -p "$result_dir"

            # Run simulation and capture output
            result=$(./gem5.opt --outdir="$result_dir" $config_file --cpu="$cpu" --freq="$freq" --mem="$mem" 2>&1)

            # Check if the simulation was successful
            if [ $? -ne 0 ]; then
                echo "Error: Simulation failed for $cpu@$freq with $mem" >&2
                tick_count="ERROR"
            else
                # Extract the tick count from the result
                tick_count=$(echo "$result" | grep "Exiting @ tick" | awk '{print $4}')
                
                # If tick count is not found, set it to "NOT FOUND"
                if [ -z "$tick_count" ]; then
                    tick_count="NOT FOUND"
                fi
                
                printf "%-10s %-25s -> Done!\n" "$freq" "$mem"
            fi

            # Append the results to the output file
            printf "%-20s %-25s %-10s %-15s\n" "$cpu" "$mem" "$freq" "$tick_count" >> $fnl_res
        done
    done
done

echo -e "\nSimulation completed. Results saved to $fnl_res."