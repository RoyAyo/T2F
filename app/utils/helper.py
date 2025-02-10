import os

def create_text_to_audio_map(audio_dir):
    text_to_audio_map = []
    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.endswith(".wav"):
                text = file.split(".")[0].split("_")[1]
                text_to_audio_map.append((text, file))
    return text_to_audio_map

def convert_string_text_to_array(text):
    text = text.replace("[", "").replace("]", "").replace('"', "").replace("`", "")
    array_text = text.split(",")
    return array_text