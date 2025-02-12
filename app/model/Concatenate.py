import io
import numpy as np
import librosa
import soundfile as sf
from app.data_model.expressions import Expressions
from app.model.ai import AI
from app.twitter.bot import get_tweet_text
from app.utils.helper import convert_string_text_to_array
from app.settings.cache import redisClient

class ConcatenateFarts:
    def __init__(self):
        self.ai = AI()
        self.sample_rate = 44100
        self.crossfade_duration = int(0.08 * self.sample_rate)
        self.silence_duration = int(self.sample_rate * 0.3)

    def combine_audios(self, audios):
        if not audios:
            return None, None

        combined_audio = np.array([])

        for audio_path in audios:
            audio = audio_path.value.strip()
            if audio == "silence" or audio not in Expressions._value2member_map_:
                print(f"audio {audio} not found")
                silence = np.zeros(self.silence_duration)
                combined_audio = np.concatenate([combined_audio, silence]) if combined_audio.size else silence
                continue

            y, sr = librosa.load(f"farts_new/{audio}.wav", sr=self.sample_rate)
            combined_audio = self._crossfade_and_concatenate(combined_audio, y)

        sf.write("combined_audio.wav", combined_audio, self.sample_rate, format="WAV")
        return combined_audio, self.sample_rate

    def _crossfade_and_concatenate(self, combined_audio, new_audio):
        if combined_audio.size == 0:
            return new_audio

        fade_out = np.linspace(1, 0, self.crossfade_duration)
        fade_in = np.linspace(0, 1, self.crossfade_duration)

        combined_audio[-self.crossfade_duration:] *= fade_out
        new_audio[:self.crossfade_duration] *= fade_in

        return np.concatenate([combined_audio, new_audio])

    def create_fart_buffer(self, audio, sr):
        buffer = io.BytesIO()
        sf.write(buffer, audio, sr, format="WAV")
        buffer.seek(0)
        return buffer

    def generate_audio(self, text):
        farts_text = self.ai.get_fart_audios_to_user(text)
        print("farts_text", farts_text)
        farts = convert_string_text_to_array(farts_text)
        audios, sr = self.combine_audios(farts)
        print(audios)
        buffer = self.create_fart_buffer(audios, sr)
        print(buffer, "buffer")
        return buffer

    def generate_sentiment_audio(self, tweet):
        print(tweet, "tweet")
        cached_tweet = redisClient.get(tweet)
        if cached_tweet:
            return io.BytesIO(cached_tweet)

        text = get_tweet_text(tweet)
        if not text:
            raise Exception("Unable to load tweet...")

        sentiment = self.ai.sentiment_analysis(text)
        farts = sentiment.get("expressions")
        print("expressions", farts)
        audios, sr = self.combine_audios(farts)
        buffer = self.create_fart_buffer(audios, sr)
        redisClient.set(tweet, buffer.getvalue())
        return buffer
