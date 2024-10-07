import depthai as dai
import cv2
import os
import re
from utils import *

def make_pipeline(imgsz_w: int = 1920, imgsz_h: int = 1080) -> dai.Pipeline:
    '''
        Create DepthAI pipeline
        :params:
            imgsz_w: int image width (pixels)
            imgsz_h: int image height (pixels)
        :returns;
            dai.Pipeline: depthAI Pipeline object to run on an OAK device
    '''
    pipeline = dai.Pipeline()

    camRgb = pipeline.createColorCamera()
    xoutVideo = pipeline.createXLinkOut()
    
    xoutVideo.setStreamName("video")

    # Properties
    camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setVideoSize(imgsz_w, imgsz_h)

    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)

    # Linking
    camRgb.video.link(xoutVideo.input)

    return pipeline

def collect_data(new_class_name: str, class_type: str = 'person',
                class_id: int = 0, num_samples: int = 250,
                imgsz_w: int = 1920, imgsz_h: int = 1080) -> None:
    '''
        Use OAK camera to collect images for annotating
        :params:
            new_class_name: the name of the new class we are annotating
            class_type: base class that the new class comes from (e.g. a specific individual would have class_type == 'person')
            class_id: class id of the base class
            num_samples: number of images to collect before stopping
            imgsz_w: int width of images to save (pixels)
            imgsz_h: int height of images to save (pixels)
        :returns:
            None

        Note that the imgsz_w and imgsz_h can be used to speed up the program and model inference later
    '''
    
    pipeline = make_pipeline(imgsz_w, imgsz_h)

    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        max_counter = 0
        folder_path = f"./Data/{new_class_name}/Images/"
        make_output_file(folder_path)
        max_counter = get_max_counter(folder_path, 'jpg')
        counter = max_counter
        
        while counter < max_counter + num_samples:
            videoIn = video.get()
            counter += 1
            filename = get_file_name(counter, class_id) + '.jpg'
            cv2.imwrite(folder_path + filename, videoIn.getCvFrame())
            cv2.imshow("video", videoIn.getCvFrame())
            if cv2.waitKey(1) == ord('q'):
                break
        
        cv2.destroyAllWindows()