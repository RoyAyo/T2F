from typing import Concatenate
from app.model.Audiowave import AudioWave
from app.model.Diffwave import DiffWave
from phonemizer import phonemize


class FartModel:
    def __init__(self, generator="Concatenate"):
        self.generator = generator
        self.audiowave = AudioWave()
        self.diffwave = DiffWave()
        self.concatenator = Concatenate()

    def text_to_phenome(self, text):
        words = [word for word in text.split(" ")]
        phonemes = []
        for word in words:
            phoneme = phonemize(word, language="en-gb", backend="espeak", strip=True)
            phonemes.append(phoneme)
        return phonemes

    def generate_audio(self, text):
        if self.generator == "Audiowave":
            return self.generate_audiowave_fart(text)
        elif self.generator == "Diffwave":
            return self.generate_diffwave_fart(text)
        else:
            return self.generate_concatenate_fart(text)
        
    def generate_concatenate_fart(self, text):
        audio, sr, path = self.concatenator.generate_audio(text)
        return audio, sr, path

    def generate_audiowave_fart(self, text):
        audio_path = self.audiowave.generate_audio(text)
        return audio_path
    
    def generate_diffwave_fart(self, text):
        audio_path = self.diffwave.generate_audio(text)
        return audio_path
    
    def generate_vae_fart(self, text):
        pass