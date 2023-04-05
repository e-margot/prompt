import os
import pandas as pd
from parse_multiwoz import parse_multiwoz


# Specify the directory path where the JSON files are located
dir_path = "MultiWOZ_2.2/train"
# Specify the directory path where the dialogues.txt files will be saved
output_path = "data/dialogues"

# Create an empty list to store the dataframes
dfs = []

# Loop through all files in the directory
for filename in os.listdir(dir_path):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Send json file to parser
        input_path = os.path.join(dir_path, filename)
        df = parse_multiwoz(input_path, output_path)
        dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
df.to_csv('data/multiwoz_dialogs.csv', index=False)
