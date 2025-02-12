from app.model.Audiowave import AudioWave
from app.model.Concatenate import ConcatenateFarts
from app.model.Diffwave import DiffWave

class FartModel:
    def __init__(self, generator="Concatenate"):
        self.generator = generator
        
        self.concatenator = ConcatenateFarts()
    
    def generate_audio_from_tweet(self, tweet):
        return self.concatenator.generate_sentiment_audio(tweet)

    def generate_audio(self, text):
        if self.generator == "Audiowave":
            return self.generate_audiowave_fart(text)
        elif self.generator == "Diffwave":
            return self.generate_diffwave_fart(text)
        else:
            return self.generate_concatenate_fart(text)

    def generate_concatenate_fart(self, text):
        buffer = self.concatenator.generate_audio(text)
        return buffer

    def generate_audiowave_fart(self, text):
        audiowave = AudioWave()
        audio_path = audiowave.generate_audio(text)
        return audio_path
    
    def generate_diffwave_fart(self, text):
        diffwave = DiffWave()
        audio_path = diffwave.generate_audio(text)
        return audio_path