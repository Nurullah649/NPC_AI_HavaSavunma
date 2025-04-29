from Class.GUI import CameraApp
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    # Uygulama başlatma
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())