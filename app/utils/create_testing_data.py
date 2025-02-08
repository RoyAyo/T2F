from pydub import AudioSegment

# Load individual phoneme sounds
sound1 = AudioSegment.from_wav("fart/fart_h.wav")
sound2 = AudioSegment.from_wav("fart/fart_ə.wav")
sound3 = AudioSegment.from_wav("fart/fart_l.wav")
sound4 = AudioSegment.from_wav("fart/fart_ə.wav")

# Concatenate them
combined = sound1 + sound2 + sound3 + sound4

# Save as a new file
combined.export("helə.wav", format="wav")

print("Created æk.wav successfully!")
