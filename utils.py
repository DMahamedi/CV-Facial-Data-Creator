import re
import os


def get_max_counter(folder_path: str, filetype: str = 'jpg') -> int:
    '''
        Find the number of images or annotations which have already been created for a given new class
            Since the annotations copy their respective image names, and since images and annotations are named
            in order of creation, this has the effect of determining at what number to start labeling new images or annotations
        :params:
            folder_path: path to the folder containing either the images or annotations
            filetype: either 'jpg' or 'txt, determines whether we are checking annotations or images
        returns:
            int: index of the last image or annotation created
    '''
    pattern = re.compile(rf"^\d{{2}}_(\d{{6}})\.{filetype}$")
    max_counter = -1

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            counter = int(match.group(1))
            max_counter = max(max_counter, counter)
    return max_counter

def make_output_file(folder_path: str) -> None:
    '''
        Make the output folder if it does not already exist
        :params:
            folder_path: path of the folder to create
    '''
    os.makedirs(os.path.dirname(folder_path), exist_ok=True)