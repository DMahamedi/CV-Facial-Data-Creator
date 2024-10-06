import config
from get_image_data import *
from annotate_data import *



collect_data(config.NEW_CLASS_NAME, config.CLASS_TYPE, config.CLASS_ID,
             config.NUM_FRAME_SAMPLES, config.IMGSZ_W, config.IMGSZ_H)
annotate_images(config.NEW_CLASS_NAME, 'person', './Models/yolov10m.pt', 0)