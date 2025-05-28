import serial
import time

def adım_gonder(adim):
    adim=(adim*1.3)
    try:
        arduino= serial.Serial('/dev/ttyUSB0', 9600)

        time.sleep(2)  # Arduino'nun açılması/reseti için bekle

        veri = f"{adim}\n"
        arduino.write(veri.encode())  # Veriyi gönder
        print(f"{adim} adım gönderildi.")

        arduino.close()
    except serial.SerialException as e:
        print(f"Seri bağlantı hatası: {e}")

