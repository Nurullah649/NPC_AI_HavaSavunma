import cv2

# Kamera başlatma
cap = cv2.VideoCapture(4)  # 0, varsayılan kamerayı temsil eder

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    # Kareyi okuma
    ret, frame = cap.read()
    
    if not ret:
        print("Kare okunamadı!")
        break
    
    # Kameradaki görüntüyü gösterme
    cv2.imshow("Kamera", frame)
    
    # 'q' tuşuna basıldığında çıkma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve tüm pencereleri kapat
cap.release()
cv2.destroyAllWindows()
