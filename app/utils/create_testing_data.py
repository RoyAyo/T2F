from pydub import AudioSegment
import threading
from threading import Semaphore

def process_phoneme(phoneme, semaphore = ""):
    try:
        sounds = []
        # print(phoneme)
        for p in phoneme.strip().split("."):
            if p == "":
                continue
            sound = AudioSegment.from_wav(f"fart/fart_{p}.wav")
            sounds.append(sound)
        combined = sum(sounds)
        combined.export(f"fart_test/{phoneme}.wav", format="wav")
        print(f"Created {phoneme}.wav successfully!")
    except Exception as e:
        print(e)
    finally:
        semaphore.release()

# Read phoneme file paths from a text file
with open("public/phonemes.txt", "r") as file:
    phonemes = [line.strip() for line in file.readlines()]

    print(len(phonemes))

    # Create a semaphore to limit the number of concurrent threads
    semaphore = Semaphore(4)

    # # Create and start threads for each phoneme
    threads = []
    for phoneme in phonemes:
        semaphore.acquire()
        thread = threading.Thread(target=process_phoneme, args=(phoneme, semaphore))
        threads.append(thread)
        thread.start()

    # # Wait for all threads to complete
    for thread in threads:
        thread.join()