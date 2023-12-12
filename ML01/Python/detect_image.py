import cv2
import imutils
import ssl
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import os
import time

ssl._create_default_https_context = ssl._create_unverified_context

# Load modal phat hien guong mat trong khung anh
prototxtPath = r"/Users/macbook/documentOfKhanh/Mask_Detect/face_detector/deploy.prototxt"
weightsPath = r"/Users/macbook/documentOfKhanh/Mask_Detect/face_detector/res10_300x300_ssd_iter_140000.caffemodel"

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# Load modal nhan dien deo khau trang da duoc training vao giai thuat
maskNet = load_model("bikini_detector_1000_images_128_dense_08.model")


def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
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


def DetectImage():
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (50, 50)

    # fontScale
    fontScale = 1

    # Blue color in BGR
    color1 = (0, 0, 255)
    # Blue color in BGR
    color2 = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    path1 = '/Users/macbook/documentOfKhanh/google_download/test/result-06-12/unsafe'
    path2 = '/Users/macbook/documentOfKhanh/google_download/test/result-06-12/safe'

    for images in os.listdir("/Users/macbook/documentOfKhanh/google_download/test/images"):
        newimage = cv2.imread(os.path.join(
            "/Users/macbook/documentOfKhanh/google_download/test/images", images))
        # newimage = cv2.imread(
        #     "/Users/macbook/Downloads/with_porn/330376922_234372445594225_7684086608547761110_n.jpg")
        print(images)

        cv2.imwrite('test-image.png', newimage)
        frame = imutils.resize(newimage, width=256)

        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

        for (box, pred) in zip(locs, preds):
            (porn, withoutPorn) = pred
            if porn > withoutPorn and porn > 0.9:
                frame = cv2.putText(frame, '18+', org, font,
                                    fontScale, color1, thickness, cv2.LINE_AA)
                imageName = images + \
                    time.strftime("%Y-%m-%d-%H:%M") + '_porn' + '.png'
                # cv2.imwrite(frame, imageName)
                cv2.imwrite(os.path.join(path1, imageName), frame)
                print("Đây là hình ảnh 18+")
                break
            else:
                frame = cv2.putText(frame, 'Normal', org, font,
                                    fontScale, color2, thickness, cv2.LINE_AA)
                imageName = images + \
                    time.strftime("%Y-%m-%d-%H:%M") + '_porn' + '.png'
                cv2.imwrite(os.path.join(path2, imageName), frame)

                print("Đây là hình ảnhh bình thường")
                break


if __name__ == "__main__":
    DetectImage()
