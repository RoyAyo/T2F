import os
import librosa
import librosa.display
import numpy as np
import soundfile as sf
from tqdm import tqdm

# Input and output folders
input_folder = "fart_sound"  # Folder with 16-bit PCM mono WAVs
output_folder = "fart_sound_consistent"
os.makedirs(output_folder, exist_ok=True)

N_MELS = 128
N_FFT = 1024
HOP_LENGTH = 512 

TARGET_DURATION = 3  # Seconds
TARGET_SAMPLES = int(TARGET_DURATION * 44100)

def process_audio_to_16bit(file_path, output_path):
    y, sr = librosa.load(file_path, sr=44100, mono=True)

    # Pad or trim to ensure consistent length
    if len(y) < TARGET_SAMPLES:
        y = np.pad(y, (0, TARGET_SAMPLES - len(y)), mode="constant")
    else:
        y = y[:TARGET_SAMPLES]

    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS)    
    y_reconstructed = librosa.feature.inverse.mel_to_audio(mel_spec, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH)

    sf.write(output_path, y_reconstructed, sr, subtype="PCM_16")

for filename in tqdm(os.listdir(input_folder), desc="Processing audio files"):
    if filename.endswith(".wav"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        process_audio_to_16bit(input_path, output_path)

print("✅ All files processed successfully!")
