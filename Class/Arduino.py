import serial

class Arduino:
    def __init__(self, portx,portz):
        self.portx = portx
        self.portz = portz
        self.baudrate = 9600
        self.serialx = None
        self.serialz = None

    def connect(self):
        self.serialx = serial.Serial(self.portx, self.baudrate)
        self.serialz = serial.Serial(self.portz, self.baudrate)

    def disconnect(self):
        if self.serialx:
            self.serialx.close()
            self.serialx = None
        if self.serialz:
            self.serialz.close()
            self.serialz = None

    def send_step(self, step):
        if self.serialx:
            self.serialx.write(step.encode())
        if self.serialz:
            self.serialz.write(step.encode())