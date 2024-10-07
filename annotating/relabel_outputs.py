import os

def rewrite_annotation_label(annotation_filepath: str, new_class_id: int) -> None:
    '''
        Relabel the model-assigned class id to a custom class id for a specific annotation
        :params:
            annotation_filepath: str path to a specific annotation .txt file
            new_class_id: new class id to give the annotation
        :returns:
            None
    '''
    with open(annotation_filepath, 'r+') as f:
        line = f.readline()
        values = line.strip().split()
        values[0] = str(new_class_id)
        f.seek(0) #note this is meant for one-line file annotations
        f.write(' '.join(values))

def rewrite_annotation_class(class_name: str, new_class_id: int) -> None:
    '''
        Relabel all of a new class types annotations to have a unique class id
        Needed for converting generic classes (i.e. person) to something unique (like a specific individual)
        :params:
            class_name: name of the new class we want to label
            new_class_id: the class id we want to give the new class
        :returns:
            None
    '''
    annotation_folder_path = f'./Data/{class_name}/Labels/'
    
    for annotation_file in os.listdir(annotation_folder_path):
        rewrite_annotation_label(annotation_folder_path+annotation_file, new_class_id)
    