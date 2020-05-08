# from pydub import AudioSegment
# from pydub.playback import play

# sound = AudioSegment.from_wav('/home/pi/the_metal.mp3')
# play(sound)

# from playsound import playsound

# playsound('/home/pi/the_metal.mp3')


import pygame

pygame.mixer.init()
pygame.mixer.music.load('/home/pi/the_metal.mp3')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy(): 
    pygame.time.Clock().tick(10)