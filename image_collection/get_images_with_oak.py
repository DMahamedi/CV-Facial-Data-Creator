import depthai as dai
import cv2
import os
import re
from utils import *

def make_pipeline(imgsz_w: int = 1920, imgsz_h: int = 1080) -> dai.Pipeline:
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

def collect_data(class_name: str, class_type: str = 'person',
                class_id: int = 0, num_samples: int = 250, imgsz_w: int = 1920, imgsz_h: int = 1080) -> None:
    
    pipeline = make_pipeline(imgsz_w, imgsz_h)

    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        max_counter = 0
        folder_path = f"./Data/{class_name}/Images/"
        make_output_file(folder_path)
        max_counter = get_max_counter(folder_path, 'jpg')
        counter = max_counter
        
        while counter < max_counter + num_samples:
            videoIn = video.get()
            counter += 1
            filename = f"{class_id:02d}_{counter:06d}.jpg"
            cv2.imwrite(folder_path + filename, videoIn.getCvFrame())
            cv2.imshow("video", videoIn.getCvFrame())
            if cv2.waitKey(1) == ord('q'):
                break
        
        cv2.destroyAllWindows()