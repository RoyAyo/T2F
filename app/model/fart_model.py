from app.model.Audiowave import AudioWave
from app.model.Concatenate import ConcatenateFarts
from app.model.Diffwave import DiffWave
from phonemizer import phonemize

from app.twitter.bot import get_tweet_text


class FartModel:
    def __init__(self, generator="Concatenate"):
        self.generator = generator
        
        self.concatenator = ConcatenateFarts()

    def text_to_phenome(self, text):
        words = [word for word in text.split(" ")]
        phonemes = []
        for word in words:
            phoneme = phonemize(word, language="en-gb", backend="espeak", strip=True)
            phonemes.append(phoneme)
        return phonemes
    
    def generate_audio_from_tweet(self, tweet):
        message = get_tweet_text(tweet)
        if not message:
            raise Exception("Unable to load tweet...")
        return self.generate_audio(message)

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
    
    def generate_vae_fart(self, text):
        pass

    def generate_video_fart(self, tweet):
        pass