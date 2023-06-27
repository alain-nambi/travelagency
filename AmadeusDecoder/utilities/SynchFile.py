import os
import pandas as pd

from io import BytesIO

def retrieve_file(path):
    df = pd.read_csv(path)
    return df

def move_file_to_parent_folder(file_path, current_directory):
    # Extract the filename from the file path
    file_name = os.path.basename(file_path)

    # Create the destination directory inside the parent directory
    destination_directory = os.path.join(current_directory, 'processed')
    os.makedirs(destination_directory, exist_ok=True)

    # Move the file to the destination directory
    destination_path = os.path.join(destination_directory, file_name)
    os.rename(file_path, destination_path)

    print(f"File '{file_name}' moved to '{destination_directory}'.")

