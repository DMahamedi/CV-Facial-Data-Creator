import depthai as dai
import cv2
import os
import re

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

def get_max_counter(folder_path: str) -> int:
    pattern = re.compile(r"^\d{2}_(\d{6})\.jpg$")
    max_counter = 0

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            counter = int(match.group(1))
            max_counter = max(max_counter, counter)
    return max_counter

def collect_data(class_name: str, class_type: str = 'person',
                class_id: int = 0, num_samples: int = 250, imgsz_w: int = 1920, imgsz_h: int = 1080) -> None:
    
    pipeline = make_pipeline(imgsz_w, imgsz_h)

    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        max_counter = 0
        folder_path = f"./Data/{class_name}/"
        if os.path.isdir(folder_path):
            max_counter = get_max_counter(folder_path)
            print('x')
        else:
            os.makedirs(os.path.dirname(folder_path), exist_ok=True)
        counter = max_counter
        while counter < max_counter + num_samples:
            videoIn = video.get()
            counter += 1
            filename = f"{class_id:02d}_{counter:06d}.jpg"
            cv2.imwrite(folder_path + filename, videoIn.getCvFrame())
            # Get BGR frame from NV12 encoded video frame to show with opencv
            # Visualizing the frame on slower hosts might have overhead
            cv2.imshow("video", videoIn.getCvFrame())
            if cv2.waitKey(1) == ord('q'):
                break