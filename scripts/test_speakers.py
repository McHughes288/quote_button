import pygame
import wave
import mutagen.mp3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--soundfile",
    "-s",
    action="store",
    default="/home/pi/mnt/gdrive/Brian/the_bart_of_technology.wav",
    dest="soundfile",
)
args = parser.parse_args()

type_of_file = args.soundfile.split(".")[-1]

if type_of_file == "mp3":
    mp3 = mutagen.mp3.MP3(args.soundfile)
    sampling_rate = mp3.info.sample_rate
elif type_of_file == "wav":
    try:
        file_wav = wave.open(args.soundfile)
        sampling_rate = file_wav.getframerate()
    except:
        sampling_rate=16000

pygame.mixer.init(frequency=sampling_rate)
pygame.mixer.music.load(args.soundfile)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)