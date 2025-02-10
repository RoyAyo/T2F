from app.model.ai import AI
from phonemizer import phonemize
from phonemizer.separator import Separator
import pyphen
import numpy as np
import librosa
import soundfile as sf
import re

ai = AI()

def combine_audios(audios):
    if len(audios) == 0:
        return
    combined_audio = np.array([])
    for audio in audios:
        y, sr = librosa.load(f"farts_/{audio}.wav", sr=44100)
        if combined_audio.size == 0:
            combined_audio = y
        else:
            # Define crossfade duration (in samples)
            crossfade_duration = int(0.1 * sr)  # 70ms crossfade

            # Apply linear crossfade
            fade_out = np.linspace(1, 0, crossfade_duration)
            fade_in = np.linspace(0, 1, crossfade_duration)

            combined_audio[-crossfade_duration:] *= fade_out
            y[:crossfade_duration] *= fade_in

            # Combine the sounds with crossfade
            combined_audio = np.concatenate([combined_audio, y])
    
    # Save the combined sound
    # sf.write(f"{"".join(audios)}.wav", combined_audio, sr)
    return combined_audio, sr


def generate_audio(text):
    farts = ai.get_fart_audios_to_user(text)
    audios, sr = combine_audios(farts)

    sf.write(f"{"".join(audios)}.wav", audios, sr)
    return audios, sr