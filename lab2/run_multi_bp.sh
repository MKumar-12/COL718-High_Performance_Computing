#!/bin/bash

# Configuration file for the simulation
config_file="branch_pred_multi.py" 

# CPU models
cpu_models=("DerivO3CPU" "TimingSimpleCPU")

# Branch prediction methods
bp_methods=("BiModeBP" "TournamentBP" "LocalBP" "TAGE")


# Output file and results directory
fnl_res="simulation_bp.txt"
output_dir="results_bp"

# Remove any existing results directory and output file
echo "Cleaning up old simulation results..."
rm -rf $output_dir
rm -f $fnl_res


mkdir -p $output_dir
printf "%-20s %-20s %-15s\n" "CPU Model" "Branch Predictor" "Tick Count" > $fnl_res

# Run simulations
for cpu in "${cpu_models[@]}"; do
    echo -e "\n\nSimulating CPU model: $cpu"
    echo "=============================================="
    
    for bp in "${bp_methods[@]}"; do
        # Create a directory for each simulation result
        result_dir="${output_dir}/${cpu}_${bp}"
        mkdir -p "$result_dir"

        # Run simulation and capture output
        result=$(./gem5.opt --outdir="$result_dir" $config_file --cpu="$cpu" --bp="$bp" 2>&1)

        # Check if the simulation was successful
        if [ $? -ne 0 ]; then
            echo "Error: Simulation failed for $cpu with $bp" >&2
            tick_count="ERROR"
        else
            # Extract the tick count from the result
            tick_count=$(echo "$result" | grep "Exiting @ tick" | awk '{print $4}')
            
            # If tick count is not found, set it to "NOT FOUND"
            if [ -z "$tick_count" ]; then
                tick_count="NOT FOUND"
            fi
            
            printf "%-20s %-20s -> Done!\n" "$cpu" "$bp"
        fi

        # Append the results to the output file
        printf "%-20s %-20s %-15s\n" "$cpu" "$bp" "$tick_count" >> $fnl_res
    done
done

echo -e "\nSimulation completed. Results saved to $fnl_res."