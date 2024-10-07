import cv2
import os


def get_bounding_box(annotation_filepath: str) -> list:
    '''
        Read the bounding box from a specific annotation
        :params:
            annotation_filepath: path to the annotation file
    '''
    box = []
    with open(annotation_filepath, 'r') as f:
        line = f.readline().strip().split(' ')
        class_id, x_center, y_center, width, height = int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4])
        box.append([class_id, x_center, y_center, width, height])
    return box

def filter_annotations(new_class_name: str) -> None:
    '''
        Used to view each synthetic data annotation for a specific new class and verify whether it is usable for training
            Use 'x' to specify/delete bad data, 'q' to quit early, press any other key to continue
        :params:
            new_class_name: str name of the new class being labeled
    '''
    folder_path = f'./Data/{new_class_name}/'
    images_path = f'{folder_path}/Images/'
    labels_path = f'{folder_path}/Labels/'

    for annotation_filename in os.listdir(labels_path):
        image_name = annotation_filename[:-4] #filename=XXX_XXXXXX.txt, cut the '.txt'
        image_filepath = images_path + image_name + '.jpg'
        annotation_filepath = labels_path + annotation_filename

        if not os.path.exists(image_filepath):
            os.remove(annotation_filepath)
        else:
            image = cv2.imread(image_filepath)
            bounding_boxes = get_bounding_box(annotation_filepath)
            img_height, img_width, _ = image.shape
            for box in bounding_boxes:
                class_id, x_center, y_center, width, height = box[0],box[1],box[2],box[3],box[4]
                
                left = int((x_center - (width / 2)) * img_width)
                top = int((y_center - (height / 2)) * img_height)
                right = int((x_center + (width / 2)) * img_width)
                bottom = int((y_center + (height / 2)) * img_height)

                cv2.putText(image, f'{new_class_name}',
                        (left,top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                        (255,0,0), 2, cv2.LINE_AA)

                cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)

            cv2.putText(image, f'Image {annotation_filename[:-4]}',
                        (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                        (0,0,255), 2, cv2.LINE_AA)

            cv2.imshow(f'Image with bounding box', image)
            key = cv2.waitKey(0)  # Wait for a key press to close the image window or delete image

            if key == ord('x'):
                os.remove(annotation_filepath)
                os.remove(image_filepath)
            elif key == ord('q'):
                break

    cv2.destroyAllWindows()