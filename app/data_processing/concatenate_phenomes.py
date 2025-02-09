from pydub import AudioSegment
import threading
from threading import Semaphore

def process_phoneme(phoneme, semaphore):
    try:
        sounds = []
        for p in list(phoneme):
            sound = AudioSegment.from_wav(f"fart/fart_{p}.wav")
            sounds.append(sound)
        combined = sum(sounds)
        combined.export(f"word_farts/{phoneme}.wav", format="wav")
        print(f"Created {phoneme}.wav successfully!")
    finally:
        semaphore.release()

# Read phoneme file paths from a text file
with open("phonemes.txt", "r") as file:
    phonemes = [line.strip() for line in file.readlines()]

    # Create a semaphore to limit the number of concurrent threads
    semaphore = Semaphore(4)

    # Create and start threads for each phoneme
    threads = []
    for phoneme in phonemes:
        semaphore.acquire()
        thread = threading.Thread(target=process_phoneme, args=(phoneme, semaphore))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()