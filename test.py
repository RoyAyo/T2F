import os

folder_path = "fart"  # Change this if needed

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path) and not filename.startswith("fart"):
        # Split filename and extension
        name, ext = os.path.splitext(filename)
        
        # Remove all dots from the name part
        name = name.replace(".", "")

        # Create new filename with "goat_" prefix
        new_name = f"fart_{name}{ext}"
        new_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(file_path, new_path)
        print(f'Renamed: {filename} -> {new_name}')

print("Renaming completed!")
