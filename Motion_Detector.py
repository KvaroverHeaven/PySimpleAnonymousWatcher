import datetime
import imutils
import threading
import requests
import numpy
import cv2

prevFrame = None
video = cv2.VideoCapture(0)
detectedTime = None

while True:
    text = "Safe"
    check, frame = video.read()
    frame = imutils.resize(frame, width=1200)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if (prevFrame is None):
        prevFrame = gray
        continue

    diffFrame = cv2.absdiff(prevFrame, gray)
    threshold = cv2.threshold(diffFrame, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=5)
    contours = cv2.findContours(
        threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for c in contours:
        if cv2.contourArea(c) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Detected!"

        if (detectedTime is None or (datetime.datetime.now() - detectedTime).seconds > 10):
            detectedTime = datetime.datetime.now()
            extension = detectedTime.strftime("%Y-%m-%d %H:%M:%S") + ".jpg"
            #cv2.imwrite('C:/Users/bakad/OneDrive/Python Project/' + extension, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            #requests.post('https://yaoweb.azurewebsites.net/test.php', files={'file': open('./Images/' + extension, "rb")})
            #t = threading.Thread(target=lambda location, time, image: requests.post("https://maker.ifttt.com/trigger/line/with/key/bkx-fUXwG4fuqYjlqplda5WXZIbAmyWbuW4dRnbGWLb",
            #    data={"value1": location, "value2": time, "value3": image}), args=("407", detectedTime.strftime("%Y-%m-%d %H:%M:%S"), "https://yaoweb.azurewebsites.net/Images" + extension), )
            #t.start()
            #prevFrame = gray

    cv2.putText(frame, "Room Status: {}".format(text), (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("Current Time: %Y-%m-%d %H:%M:%S"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.imshow("gray", gray)
    #cv2.imshow("threshold", threshold)
    #cv2.imshow("diffFrame", diffFrame)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(50)
    prevFrame = gray

    if (key == ord('q')):
        break
video.release()
cv2.destroyAllWindows()
