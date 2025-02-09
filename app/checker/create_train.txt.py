import os

def read_file_names_in_folder(folder_path):
    file_names = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            name = os.path.splitext(filename)[0]
            file_names.append(name)
    return file_names

folder_path = 'fart/'
file_names = read_file_names_in_folder(folder_path)
print(len(file_names))

output_file_path = 'train.txt'
with open(output_file_path, 'w') as output_file:
    for filename in file_names:
        name = filename.split("_")[1]
        output_file.write(f"{name}|{name}.wav\n")
    