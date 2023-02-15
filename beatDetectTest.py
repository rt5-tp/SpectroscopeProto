import pygame
import librosa
import librosa.display
import numpy as np


audio_path = 'Cascada - Everytime We Touch (Official Video).wav'
y, sr = librosa.load(audio_path)
onset_env = librosa.onset.onset_strength(y, sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

color = (255, 255, 255)  # white
flash_duration = 50  # milliseconds
last_flash_time = 0
onset_index = 0

pygame.mixer.init()
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Flash the color if there is an onset within the flash duration
    if onset_index < len(onset_times) and onset_times[onset_index] * 1000 <= current_time + flash_duration:
        color = tuple(np.random.randint(0, 256, 3))
        onset_index += 1
        last_flash_time = current_time

    # Clear the screen and draw the color
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, color, pygame.Rect(100, 100, 300, 300))

    # Update the display and tick the clock
    pygame.display.flip()
    clock.tick(60)

    # Wait until the next flash time
    while pygame.time.get_ticks() < last_flash_time + flash_duration:
       pass