from app.model.ai import AI
from phonemizer.separator import Separator
import numpy as np
import librosa
import soundfile as sf

ai = AI()

class Concatenate:
    def combine_audios(self, audios):
        if len(audios) == 0:
            return None, None

        combined_audio = np.array([])
        sr = 44100

        for audio in audios:
            if audio == "":
                silence = np.zeros(int(sr * 0.3))
                if combined_audio.size == 0:
                    combined_audio = silence
                else:
                    combined_audio = np.concatenate([combined_audio, silence])
                continue 

            y, sr = librosa.load(f"farts_/{audio}.wav", sr=sr)

            if combined_audio.size == 0:
                combined_audio = y
            else:
                crossfade_duration = int(0.08 * sr)  

                fade_out = np.linspace(1, 0, crossfade_duration)
                fade_in = np.linspace(0, 1, crossfade_duration)

                combined_audio[-crossfade_duration:] *= fade_out
                y[:crossfade_duration] *= fade_in

                combined_audio = np.concatenate([combined_audio, y])

        return combined_audio, sr

    def generate_audio(self, text):
        farts = ai.get_fart_audios_to_user(text)
        print("farts")
        audios, sr = self.combine_audios(farts)

        sf.write(f"{"".join(audios)}.wav", audios, sr)
        return audios, sr