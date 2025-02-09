import os

def list_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        cs = []
        for file in files:
            c  = file.split("_")[1].split(".")[0]
            cs.append(c)
        print(cs)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
folder_path = 'fart'
files = list_files_in_folder(folder_path)
