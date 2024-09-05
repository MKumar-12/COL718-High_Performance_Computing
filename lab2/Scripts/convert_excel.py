import pandas as pd

# Define the data as a dictionary of lists
data = {
    'Configuration': [
        'DerivO3CPU_BiModeBP', 'DerivO3CPU_TournamentBP', 'TimingSimpleCPU_LocalBP', 
        'TimingSimpleCPU_BiModeBP', 'DerivO3CPU_TAGE', 'TimingSimpleCPU_TournamentBP', 
        'TimingSimpleCPU_TAGE', 'DerivO3CPU_LocalBP'
    ],
    'simSeconds(ms)': [8.161, 7.406, 131.132, 131.132, 7.43, 131.132, 131.132, 9.819],
    'cpi': [9.36934, 8.502244, 150.542306, 150.542306, 8.530268, 150.542306, 150.542306, 11.272931],
    'condPredicted': [107344, 97077, 95670, 95670, 97527, 95670, 95670, 110269],
    'condPredictedTaken': [58278, 56315, 41498, 50111, 56246, 55597, 54895, 56168],
    'condIncorrect': [5568, 945, 14989, 6262, 1034, 759, 1532, 15358],
    'TakenMispredicted': [252, 83, 177, 142, 173, 80, 166, 1487],
    'NotTakenMispredicted': [5316, 862, 14812, 6120, 861, 679, 1366, 13871],
    'predTakenBTBMiss': [297, 390, 242, 226, 300, 271, 229, 314],
    'BTBLookups': [124887, 111378, 109387, 109387, 112039, 109387, 109387, 127638],
    'BTBUpdates': [5195, 756, 14728, 6036, 753, 595, 1282, 13762],
    'BTBHits': [121997, 108742, 107987, 107987, 109255, 107987, 107987, 124871],
    'BTBHitRatio': [0.976859, 0.976333, 0.987201, 0.987201, 0.975152, 0.987201, 0.987201, 0.978322]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel
excel_file = 'branch_prediction_stats_new.xlsx'
df.to_excel(excel_file, index=False)

print(f"Excel file '{excel_file}' created successfully.")
