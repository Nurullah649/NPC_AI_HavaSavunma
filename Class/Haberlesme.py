import serial
import time

class Arduino:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # SADECE İLK BAĞLANTIDA Arduino'nun resetlenmesi için bekle
            print(f"Arduino ile {self.port} portunda bağlantı kuruldu.")
            return True
        except serial.SerialException as e:
            print(f"Seri bağlantı hatası: {e}")
            self.serial_connection = None
            return False

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Arduino bağlantısı kesildi.")

    def send_data(self, data):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                message = f"{data}\n"
                self.serial_connection.write(message.encode())
                # print(f"Gönderildi: {data}") # Hata ayıklama için açılabilir
                return True
            except Exception as e:
                print(f"Veri gönderme hatası: {e}")
                return False
        else:
            print("Bağlantı kapalı, veri gönderilemiyor.")
            return False

    def is_connected(self):
        return self.serial_connection and self.serial_connection.is_open
