import cv2

cap = cv2.VideoCapture(0)
print("type something")

while True:
    ret, frame = cap.read()
    cv2.imshow("test", frame)
    k = cv2.waitKey(1)

    if k > 0:
        print(k)

    if k == 113:
        break
