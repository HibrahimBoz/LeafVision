import sys
import os
import time
import matplotlib.pyplot as plt

# OpenCV DLL dizinini sisteme tanıt (Temiz Mimari)
opencv_bin_dir = "C:/Users/Halil/Downloads/Programs/opencv/build/x64/vc16/bin"
if os.path.exists(opencv_bin_dir):
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(opencv_bin_dir)

# Kök dizini ve modül yollarını ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Kendi yazdığımız C++ modülünü içe aktarıyoruz!
try:
    import leaf_vision
except ImportError:
    print("Hata: leaf_vision modülü bulunamadı. Lütfen önce derleme yapın.")
    sys.exit(1)

def main():
    # Assets klasöründeki resmi kullan
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../assets/leaf.jpg'))

    print("C++ motoru calistiriliyor...")
    start_time = time.time()

    # C++ fonksiyonunu çağır! (7 asamali pipeline dondurur)
    pipeline = leaf_vision.process_leaf(image_path)

    print(f"Islem tamamlandi. Sure: {time.time() - start_time:.4f} saniye")
    print(f"Pipeline asamalari: {list(pipeline.keys())}")

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for ax, (step_name, img) in zip(axes.flat, pipeline.items()):
        ax.imshow(img, cmap=None if img.ndim == 3 else 'gray')
        ax.set_title(step_name)
        ax.axis('off')
    for ax in axes.flat[len(pipeline):]:
        ax.axis('off')

    fig.suptitle('Yaprak Analizi Pipeline (C++ Backend)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()