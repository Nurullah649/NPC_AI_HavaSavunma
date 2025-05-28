import sys
import time
import cv2
import numpy as np
from .Haberlesme import *

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
    """Sadece Y eksenindeki piksel farkını (ΔY) döndüren sürüm."""

    def __init__(self):
        super().__init__()
        # Arka plan
        self.setStyleSheet(
            """
            QWidget {
                background-image: url(data/GUI_images/background.png);
                background-repeat: no-repeat;
                background-position: center;
            }
            """
        )
        self.setWindowTitle("Kamera Görüntü Uygulaması (OpenCV)")
        self.showFullScreen()

        # Kamera
        self.camera_index = 4
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise IOError(
                f"Kamera açılmadı. Kamera indexi {self.camera_index} kontrol edin."
            )
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Model / durum
        self.model: Chapter1 | None = None
        self.realtime = False

        # UI
        self.init_ui()

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        button_layout = QVBoxLayout()
        video_and_text_layout = QHBoxLayout()

        actions = {
            "HER ŞEYİ İMHA ET": "data/GUI_images/chapter1.png",
            "SADECE DÜŞMANI İMHA ET": "data/GUI_images/chapter2.png",
            "ANGAJMAN GÖREVİ": "data/GUI_images/chapter3.png",
            "KAPAT": "data/GUI_images/quit.png",
        }
        size = 240
        for text, icon_path in actions.items():
            btn = QPushButton("")
            pixmap = QPixmap(icon_path).scaled(
                size,
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation,
            )
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(QSize(size, size))
            btn.setFlat(True)
            btn.setToolTip(text)
            if text == "HER ŞEYİ İMHA ET":
                btn.clicked.connect(self.birinci_gorev)
            elif text == "SADECE DÜŞMANI İMHA ET":
                btn.clicked.connect(self.ikinci_gorev)
            elif text == "KAPAT":
                btn.clicked.connect(self.kapat)
            else:
                btn.clicked.connect(self.angajman_gorev)
            button_layout.addWidget(btn)

        self.video_and_text = QTextBrowser()
        self.video_and_text.setMinimumSize(350, 600)

        self.video_frame = QLabel()
        self.video_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        video_and_text_layout.addWidget(self.video_frame)
        video_and_text_layout.addWidget(self.video_and_text)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(video_and_text_layout)

    # ------------------------------------------------------------------
    # Yardımcılar
    # ------------------------------------------------------------------
    @staticmethod
    def zaman_hesapla():
        tm = time.localtime()
        return f"{tm.tm_hour:02d}:{tm.tm_min:02d}:{tm.tm_sec:02d}"

    def birinci_gorev(self):
        self.video_and_text.append(
            f"[{self.zaman_hesapla()}] Birinci göreve (realtime) geçildi."
        )
        if self.model is None:
            self.model = Chapter1()
        self.realtime = True

    def ikinci_gorev(self):
        self.video_and_text.append(
            f"[{self.zaman_hesapla()}] İkinci göreve geçildi. Realtime tespit durduruldu."
        )
        self.realtime = False

    def angajman_gorev(self):
        self.video_and_text.append(
            f"[{self.zaman_hesapla()}] Angajman görevine geçildi. Realtime tespit durduruldu."
        )
        self.realtime = False

    def kapat(self):
        self.video_and_text.append(f"[{self.zaman_hesapla()}] Uygulama kapatılıyor...")
        self.close()

    # ------------------------------------------------------------------
    # Çekirdek döngü
    # ------------------------------------------------------------------
    def update_frame(self):
        # Kare al
        ret, frame_bgr = self.cap.read()
        if not ret:
            return

        h, w, ch = frame_bgr.shape
        cx, cy = (w // 2) - 25, (h // 2) + 173  # crosshair

        if self.realtime and self.model:
            results = self.model.predict(frame_bgr)[0]
            for box, cls, conf in zip(
                results.boxes.xyxy, results.boxes.cls, results.boxes.conf
            ):
                x1, y1, x2, y2 = map(int, box)

                # Nesnenin merkezi (X gerekmediği için sadece Y kullanacağız)
                center_y = int((y1 + y2) / 2)

                # Y eksenindeki piksel farkı (pozitif: aşağı, negatif: yukarı)
                dy = center_y - cy

                # Görsel çizimler
                cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{self.model.model.names[int(cls)]} {conf:.2f}"
                cv2.putText(
                    frame_bgr,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )

                # Y farkını göster
                cv2.putText(
                    frame_bgr,
                    f"ΔY:{dy:+} px",
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                )
                time.sleep(1)
                adım_gonder(dy)

                # Crosshair ile nesne merkezi arasında çizgi
                center_x = int((x1 + x2) / 2)  # sadece çizmek için X yine lazım
                cv2.line(frame_bgr, (cx, cy), (center_x, center_y), (255, 255, 255), 2)

        # Crosshair
        size = 25
        cv2.line(frame_bgr, (cx - size, cy), (cx + size, cy), (255, 255, 255), 2)
        cv2.line(frame_bgr, (cx, cy - size), (cx, cy + size), (255, 255, 255), 2)

        # Göster
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        qimg = QImage(
            frame_rgb.data,
            w,
            h,
            ch * w,
            QImage.Format.Format_RGB888,
        )
        self.video_frame.setPixmap(QPixmap.fromImage(qimg))


    # ------------------------------------------------------------------
    def closeEvent(self, event):
        try:
            self.cap.release()
        except Exception:
            pass
        super().closeEvent(event)
