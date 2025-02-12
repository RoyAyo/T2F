import librosa
import numpy as np
import soundfile as sf

def extract_meaningful_audio(input_wav, output_wav, duration=5.0):
    # Load audio
    y, sr = librosa.load(input_wav, sr=None)  # Preserve original sample rate
    
    # Compute energy (sum of squared samples in a window)
    frame_length = int(sr * 0.05)  # 50ms per frame
    hop_length = int(frame_length / 2)  # Overlapping frames
    energy = np.array([
        np.sum(np.square(y[i:i + frame_length])) 
        for i in range(0, len(y) - frame_length, hop_length)
    ])
    
    # Find the segment with the highest energy
    segment_length = int(sr * duration)  # Convert seconds to samples
    max_energy_idx = np.argmax([
        np.sum(energy[i:i + segment_length // hop_length])
        for i in range(len(energy) - segment_length // hop_length)
    ])
    
    # Extract the corresponding audio
    start_sample = max_energy_idx * hop_length
    end_sample = start_sample + segment_length
    y_trimmed = y[start_sample:end_sample]
    
    # Save the extracted segment
    sf.write(output_wav, y_trimmed, sr)
    print(f"Extracted meaningful {duration} seconds to: {output_wav}")

# Usage Example
def extract_first_n_seconds(input_wav, output_wav, duration=5.0):
    # Load audio file
    y, sr = librosa.load(input_wav, sr=None)  # Preserve original sample rate
    
    # Compute number of samples corresponding to 'duration' seconds
    # num_samples = int(sr * duration)
    start_sample = int(sr * 2)
    end_sample = int(sr * 6)
    
    # Extract first 'duration' seconds
    y_trimmed = y[start_sample: end_sample]
    
    # Save the extracted segment
    sf.write(output_wav, y_trimmed, sr)
    print(f"Extracted first {duration} seconds to: {output_wav}")

audio_files = [
    "warbly_weird.wav"
]
for file in audio_files:
    # extract_meaningful_audio(f"farts_new/{file}", f"{file}.wav", duration=6.0)
    extract_first_n_seconds(f"farts_new/{file}", f"{file}.wav", duration=5.0)

