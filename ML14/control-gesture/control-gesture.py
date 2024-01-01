import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import screen_brightness_control as sbc

# MENU
def main():
    while True:
        print("-------- MENU --------")
        print("1. Chỉnh âm lượng")
        print("2. Chỉnh độ sáng")
        print("0. Thoát")
        a = int(input("Chọn chức năng:"))
        if a == 0:
            break
        if a == 1:
            print('Chạy chức năng chỉnh âm lượng...')
            volumeControl()
        if a == 2:
            print('Chạy chức năng chỉnh độ sáng...')
            brightnessControl()


# Chuẩn bị camera, bàn tay và chức năng vẽ
def cameraAndHand():
    # Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Bàn tay
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()

    # Vẽ
    mpDraw = mp.solutions.drawing_utils

    return cap, mpHands, hands, mpDraw

# Chỉnh âm lượng
def volumeControl():
    cap, mpHands, hands, mpDraw = cameraAndHand()

    # Truy cập vào loa của thiết bị thông qua pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Vị trí 0% của thanh âm lượng
    volbar=400
    # Phần trăm âm lượng
    volper=0

    # Lấy ra giá trị thấp và cao nhất của âm lượng máy
    volMin,volMax = volume.GetVolumeRange()[:2]

    while True:
        # Đọc ảnh chụp được từ camera
        _,img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        key = cv2.waitKey(1)
        # Kiểm tra nút được ấn
        mode = select_mode(key, 0)
        if mode == -1:
            print('Thoát chỉnh âm lượng')
            break
        
        # Xử lý ảnh để nhận diện bàn tay
        results = hands.process(imgRGB)

        cv2.putText(img,f"Nhan ESC de thoat",(500,30),cv2.FONT_ITALIC,1,(0, 255, 98),3)

        # Lưu trữ các vị trí trên bàn tay và vẽ đường nối
        h, w, _ = img.shape
        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id,lm in enumerate(handlandmark.landmark):
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    lmList.append([id,cx,cy]) #adding to the empty list 'lmList'
                mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

        # Xử lý chuyển đổi khoảng cách giữ 2 ngón tay ra âm lượng
        if lmList != []:
            x1,y1 = lmList[4][1],lmList[4][2]  # ngón cái
            x2,y2 = lmList[8][1],lmList[8][2]  # ngón trỏ

            cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED) # Các thông số lần lượt (ảnh, vị trí x y, bán kính, rgb)
            cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

            # Tính khoảng cách giữa 2 ngón tay bằng công thức tính cạnh huyền
            length = hypot(x2-x1,y2-y1)

            # Chuyển đổi từ khoảng cách giữa 2 ngón tay ra âm lượng, thanh âm lượng, phần trăm âm lượng
            # bằng phương pháp nội suy tuyến tính
            vol = np.interp(length,[30, 220],[volMin,volMax])
            volbar=np.interp(length,[30, 220],[400,150])
            volper=np.interp(length,[30, 220],[0,100])
            print(vol,int(length))

            # Đặt giá trị âm lượng vừa tính được cho thiết bị
            volume.SetMasterVolumeLevel(vol, None)

            # Vẽ thanh âm lượng
            cv2.rectangle(img,(50,150),(85,400),(0,0,255),4) # ảnh, vị trí bắt đầu, vị trí kết thúc, rgb, độ dày
            cv2.rectangle(img,(50,int(volbar)),(85,400),(0,0,255),cv2.FILLED)
            cv2.putText(img,f"{int(volper)}%",(45,130),cv2.FONT_ITALIC,1,(0, 255, 98),3)

        cv2.imshow('Chỉnh âm lượng',img)

    cap.release()
    cv2.destroyAllWindows()

# Kiểm tra nút được ấn
def select_mode(key, mode):
    if key == 27: # ESC
        mode = -1
    return mode

# Chỉnh độ sáng
def brightnessControl():
    cap, mpHands, hands, Draw = cameraAndHand()

    while True:
        # Đọc ảnh chụp được từ camera
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Kiểm tra nút được ấn
        key = cv2.waitKey(1)
        mode = select_mode(key, 0)
        if mode == -1:
            print('Thoát chỉnh độ sáng')
            break
            
        # Xử lý ảnh để nhận diện bàn tay
        Process = hands.process(imgRGB)

        cv2.putText(img,f"Nhan ESC de thoat",(500,30),cv2.FONT_ITALIC,1,(0, 255, 98),3)

        # Lưu trữ các vị trí trên bàn tay và vẽ đường nối
        height, width, _ = img.shape
        landmarkList = []
        if Process.multi_hand_landmarks:
            for handlm in Process.multi_hand_landmarks:
                for _id, landmarks in enumerate(handlm.landmark):
                    x, y = int(landmarks.x*width), int(landmarks.y*height)
                    landmarkList.append([_id, x, y])
                
                Draw.draw_landmarks(img, handlm, mpHands.HAND_CONNECTIONS)

        # Xử lý chuyển đổi khoảng cách giữ 2 ngón tay ra độ sáng
        if landmarkList != []:
            # ngón cái
            x1, y1 = landmarkList[4][1], landmarkList[4][2]
            # ngón trỏ
            x2, y2 = landmarkList[8][1], landmarkList[8][2]

            cv2.circle(img, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Tính khoảng cách giữa 2 ngón tay bằng công thức tính cạnh huyền
            L = hypot(x2-x1, y2-y1)

            # Chuyển đổi từ khoảng cách giữa 2 ngón tay ra độ sáng, thanh độ sáng
            # bằng phương pháp nội suy tuyến tính
            b_level = np.interp(L, [30, 220], [0, 100])
            b_level_bar = np.interp(L, [30, 220], [400, 150])
            print(b_level)

            sbc.set_brightness(int(b_level), display=0)
            cv2.rectangle(img,(50,150),(85,400),(0,0,255),4) # ảnh, vị trí bắt đầu, vị trí kết thúc, rgb, độ dày
            cv2.rectangle(img,(50,int(b_level_bar)),(85,400),(0,0,255),cv2.FILLED)
            cv2.putText(img,f"{int(b_level)}%",(45,130),cv2.FONT_ITALIC,1,(0, 255, 98),3)

        cv2.imshow('Chỉnh độ sáng', img)

    cap.release()
    cv2.destroyAllWindows()

# Phóng to video

main()