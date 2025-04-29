import sys
import time
import cv2
import numpy as np
import pyrealsense2 as rs

from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextBrowser
)
from .Chapter1 import Chapter1
from .Chapter2 import Chapter2
from .Chapter3 import Chapter3
class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        # Arka plan resmi için Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-image: url(data/GUI_images/background.png);
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        self.setWindowTitle('Kamera Görüntü Uygulaması (RealSense)')
        self.setGeometry(100, 100, 800, 600)

        # RealSense pipeline başlatma
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        try:
            self.pipeline.start(config)
        except Exception as e:
            raise IOError(f"RealSense pipeline açılamadı: {e}")

        # Model ve realtime kontrol flag
        self.model = None
        self.realtime = False

        # Arayüzü oluştur
        self.init_ui()

        # Frame güncelleme timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        button_layout = QVBoxLayout()
        video_and_text_layout = QHBoxLayout()

        # Buton metinleri ve ikon dosya yollarını eşleyin
        actions = {
            'HER ŞEYİ İMHA ET': 'data/GUI_images/chapter1.png',
            'SADECE DÜŞMANI İMHA ET': 'data/GUI_images/chapter2.png',
            'ANGAJMAN GÖREVİ': 'data/GUI_images/chapter3.png',
            'KAPAT': 'data/GUI_images/quit.png'
        }
        size = 240
        for text, icon_path in actions.items():
            btn = QPushButton('')
            pixmap = QPixmap(icon_path).scaled(size, size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(QSize(size, size))
            btn.setFlat(True)
            btn.setToolTip(text)
            if text == 'HER ŞEYİ İMHA ET':
                btn.clicked.connect(self.birinci_gorev)
            elif text == 'SADECE DÜŞMANI İMHA ET':
                btn.clicked.connect(self.ikinci_gorev)
            elif text == 'KAPAT':
                btn.clicked.connect(self.kapat)
            else:
                btn.clicked.connect(self.angajman_gorev)
            button_layout.addWidget(btn)

        # Metin alanı
        self.video_and_text = QTextBrowser()
        self.video_and_text.setMinimumSize(350, 600)

        # Video görüntü alanı
        self.video_frame = QLabel()
        self.video_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        video_and_text_layout.addWidget(self.video_frame)
        video_and_text_layout.addWidget(self.video_and_text)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(video_and_text_layout)

    def zaman_hesapla(self):
        tm = time.localtime()
        return f"{tm.tm_hour:02d}:{tm.tm_min:02d}:{tm.tm_sec:02d}"

    def birinci_gorev(self):
        self.video_and_text.append(f"[{self.zaman_hesapla()}] Birinci göreve (realtime) geçildi.")
        if self.model is None:
            self.model = Chapter1()
        self.realtime = True


    def ikinci_gorev(self):
        self.video_and_text.append(f"[{self.zaman_hesapla()}] İkinci göreve geçildi. Realtime tespit durduruldu.")
        self.realtime = False

    def angajman_gorev(self):
        self.video_and_text.append(f"[{self.zaman_hesapla()}] Angajman görevine geçildi. Realtime tespit durduruldu.")
        self.realtime = False

    def kapat(self):
        self.video_and_text.append(f"[{self.zaman_hesapla()}] Uygulama kapatılıyor...")
        self.close()

    def update_frame(self):
        # RealSense'ten yeni kare al
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return

        # BGR formatında NumPy dizisi
        frame_bgr = np.asanyarray(color_frame.get_data())

        # Gerçek zamanlı tespit isteniyorsa
        if self.realtime and self.model:
            results = self.model.predict(frame_bgr)[0]
            for box, cls, conf in zip(results.boxes.xyxy,
                                      results.boxes.cls,
                                      results.boxes.conf):
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{self.model.model.names[int(cls)]} {conf:.2f}"
                cv2.putText(frame_bgr, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Artı işareti
        h, w, ch = frame_bgr.shape
        cx, cy = (w // 2)-23, (h // 2)+80
        size = 25
        cv2.line(frame_bgr, (cx - size, cy), (cx + size, cy), (255, 255, 255), 2)
        cv2.line(frame_bgr, (cx, cy - size), (cx, cy + size), (255, 255, 255), 2)

        # RGB'ye çevir ve QImage olarak göster
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        bytes_per_line = ch * w
        qimg = QImage(frame_rgb.data, w, h, bytes_per_line,
                      QImage.Format.Format_RGB888)
        self.video_frame.setPixmap(QPixmap.fromImage(qimg))


    def closeEvent(self, event):
        try:
            self.pipeline.stop()
        except:
            pass
        super().closeEvent(event)

