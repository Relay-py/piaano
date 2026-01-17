import cv2
import os
import numpy as np
import mediapipe as mp
from dotenv import load_dotenv
import time


def initialize_mediapipe_hands(num_frames: int):
    # Initializes mediapipe hands models

    if num_frames > 2:
        raise ValueError("Maximum 2 frames permitted")
    
    mp_hands = mp.solutions.hands
    
    hands = []
    for _ in range(num_frames):
        hand = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        hands.append(hand)

    return hands



def main():
    load_dotenv()

    hands_top, hands_front = initialize_mediapipe_hands(2)

    top_cap = cv2.VideoCapture(0)
    top_ip = os.environ.get('FRONT_IP')
    top_port = os.environ.get('PORT')
    top_url = f"http://{top_ip}:{top_port}/video"

    front_cap = cv2.VideoCapture(0)
    front_ip = os.environ.get('FRONT_IP')
    front_port = os.environ.get('PORT')
    front_url = f"http://{front_ip}:{front_port}/video"


    while True:
        if top_cap.isOpened():
            _, top_frame = top_cap.read()

            if top_frame is None:
                continue

            cv2.imshow("Top Frame", top_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



        


if __name__ == "__main__":
    main()