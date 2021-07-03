from PIL import Image
import numpy as np
import multi_hand_tracker_v1 as mht
import plot_hand

img_path = "../og.png"
img = Image.open(img_path)
img = np.array(img)

palm_model_path = "./models/palm_detection_without_custom_op.tflite"
landmark_model_path = "./models/hand_landmark.tflite"
anchors_path = "./data/anchors.csv" 

# Initialise detector
# the independent flag makes the detector process each image independently
detector = mht.MultiHandTracker3D(palm_model_path, landmark_model_path, anchors_path, box_enlarge = 1.5, 
                 box_shift = 0.2, 
                 max_hands = 12,
                 detect_hand_thres = 0.5,
                 detect_keypoints_thres = 0.3,
                 iou_thres = 0.4)

# Get predictions
kp_list, box_list = detector(img)

# Plot predictions
plot_hand.plot_img(img, kp_list, box_list)
