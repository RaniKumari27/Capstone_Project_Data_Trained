import pandas as pd

# List of CSV files to merge
csv_files = ['nike.csv', 'columbia.csv', 'puma.csv', 'puma-women.csv']

# Read the first CSV file
merged_df = pd.read_csv(csv_files[0])

# Iterate over the remaining CSV files and merge on common columns
for file in csv_files[1:]:
    df = pd.read_csv(file)
    if merged_df['shoe_type'].dtype != df['shoe_type'].dtype:
        df['shoe_type'] = df['shoe_type'].astype(str)
    merged_df = pd.merge(merged_df, df, how='inner')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_output.csv', index=False)
