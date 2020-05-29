import wave
import mutagen.mp3
import os
import pygame


def get_sample_rate(sound_file_path):
    type_of_file = sound_file_path.split(".")[-1]

    if type_of_file == "mp3":
        mp3 = mutagen.mp3.MP3(sound_file_path)
        sampling_rate = mp3.info.sample_rate
    elif type_of_file == "wav":
        file_wav = wave.open(sound_file_path)
        sampling_rate = file_wav.getframerate()

    return sampling_rate


def play_sound(sound_file_path, wait_to_finish=False):
    sampling_rate = get_sample_rate(sound_file_path)

    pygame.mixer.init(frequency=sampling_rate)
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

    if wait_to_finish:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


def get_available_sounds(button_name, gdrive_path="/home/pi/mnt/gdrive"):
    """
    Input: button_name - must match one of teh folders in the google drive
    Output: list of files in that directory
    """
    sound_file_paths = []
    folder_path = f"{gdrive_path}/{button_name}"
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        sound_file_paths.extend([f"{dirpath}/{name}" for name in filenames])
    return sound_file_paths
