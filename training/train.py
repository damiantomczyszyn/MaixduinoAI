import sys
sys.path.append('/content/aXeleRate')

from axelerate import setup_training, setup_inference, setup_evaluation

import matplotlib

#!gdown https://drive.google.com/uc?id=1-2jYfTRPX4kSUTL5SUQVxwHKjBclrBTA  #pre-trained model
#!unzip --qq pascal_20_detection.zip
print(sys.path)
from axelerate.networks.common_utils.augment import visualize_detection_dataset as vdd

vdd(img_folder='pascal_20_detection/imgs_validation', ann_folder='pascal_20_detection/anns_validation', num_imgs=10, img_size=320, augment=True)


import tensorflow as tf


config = {
        "model":{
            "type":                 "Detector",
            "architecture":         "MobileNet1_0",
            "input_size":           [224, 320],
            "anchors":              [[[0.76120044, 0.57155991], [0.6923348, 0.88535553], [0.47163042, 0.34163313]],
                                    [[0.33340788, 0.70065861], [0.18124964, 0.38986752], [0.08497349, 0.1527057 ]]],
            "labels":               ["person", "bird", "cat", "cow", "dog", "horse", "sheep", "aeroplane", "bicycle", "boat", "bus", "car", "motorbike", "train","bottle", "chair", "diningtable", "pottedplant", "sofa", "tvmonitor"],
            "obj_thresh" : 		    0.7,
            "iou_thresh" : 		    0.5,
            "coord_scale" : 		  1.0,
            "object_scale" : 		  3.0,
            "no_object_scale" : 	1.0
        },
        "weights" : {
            "full":   				  "",
            "backend":   		    "imagenet"
        },
        "train" : {
            "actual_epoch":         50,
            "train_image_folder":   "pascal_20_detection/imgs",
            "train_annot_folder":   "pascal_20_detection/anns",
            "train_times":          1,
            "valid_image_folder":   "pascal_20_detection/imgs_validation",
            "valid_annot_folder":   "pascal_20_detection/anns_validation",
            "valid_times":          1,
            "valid_metric":         "recall",
            "batch_size":           32,
            "learning_rate":        1e-3,
            "saved_folder":   		F"/content/drive/MyDrive/projects/pascal20_yolov3",
            "first_trainable_layer": "",
            "augmentation":				  True,
            "is_only_detect" : 		  False
        },
        "converter" : {
            "type":   				[]
        }
}

from keras import backend as K
K.clear_session()
model_path = setup_training(config_dict=config)


from keras import backend as K
K.clear_session()
setup_inference(config, model_path)
