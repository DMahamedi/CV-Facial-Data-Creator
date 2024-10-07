import os
import cv2
from utils import *

def get_images_from_video(video_path: str, new_class_name: str, class_id: int) -> None:
    '''
        Make the data using an existing video
        :params:
            video_path: path to the video
            new_class_name: name of the new class we are annotating
            class_id: class id of the base class
        :returns:
            None
    '''
    folder_path = f'./Data/{new_class_name}/'
    make_output_file(folder_path)
    image_folder_path = folder_path + 'Images/'
    make_output_file(image_folder_path)
    counter = get_max_counter(image_folder_path, 'jpg')

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}.")
        exit()
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        frame_filename = get_file_name(counter, class_id) + '.jpg'
        cv2.imwrite(frame_filename, frame)        
        frame_number += 1

    cap.release()