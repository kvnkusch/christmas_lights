import sys
import pygame
import time
from random import random
from scipy.io.wavfile import read
from scipy.signal import stft
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SLOT_COUNT = 5
SLOT_HEIGHT = 75
MIN_SLOT_WIDTH = 100

STEPS_PER_SECOND = 8
step_time = 1000 / STEPS_PER_SECOND

window_width = (SLOT_COUNT + 1) * MIN_SLOT_WIDTH
window_height = SLOT_COUNT * SLOT_HEIGHT

rects = {
    i: (
        (window_width - MIN_SLOT_WIDTH * (i + 1)) / 2,
        SLOT_HEIGHT * i,
        MIN_SLOT_WIDTH * (i + 1),
        SLOT_HEIGHT,
    )
    for i in range(SLOT_COUNT)
}


def get_random_step():
    return [round(random()) for _ in range(SLOT_COUNT)]


def make_get_next_step(f, t, Zxx):
    f_i = Zxx.shape[0] / SLOT_COUNT
    t_factor = t[-1] * STEPS_PER_SECOND * 0.1

    freq_means = [
        abs(Zxx[round(i * f_i) : round((i + 1) * f_i), :].sum()) / t_factor
        for i in range(SLOT_COUNT)
    ]

    def func(last_t_index, next_t_index):
        return [
            1
            if abs(
                Zxx[
                    round(i * f_i) : round((i + 1) * f_i), last_t_index:next_t_index
                ].sum()
            )
            > freq_means[i]
            else 0
            for i in range(SLOT_COUNT)
        ]

    return func


def draw_next_step(window, next_step):
    window.fill(BLACK)
    for i, is_on in enumerate(next_step):
        if is_on:
            pygame.draw.rect(window, YELLOW, rects[i])
    pygame.display.flip()


def run(name):
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    window.fill(BLACK)

    src = f"data/{name}.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(src)
    pygame.mixer.music.play()

    Fs, data = read(src)
    data = data[:, 0]

    f, t, Zxx = stft(data, fs=Fs)
    get_next_step = make_get_next_step(f, t, Zxx)

    step = 0
    start_time = int(round(time.time() * 1000))
    next_time = 0
    last_t_index = 0
    t *= 1000

    run = True
    while run:
        cur_time = int(round(time.time() * 1000)) - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if next_time <= cur_time:
            next_t_index = np.argmax(t > next_time)
            next_step = get_next_step(last_t_index, next_t_index)

            draw_next_step(window, next_step)

            step += 1
            next_time += step_time
            last_t_index = next_t_index


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nProvide name of wav file (w/o extension)\n")
    else:
        run(sys.argv[1])
