import cv2
import os
from ultralytics import YOLO
from utils import *

def get_images_to_annotate(image_folder_path: str, label_folder_path: str) -> list[str]:
    max_counter = get_max_counter(label_folder_path, 'txt')
    annotation_images = []
    annotation_names = []
    for filename in os.listdir(image_folder_path):
        file_counter = int(filename.split('_')[-1][:-4])
        if file_counter > max_counter:
            annotation_images.append(image_folder_path + filename)
            annotation_names.append(filename[:-4])
    return annotation_images, annotation_names

def annotate_images(class_name: str, class_type: str = 'person', model_name: str = './Models/yolov10m.pt', class_id: int = 0) -> None:
    model = YOLO(model_name)

    annotation_labels_path = f'./Data/{class_name}/Labels/'
    annotation_images_path = f'./Data/{class_name}/Images/'
    make_output_file(annotation_labels_path)
    min_counter = get_max_counter(annotation_labels_path)
    annotation_images, annotation_names = get_images_to_annotate(annotation_images_path, annotation_labels_path)

    results = model(annotation_images, device='cuda:0', half = True, classes=[class_id], max_det=1)

    for i in range(len(results)):
        output_path = f'{annotation_labels_path}{annotation_names[i]}.txt'
        results[i].save_txt(output_path)
