import pyrealsense2 as rs
import cv2
import numpy as np
import os

# RealSense pipeline başlatılır
pipe = rs.pipeline()
config = rs.config()

# Kamera çözünürlüğünü ve FPS ayarlarını belirleyin
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)  # 1280x720 çözünürlük, 30 FPS
profile = pipe.start()

# FPS ve çözünürlük değerlerini alalım
fps = profile.get_stream(rs.stream.color).fps()  # fps() methodunu çağırarak değeri alıyoruz
width = profile.get_stream(rs.stream.color).as_video_stream_profile().width()
height = profile.get_stream(rs.stream.color).as_video_stream_profile().height()

print(f"Görüntü çözünürlüğü: {width}x{height}")
print(f"FPS: {fps}")

# 'frames' klasörünü oluşturuyoruz
output_folder = '/home/nurullah/NPC-AI_HavaSavunma/frames'
os.chmod(output_folder, 0o666)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

frame_count = 0  # Frame sayısını takip etmek için değişken

try:
    while True:  # 100 frame al, isterseniz değiştirebilirsiniz
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Renkli görüntü numpy array'e dönüştürülür
        color_image = np.asanyarray(color_frame.get_data())

        # Görüntüyü BGR'den RGB'ye çeviriyoruz
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Frame numarasını artırıyoruz
        frame_count += 1

        # Frame'i RGB olarak dosya olarak kaydediyoruz
        frame_filename = f"{output_folder}/frame_{frame_count:04d}.png"  # PNG formatı kullanalım
        cv2.imwrite(frame_filename, color_image_rgb)  # Frame'i kaydet (RGB olarak)

        # Dosyanın yazma izinlerini değiştiriyoruz
        os.chmod(frame_filename, 0o666)  # Yazma izni veriyoruz

        # Görüntüyü RGB formatında ekranda göster
        cv2.imshow("Camera Feed (RGB)", color_image_rgb)

        # 'q' tuşuna basıldığında çıkış yapar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Çıkış yapılıyor...")
            break  # Çıkış yap

finally:
    # Kamera bağlantısını kes ve video kaydını kapat
    pipe.stop()
    cv2.destroyAllWindows()
