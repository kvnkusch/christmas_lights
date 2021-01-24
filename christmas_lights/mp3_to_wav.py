from os import path
import sys
from pydub import AudioSegment


def mp3_to_wav(name):
    src = f"data/{name}.mp3"
    dst = f"data/{name}.wav"

    print(f"Converting {src} to {dst}")

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nProvide name of mp3 file (w/o extension) to convert to wav\n")
    else:
        mp3_to_wav(sys.argv[1])
