import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread("C:\\Users\\bianc\\RecapIt\\static\\images\\Jessie.png")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#print(pytesseract.image_to_string(img))
#print(pytesseract.image_to_boxes(img))
heightimg, widthimg, a = img.shape
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
    b = b.split()
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(img, (x, heightimg-y), (w, heightimg-h), (0, 0, 255), 3)
    cv2.putText(img, b[0], (x, heightimg-y+25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
cv2.imshow('Result', img)
cv2.waitKey(0)


