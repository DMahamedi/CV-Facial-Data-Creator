import cv2
import os
from ultralytics import YOLO
from utils import *
from annotating.relabel_outputs import rewrite_annotation_class_id

def get_images_to_annotate(image_folder_path: str, label_folder_path: str) -> list[str]:
    '''
        Finds the newest images which were not previously annotated, in case of adding to existing data
        :params:
            image_folder_path: path to the images being annotated
            label_folder_path: path to the folder for annotation outputs
        :returns:
            list[str]: list of which images to annotate (leaving out ones with existing annotations)
    '''
    max_counter = get_max_counter(label_folder_path, 'txt')
    annotation_images = []
    annotation_names = []
    for filename in os.listdir(image_folder_path):
        file_counter = int(filename.split('_')[-1][:-4])
        if file_counter > max_counter:
            annotation_images.append(image_folder_path + filename)
            annotation_names.append(filename[:-4])
    return annotation_images, annotation_names

def annotate_images(new_class_name: str, model_name: str = './Models/yolov10m.pt', base_class_id: int = 0, new_class_id: int = None) -> None:
    '''
        Use a trained model to identify the base class, relabel the predictions to be the new class type
        :params:
            new_class_name: str name of the new class we want to annotate
            model_name: model to use to get the class_type predictions
            base_class_id: class id of the base class that the new class is 'derived' from
            new_class_id: id to give the new class we are labeling. Optional.
        :returns:
            None
    '''
    model = YOLO(model_name)

    annotation_labels_path = f'./Data/{new_class_name}/Labels/'
    annotation_images_path = f'./Data/{new_class_name}/Images/'
    make_output_file(annotation_labels_path)
    min_counter = get_max_counter(annotation_labels_path)
    annotation_images, annotation_names = get_images_to_annotate(annotation_images_path, annotation_labels_path)

    results = model(annotation_images, device='cuda:0', half = True, classes=[base_class_id], max_det=1)

    for i in range(len(results)):
        output_path = f'{annotation_labels_path}{annotation_names[i]}.txt'
        results[i].save_txt(output_path)
    
    if new_class_id:
        rewrite_annotation_class_id(new_class_name, new_class_id)
