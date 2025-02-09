from app.model.Audiowave import AudioWave
from app.model.Diffwave import DiffWave
from phonemizer import phonemize
# from phonemizer


class FartModel:
    def __init__(self, generator="Concatenate"):
        self.generator = generator

    def text_to_phenome(self, text):
        words = [word for word in text.split(" ")]
        phonemes = []
        for word in words:
            phoneme = phonemize(word, language="en-gb", backend="espeak", strip=True)
            phonemes.append(phoneme)
        return phonemes

    def generate_fart(self, text):
        
        if self.generator == "Audiowave":
            return self.generate_audiowave_fart(text)
        elif self.generator == "Diffwave":
            return self.generate_diffwave_fart(text)
        else:
            # default to the concatenator
            return "Invalid generator"
        
    def concatenate_fart_phenomes(self):
        pass

    def generate_audiowave_fart(self, text):
        audiowave = AudioWave()
        audio_path = audiowave.generate_audio(text)
        return audio_path
    
    def generate_diffwave_fart(self, text):
        diffwave = DiffWave()
        audio_path = diffwave.generate_audio(text)
        return audio_path
    
    def generate_vae_fart(self, text):
        pass