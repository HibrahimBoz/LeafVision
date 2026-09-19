# LeafVision

C++/OpenCV çekirdekli, Python API'li yaprak sınırı tespiti ve segmentasyon motoru. Bir MATLAB prototipinden başlayıp C++ + pybind11 + FastAPI hibrit mimarisine evrilmiş bir görüntü işleme projesi.

## Evrim

1. **MATLAB prototipi** (`docs/archive/Leaf Boundary.m`) — RGB kanal ayrıştırma, basit yeşil eşikleme (`g - r/2 - b/2`), morfolojik temizlik.
2. **C++17 + OpenCV çekirdeği** (`src/core/leaf_boundary.cpp`) — LAB renk uzayı + Excess Green Index ile renk ayrıştırma, Otsu eşikleme, distance transform ve watershed ile üst üste binen yaprakların ayrılması. [pybind11](extern/pybind11) ile `leaf_vision` adlı bir Python modülü olarak derlenir.
3. **FastAPI servisi** (`src/api/server.py`) — görüntü yükleme, pipeline'ın 7 aşamasını base64 JPEG olarak döndürme; karşısında sürükle-bırak web arayüzü (`src/api/static/index.html`).

Ayrıntılı yol haritası için [docs/proje_plani.md](docs/proje_plani.md), C++ algoritma planı için [docs/cpp_improvement_plan.md](docs/cpp_improvement_plan.md), sürüm geçmişi için [docs/release_notes.txt](docs/release_notes.txt).

## Mimari

```
leaf.jpg ──► FastAPI (/process) ──► leaf_vision.pyd (pybind11)
                                          │
                                          ▼
                              C++/OpenCV pipeline (leaf_boundary.cpp)
                              1_original → 2_color_mask → 3_cleaned_mask
                              → 4_distance_map → 5_foreground_seeds
                              → 6_watershed_markers → 7_final_edges
                                          │
                                          ▼
                          base64 JPEG dizisi ──► web arayüzü (static/index.html)
```

## Gereksinimler

- Windows + Visual Studio (MSVC toolset) veya CMake + Ninja + uyumlu bir C++17 derleyicisi
- [OpenCV 4.x](https://opencv.org/releases/) (Windows build'i indirilip bir dizine çıkarılmış olmalı)
- Python 3.13+ (proje `env/` altında bir sanal ortam kullanır)

## Kurulum

```bash
# 1. Sanal ortamı oluştur ve bağımlılıkları kur
py -3.13 -m venv env
env\Scripts\pip install -r requirements.txt

# 2. OpenCV'nin nerede olduğunu bildir (varsayılan yol bu makineye özeldir)
set OpenCV_DIR=C:\path\to\opencv\build
set OPENCV_BIN_DIR=C:\path\to\opencv\build\x64\vc16\bin

# 3. C++ çekirdeğini derle (leaf_vision.pyd'yi proje köküne kopyalar)
cmake -G Ninja -S src\core -B src\core\out\build\x64-Debug
cmake --build src\core\out\build\x64-Debug --target leaf_vision
```

Visual Studio kullanıyorsanız `launch.vs.json`'daki hazır konfigürasyonlarla (Derle / API'yi başlat / Script'i test et) aynı adımları IDE üzerinden çalıştırabilirsiniz.

## Çalıştırma

```bash
# API sunucusu
env\Scripts\python src\api\server.py
# -> http://127.0.0.1:8000

# C++ motorunu doğrudan test et (pipeline'ı görselleştirir)
env\Scripts\python src\scripts\main.py

# API'ye karşı duman testi (sunucu ayrıca çalışıyor olmalı)
env\Scripts\python src\scripts\test_ui.py
```

## Proje yapısı

```
src/core/     C++17 pybind11 modülü (leaf_boundary.cpp, CMakeLists.txt)
src/api/      FastAPI servisi + statik web arayüzü
src/scripts/  Yerel test/demo betikleri
extern/       Vendored pybind11 (ayrıca klonlanır, gitignore'lu)
assets/       Örnek görüntü (leaf.jpg)
docs/         Yol haritası, mimari notları, MATLAB arşivi
fleet_management_plan.md   Çok robotlu filo yönetimi vizyonu (ileri aşama, henüz uygulanmadı)
```

## Durum

Algoritma çekirdeği (LAB/ExG renk ayrıştırma + watershed segmentasyonu) ve tek-görüntü FastAPI servisi çalışır durumda. Veri seti bazlı doğruluk ölçümü (CVPPP/PlantVillage), doku/hastalık analizi, donanım entegrasyonu ve filo yönetimi henüz uygulanmadı — güncel durum için [docs/proje_plani.md](docs/proje_plani.md)'ye bakın.
