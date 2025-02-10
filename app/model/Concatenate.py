import io
from app.model.ai import AI
from app.utils.helper import convert_string_text_to_array
import numpy as np
import librosa
import soundfile as sf
from app.model.data.sounds import fart_sounds

ai = AI()

class ConcatenateFarts:
    def combine_audios(self, audios):
        if len(audios) == 0:
            return None, None

        combined_audio = np.array([])
        sr = 44100

        for audio_path in audios:
            audio = audio_path.strip()
            if audio == "silence" or audio not in fart_sounds:
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
    
    def create_fart_buffer(self, audio, sr):
        buffer = io.BytesIO()
        sf.write(buffer, audio, sr, format="WAV")
        buffer.seek(0)
        return buffer

    def generate_audio(self, text):
        farts_text = ai.get_fart_audios_to_user(text)
        print("farts_text", farts_text)
        farts = convert_string_text_to_array(farts_text)
        audios, sr = self.combine_audios(farts)
        print(audios)
        buffer = self.create_fart_buffer(audios, sr)
        print(buffer, "buffer")
        return buffer