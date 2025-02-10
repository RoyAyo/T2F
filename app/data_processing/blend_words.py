# import nltk
# from nltk.corpus import cmudict
# import string
# from phonemizer import phonemize
# from phonemizer.separator import Separator
# import numpy as np
# import librosa
# import soundfile as sf


# # Download CMU Pronouncing Dictionary if not available
# nltk.download('cmudict')

# # Load CMU Pronouncing Dictionary
# d = cmudict.dict()

# def count_syllables(pronunciation):
#     return sum(1 for phoneme in pronunciation if any(char.isdigit() for char in phoneme))

# def is_valid_word(word):
#     return word.isalpha()  # Ensure only alphabetic words are included

# # Find words with exactly 1 syllable and 2 or 3 letters
# one_syllable_words = [word for word in d if count_syllables(d[word][0]) == 1 and is_valid_word(word) and 2 == len(word)]

# print(one_syllable_words)
# print(len(one_syllable_words))

# def blend_sound(sound1, sound2):

#     # Load two audio files
#     try:
#         y1, sr1 = librosa.load(f"fart_perfect/fart_{sound1}.wav", sr=44100)
#         y2, sr2 = librosa.load(f"fart_perfect/fart_{sound2}.wav", sr=44100)

#         # Ensure both have the same sampling rate
#         # assert sr1 == sr2

#         # Define crossfade duration (in samples)
#         crossfade_duration = int(0.07 * sr1)  # 50ms crossfade

#         # Apply linear crossfade
#         fade_out = np.linspace(1, 0, crossfade_duration)
#         fade_in = np.linspace(0, 1, crossfade_duration)

#         y1[-crossfade_duration:] *= fade_out
#         y2[:crossfade_duration] *= fade_in

#         # Combine the sounds with crossfade
#         blended_audio = np.concatenate([y1, y2])

#         # Save the blended sound
#         sf.write(f"fart_merged/{sound1}{sound2}.wav", blended_audio, sr1)
#     except:
#         print(f"Failed to blend {sound1} and {sound2}")

# # find phenomes for each word and return only the uniques ones
# for word in one_syllable_words:
#     phoneme = phonemize(word, backend="espeak", language="en", separator=Separator(phone='_'), strip=True)
#     print(phoneme)
#     phoneme_split = phoneme.split("_")
#     if len(phoneme_split) > 1:
#         blend_sound(phoneme_split[0], phoneme_split[1])
#     print(phoneme_split)
