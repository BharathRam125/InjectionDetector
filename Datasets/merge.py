import pandas as pd

# Number of dataset parts
num_parts = 12

# Generate file names dynamically
file_parts = [f"dataset_part_{i}.csv" for i in range(1, num_parts + 1)]

# Load and merge all parts
df_list = [pd.read_csv(file) for file in file_parts]
merged_df = pd.concat(df_list, ignore_index=True)

# Save merged dataset
merged_df.to_csv("injection_dataset.csv", index=False)
print("Merged dataset saved as 'injection_dataset.csv'")

