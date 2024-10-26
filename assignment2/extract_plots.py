import matplotlib.pyplot as plt
import pandas as pd

def extract_binary_name(config):
    """Extract the binary file name from the full configuration string."""
    parts = config.split('_')
    
    # The binary name is the last element after the last '_', and removing any .1 or .2 extensions
    return parts[-1].split('.')[0]  

def plot_simulation_time(data):
    """Function to plot simulation time for different configurations."""
    data['Binary'] = data['Configuration'].apply(extract_binary_name)
    
    plt.figure(figsize=(10, 6))
    
    bars = plt.bar(data['Binary'], data['simSeconds'], color='orange', width=0.3)  

    # Add labels and title
    plt.xlabel('Binary File')
    plt.ylabel('Simulation Time (seconds)')
    plt.title('Simulation Time for Different Binary Files (Pass 2)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.ylim(0, 0.1)

    # Add the data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 5), va='bottom', ha='center')  # va: vertical alignment

    plt.tight_layout()
    plt.show()


def plot_cache_missrates(data):
    """Function to plot L1icache MissRate and L1dcache MissRate for different configurations."""
    data = data.copy()
    data['Binary'] = data['Configuration'].apply(extract_binary_name)
    
    # Set up the figure with 2 subplots (1 row, 2 columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.subplots_adjust(wspace=1.5)
    
    # Plot 1: L1icache MissRate
    ax1.bar(data['Binary'], data['L1icache_MissRate'], color='purple', width=0.3)
    ax1.set_xlabel('Binary File')
    ax1.set_ylabel('L1 Instruction Cache Miss Rate')
    ax1.set_title('L1I Cache Miss Rate (Pass 2)')
    ax2.set_xticks(range(len(data['Binary'])))
    ax1.set_xticklabels(data['Binary'], rotation=45, ha='right')
    ax1.grid(axis='y', which='major', linestyle='--')

    # Plot 2: L1dcache MissRate
    ax2.bar(data['Binary'], data['L1dcache_MissRate'], color='purple', width=0.3)
    ax2.set_xlabel('Binary File')
    ax2.set_ylabel('L1 Data Cache Miss Rate')
    ax2.set_title('L1D Cache Miss Rate (Pass 2)')
    ax2.set_xticks(range(len(data['Binary'])))
    ax2.set_xticklabels(data['Binary'], rotation=45, ha='right')
    ax2.grid(axis='y', which='major', linestyle='--')

    # Adjust the layout for better spacing
    plt.tight_layout()
    plt.show()


def plot_l2_missrate(data):
    """Function to plot L2 cache MissRate for different configurations."""
    data = data.copy()
    data['Binary'] = data['Configuration'].apply(extract_binary_name)

    # Set up the figure for L2 cache miss rate
    plt.figure(figsize=(10, 6))

    # Plot L2 cache MissRate
    bars = plt.bar(data['Binary'], data['L2_MissRate'], color='green', width=0.3)
    plt.xlabel('Binary File')
    plt.ylabel('L2 Cache Miss Rate')
    plt.title('L2 Cache Miss Rate (Pass 2)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', which='major', linestyle='--')

    # Add data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 5), va='bottom', ha='center')

    # Adjust the layout for better spacing
    plt.tight_layout()
    plt.show()


def plot_grouped_cache_size_effect(data):
    """Function to plot grouped L1i and L1d cache miss rates and L2 cache miss rates in subplots."""
    # Filter data for relevant passes and configurations
    relevant_passes = data[(data['Pass Count'].isin(['Pass 1', 'Pass 3', 'Pass 4', 'Pass 5'])) & 
                            (data['Configuration'].str.contains('mm_blocked'))]

    # Set up the figure with subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

    bar_width = 0.2  # Width for L1 bars
    indices = range(len(relevant_passes))

    # Plot L1i and L1d Miss Rates in the first subplot
    ax1.bar(indices, relevant_passes['L1icache_MissRate'], width=bar_width, label='L1i Miss Rate', color='blue', align='center')
    ax1.bar([i + bar_width for i in indices], relevant_passes['L1dcache_MissRate'], width=bar_width, label='L1d Miss Rate', color='green', align='center')

    # Set labels and title for the first subplot
    ax1.set_ylabel('Miss Rate')
    ax1.set_title('L1 Cache Miss Rates for Pass 1, Pass 3, Pass 4, and Pass 5 (mm_blocked)')
    ax1.set_xticks([i + bar_width / 2 for i in indices])
    ax1.set_xticklabels(relevant_passes['Configuration'], rotation=30, ha='right', fontsize=8)
    ax1.legend()

    # Plot L2 Miss Rate in the second subplot
    ax2.bar(indices, relevant_passes['L2_MissRate'], width=bar_width, label='L2 Miss Rate', color='red', align='center')

    # Set labels and title for the second subplot
    ax2.set_xlabel('Configuration')
    ax2.set_ylabel('Miss Rate')
    ax2.set_title('L2 Cache Miss Rates for Pass 1, Pass 3, Pass 4, and Pass 5 (mm_blocked)')
    ax2.set_xticks(indices)
    ax2.set_xticklabels(relevant_passes['Configuration'], rotation=30, ha='right', fontsize=8)
    ax2.legend()

    plt.tight_layout()
    plt.show()


def plot_grouped_associativity_effect(data):
    """Function to plot grouped L1i and L1d cache miss rates and L2 cache miss rates in subplots."""
    # Filter data for relevant passes and configurations
    relevant_passes = data[(data['Pass Count'].isin(['Pass 2', 'Pass 6', 'Pass 7', 'Pass 8'])) & 
                            (data['Configuration'].str.contains('mm_blocked'))]

    # Set up the figure with subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

    bar_width = 0.2  # Width for L1 bars
    indices = range(len(relevant_passes))

    # Plot L1i and L1d Miss Rates in the first subplot
    ax1.bar(indices, relevant_passes['L1icache_MissRate'], width=bar_width, label='L1i Miss Rate', color='yellow', align='center')
    ax1.bar([i + bar_width for i in indices], relevant_passes['L1dcache_MissRate'], width=bar_width, label='L1d Miss Rate', color='pink', align='center')

    # Set labels and title for the first subplot
    ax1.set_ylabel('Miss Rate')
    ax1.set_title('L1 Cache Miss Rates for Pass 2, Pass 6, Pass 7, and Pass 8 (mm_blocked)')
    ax1.set_xticks([i + bar_width / 2 for i in indices])
    ax1.set_xticklabels(relevant_passes['Configuration'], rotation=45, ha='right', fontsize=10)  # Rotated and reduced fontsize
    ax1.legend()

    # Plot L2 Miss Rate in the second subplot
    ax2.bar(indices, relevant_passes['L2_MissRate'], width=bar_width, label='L2 Miss Rate', color='cyan', align='center')

    # Set labels and title for the second subplot
    ax2.set_xlabel('Configuration')
    ax2.set_ylabel('Miss Rate')
    ax2.set_title('L2 Cache Miss Rates for Pass 2, Pass 6, Pass 7, and Pass 8 (mm_blocked)')
    ax2.set_xticks(indices)
    ax2.set_xticklabels(relevant_passes['Configuration'], rotation=45, ha='right', fontsize=10)  # Rotated and reduced fontsize
    ax2.legend()

    plt.tight_layout()
    plt.show()


def main():
    df = pd.read_csv('simulation_results.csv')

    # Filter data for Passes
    # pass_1_data = df[df['Pass Count'] == 'Pass 1']
    # pass_2_data = df[df['Pass Count'] == 'Pass 2']

    # Print the number of entries after filtering for Pass 1
    # print(f'Entries filtered for Pass 2: {len(pass_2_data)}')

    # plot_simulation_time(pass_1_data)
    # plot_cache_missrates(pass_1_data)
    # plot_l2_missrate(pass_1_data)

    # plot_simulation_time(pass_2_data)
    # plot_cache_missrates(pass_2_data)
    # plot_l2_missrate(pass_2_data)

    # plot_grouped_cache_size_effect(df)
    plot_grouped_associativity_effect(df)

if __name__ == "__main__":
    main()