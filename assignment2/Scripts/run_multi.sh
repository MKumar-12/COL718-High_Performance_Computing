#!/bin/bash

# Configuration file for the simulation
config_file="cache_multi.py"

# Define binary executables
binaries=("mm_simple.1" "mm_rearranged.1" "mm_blocked.1")

# Output file and results directory
fnl_res="simulation_cache.txt"
output_dir="results_cache"

# Define an array of passes with cache configurations
declare -A configs=(
    # Pass 1-2: Effect of CPU Model
    ["Pass1"]="TimingSimpleCPU 16kB 32kB 256kB 2 2 2 2 8 20 20 20"
    ["Pass2"]="DerivO3CPU 16kB 32kB 256kB 2 2 2 2 8 20 20 20"
    
    # Pass 3-5: Effect of Cache Size
    ["Pass3"]="TimingSimpleCPU 64kB 128kB 256kB 2 2 2 2 8 20 20 20"
    ["Pass4"]="DerivO3CPU 64kB 128kB 256kB 2 2 2 2 8 20 20 20"
    ["Pass5"]="TimingSimpleCPU 64kB 128kB 1MB 2 2 2 2 8 20 20 20"
    
    # Pass 6-8: Effect of Cache Associativity
    ["Pass6"]="DerivO3CPU 64kB 128kB 256kB 4 2 2 2 8 20 20 20"
    ["Pass7"]="DerivO3CPU 64kB 128kB 256kB 8 2 2 2 8 20 20 20"
    ["Pass8"]="DerivO3CPU 64kB 128kB 256kB 8 2 2 2 16 20 20 20"
    
    # Pass 9-10: Effect of Cache Latency
    ["Pass9"]="DerivO3CPU 64kB 128kB 256kB 8 2 2 2 16 10 10 10"
    ["Pass10"]="DerivO3CPU 64kB 128kB 256kB 8 4 4 4 16 20 20 20"
)

# Remove any existing results directory and output file
echo "Cleaning up old simulation results..."
rm -rf $output_dir
rm -f $fnl_res

# Create output directory
mkdir -p $output_dir
printf "%-10s %-20s %-20s %-20s %-20s %-20s\n" "Pass" "CPU Model" "Binary" "Tick Count" "Cache Miss Rate" "Execution Time" > $fnl_res

# Loop through each pass and binary to run the simulations
for pass in "${!configs[@]}"; do
    config=(${configs[$pass]})
    
    cpu=${config[0]}
    size_L1i=${config[1]}
    size_L1d=${config[2]}
    size_L2=${config[3]}
    assoc_L1=${config[4]}
    tag_latency_L1=${config[5]}
    data_latency_L1=${config[6]}
    response_latency_L1=${config[7]}
    assoc_L2=${config[8]}
    tag_latency_L2=${config[9]}
    data_latency_L2=${config[10]}
    response_latency_L2=${config[11]}
    
    if [[ "$pass" == "Pass1" || "$pass" == "Pass2" ]]; then
        binaries_to_run=("${binaries[@]}")
    else
        binaries_to_run=("mm_blocked.1")            # For passes 3-10, only run with the mm_blocked.1 binary
    fi


    for binary in "${binaries_to_run[@]}"; do
        # Define the output folder name
        result_dir="${output_dir}/${cpu}_${size_L1i}_${size_L1d}_${assoc_L1}_${tag_latency_L1}_${size_L2}_${assoc_L2}_${tag_latency_L2}_${binary}"
        mkdir -p "$result_dir"
        
        # Run the simulation with the current configuration
        result=$(./gem5.opt --outdir="$result_dir" $config_file \
            --cpu "$cpu" \
            --size_L1i "$size_L1i" \
            --size_L1d "$size_L1d" \
            --size_L2 "$size_L2" \
            --assoc_L1 "$assoc_L1" \
            --tag_latency_L1 "$tag_latency_L1" \
            --data_latency_L1 "$data_latency_L1" \
            --response_latency_L1 "$response_latency_L1" \
            --assoc_L2 "$assoc_L2" \
            --tag_latency_L2 "$tag_latency_L2" \
            --data_latency_L2 "$data_latency_L2" \
            --response_latency_L2 "$response_latency_L2" \
            --bin_exec "$binary" 2>&1)
        
        # Check if the simulation was successful
        if [ $? -ne 0 ]; then
            echo "Error: Simulation failed for $cpu with binary $binary in $pass" >&2
            tick_count="ERROR"
            cache_miss_rate="ERROR"
            exec_time="ERROR"
        else
            # Extract tick count, cache miss rate, and execution time from the result
            tick_count=$(echo "$result" | grep "Exiting @ tick" | awk '{print $4}')
            cache_miss_rate=$(grep "system.cpu.dcache.overallMissRate::total" "$result_dir/stats.txt" | awk '{print $2}')
            exec_time=$(grep "simSeconds" "$result_dir/stats.txt" | awk '{print $2}')
            
            # If the stats are not found, set them to "NOT FOUND"
            [ -z "$tick_count" ] && tick_count="NOT FOUND"
            [ -z "$cache_miss_rate" ] && cache_miss_rate="NOT FOUND"
            [ -z "$exec_time" ] && exec_time="NOT FOUND"
            
            printf "%-10s %-20s %-20s -> Done!\n" "$pass" "$cpu" "$binary"
        fi

        # Append the results to the output file
        printf "%-10s %-20s %-20s %-20s %-20s %-20s\n" "$pass" "$cpu" "$binary" "$tick_count" "$cache_miss_rate" "$exec_time" >> $fnl_res
    done
done

echo -e "\nSimulation completed. Results saved to $fnl_res."