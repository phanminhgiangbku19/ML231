import cv2
import imutils
import ssl
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import os
import time
import math

ssl._create_default_https_context = ssl._create_unverified_context

# Load modal phat hien guong mat trong khung anh
prototxtPath = r"/Users/macbook/documentOfKhanh/Mask_Detect/face_detector/deploy.prototxt"
weightsPath = r"/Users/macbook/documentOfKhanh/Mask_Detect/face_detector/res10_300x300_ssd_iter_140000.caffemodel"

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
# Load modal nhan dien deo khau trang da duoc training vao giai thuat
maskNet = load_model("bikini_detector_1999_images_128_dense_08.model")


def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    blob = cv2.dnn.blobFromImage(frame, 1.0, (256, 256), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()
    print(detections.shape)

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (256, 256))
            cv2.imwrite('test-resize.jpg', face)
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((1, 1, 1, 1))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
        print(preds)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)


def DetectImage(path, fileName):
    # Path to video file
    vidObj = cv2.VideoCapture(path)
    # frameRate = vidObj.get(5)  # frame rate
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    org = (50, 50)
    # fontScale
    fontScale = 1
    # Blue color in BGR
    color1 = (0, 0, 255)
    # Blue color in BGR
    thickness = 2
    # Used as counter variable
    count = 0
    countSensitiveFrame = 0
    # checks whether frames were extracted
    success = 1

    save_path = "/Users/macbook/documentOfKhanh/Mask_Detect/static/" + fileName
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    while success:
        try:
            if (countSensitiveFrame > 25):
                return False
                break
            # frameId = vidObj.get(1)
            count += 1
            # vidObj object calls read
            # function extract frames
            success, image = vidObj.read()

            # if (frameId % math.floor(frameRate) == 0):
            # frame = imutils.resize(image, width=400)
            frame = cv2.resize(image, (256, 256))

            (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

            for (box, pred) in zip(locs, preds):
                (porn, withoutPorn) = pred
                if porn > withoutPorn and porn > 0.95:
                    frame = cv2.putText(frame, '18+', org, font,
                                        fontScale, color1, thickness, cv2.LINE_AA)
                    imageName = str(count) + \
                        time.strftime("%Y-%m-%d-%H:%M") + '_porn' + '.jpg'
                    cv2.imwrite(os.path.join(save_path, imageName), frame)
                    print("Phát hiện hình ảnh 18+")
                    countSensitiveFrame += 1
                    break

        except Exception as err:
            print(f"Unexpected {err}, {type(err)}")

            return 'error reading video'

    return True

# Driver Code
# if __name__ == '__main__':
#     DetectImage(
#         "/Users/macbook/Downloads/v10025g50000clcop7vog65lcd8ll050.mov")
