# from pydub import AudioSegment
# from pydub.silence import split_on_silence

# # Load the full fart audio file
# long_fart_audio = AudioSegment.from_wav("fart_sound/100_FART.wav")

# fart_clips = split_on_silence(
#     long_fart_audio, 
#     min_silence_len=500,
#     silence_thresh=-40
# )

# print(f"Found {len(fart_clips)} farts")

# for i, fart in enumerate(fart_clips):
#     fart.export(f"fart_sounds/fart_{i+1}.wav", format="wav")
#     print(f"Saved: fart_sounds/fart_{i+1}.wav")