import os
from pathlib import Path

FRAME_DIR = Path("dataset/valid/images")

frames = sorted([
    str(FRAME_DIR / f)
    for f in os.listdir(FRAME_DIR)
    if f.lower().endswith((".jpg",".jpeg",".png"))
])

frame_index = 0

def get_next_frame():

    global frame_index

    frame = frames[frame_index]

    frame_index += 1
    if frame_index >= len(frames):
        frame_index = 0

    return frame