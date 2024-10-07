import os

def rewrite_annotation_label(annotation_filepath: str, new_class_id: int) -> None:
    with open(annotation_filepath, 'r+') as f:
        line = f.readline()
        values = line.strip().split()
        values[0] = str(new_class_id)
        f.seek(0) #note this is meant for one-line file annotations
        f.write(' '.join(values))

def rewrite_annotation_class(class_name: str, new_class_id: int) -> None:
    annotation_folder_path = f'./Data/{class_name}/Labels/'
    
    for annotation_file in os.listdir(annotation_folder_path):
        rewrite_annotation_label(annotation_folder_path+annotation_file, new_class_id)
    