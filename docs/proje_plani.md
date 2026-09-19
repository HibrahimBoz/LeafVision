# LeafVision: Akıllı Tarım ve Otonom Robot Ekosistemi Yol Haritası

Bu belge, projenin basit bir prototipten endüstriyel "Embodied AI" (Fizikselleşmiş Yapay Zeka) seviyesine uzanan gelişimini ve otonom tarım robotu vizyonunu içermektedir.

## 🌟 Projenin Evrimi (Nereden Nereye?)
* **Başlangıç (MATLAB Prototiplenmesi):** Sadece matematiksel matris işlemleriyle renk uzayı hesabı yapıp yaprak sınırlarını bulan temel konsept (`Leaf Boundary.m`).
* **Mevcut Durum (Hibrit Motor):** C++17 ve OpenCV kullanılarak sıfırdan yazılmış, saniyede onlarca kare (FPS) işleyebilen; Pybind11 ile Python'a bağlanmış yüksek performanslı bir arka uç mimarisi.
* **Uç Bilişim (Edge Computing):** Çekirdek algoritmanın FastAPI ile internete açılıp Edge Server (Uç Sunucu) mantığına oturtulması aşaması.

## 🚀 Yol Haritası ve Fazlar

## 1. Faz: Algoritma Çekirdeği (Tamamlandı)
* **Araçlar:** C++ ve OpenCV
* **Hedef:** Donanımdan tamamen bağımsız (Windows, Linux, ARM, x86 fark etmeksizin çalışabilen) kapalı bir kutu yazmak.
* **Detaylar:** 
  * Görüntü (matris) girer, işlem yapılır, sonuç çıkar. Sistem diske dokunmaz, sadece RAM üzerinde olabildiğince hızlı çalışır.
  * **Modern Yaklaşımlar:** HSV/LAB renk uzayı dönüşümleri, Otsu eşikleme, Canny Edge Detection ve üst üste binen yaprakları ayırmak için Watershed algoritması gibi sağlam (robust) açık kaynak teknikleri bu çekirdekte uygulanır.

## 2. Faz: Test, Değerlendirme ve Prototipleme Katmanı (Tamamlandı)
* **Araçlar:** Python, Pybind11, Standart Veri Setleri
* **Hedef:** Yazdığımız C++ motorunu test ortamında (Windows/Mac) hızlıca çalıştırmak ve performansını bilimsel olarak ölçmek.
* **Detaylar:** 
  * C++ kodu her defasında baştan derlenmeden, Python üzerinden çağrılarak algoritmaların doğruluğu (hata payları vb.) ölçülecek.
  * **Veri Akışı:** C++ `cv::Mat` formatı ile Python `numpy.ndarray` arasında veri kopyalamadan (zero-copy) hızlı geçiş sağlanacak.
  * **Test ve Metrikler:** CVPPP (yaprak segmentasyonu) ve PlantVillage (hastalık tespiti) veri setleri kullanılarak, SBD (Symmetric Best Dice) ve DiC (Difference in Count) metrikleriyle algoritma başarısı test edilecek.

## 3. Faz: Gömülü Sisteme Geçiş ve İletişim (API) (Şu Anki Aşama)
* **Araçlar:** FastAPI (Python) veya C++ (Crow/cpp-httplib), Web Teknolojileri (HTML/JS veya Gradio)
* **Hedef:** Uygulamayı gömülü karta (Örn: Raspberry Pi, Jetson) yüklemek.
* **Detaylar:** 
  * Cihaz açıldığında sistem arka planda otomatik olarak başlayacak (Systemd daemon).
  * Cihaz yerel ağa bağlanıp bir IP alacak.
  * Bu IP'ye web tarayıcısından giren kullanıcılar arayüze (Kamera anlık görüntüsü, işlem sonuçları) ulaşabilecek.

## 4. Faz: Donanım Entegrasyonu (Sensörler ve Çevre Birimleri)
* **Araçlar:** GPIO Kütüphaneleri, C++
* **Hedef:** Görüntü işleme sonucuna göre fiziksel dünyaya tepki vermek.
* **Detaylar:** Algoritma sonucuna bağlı olarak (örn. "Yaprak tespit edildi") cihazın pinleri (GPIO) üzerinden röle açmak, motor tetiklemek veya sensör durumu okumak.

## 5. Faz: Ürünleştirme ve Dağıtım
* **Araçlar:** Docker, Yocto veya Buildroot
* **Hedef:** Yazılımı "Jenerik" ve "Kuruluma Hazır" hale getirmek.
* **Detaylar:** C++ derleyicileri, OpenCV kütüphaneleri ve Python gereksinimleri bir Docker imajına dönüştürülecek. İmaj tek satır kodla herhangi bir cihaza indirilip çalıştırılabilecek.

## 🤖 6. Faz: Embodied AI ve Otonom Tarım Robotu Vizyonu (Nihai Hayal)
* **Araçlar:** ROS 2 (Robot İşletim Sistemi), YOLOv8-Seg / U-Net / Mask R-CNN, Jetson Nano / RPi 5
* **Hedef:** Tek bir merkezi yapay zeka modeli ile arazide keşif ve otonom görevler (ilaçlama, hasat, hastalık tespiti) yapabilen hareketli bir robot yaratmak.
* **Detaylar:** 
  * **Derin Öğrenme (Gözler):** C++ motorunun içine OpenCV DNN entegre edilerek U-Net veya YOLOv8-Seg gibi modern segmentasyon modelleriyle ürün, yabani ot ve hastalıklı bölgelerin yapay zeka tarafından piksellerine kadar ayırt edilmesi.
  * **ROS 2 (Merkezi Sinir Sistemi):** C++ görüntü işleme modülünün bir ROS 2 "Kamera Düğümü"ne dönüştürülmesi ve bulguların doğrudan tekerleklere/aktüatörlere iletilmesi.
  * **Fiziksel Aksiyon:** Yapay zekanın kararına göre robotun otonom olarak (Navigasyon/SLAM) hedefe gidip mikrodenetleyici (Arduino) ile fiziksel görev (ilaçlama vb.) yapması.

## 🏢 7. Faz: Merkezi Yönetimli Robot Sürüsü (Fleet Management)
* **Araçlar:** MQTT Protokolü, Bulut Sunucu, Web Dashboard.
* **Hedef:** Tarladaki birden fazla otonom LeafVision robotunun merkezi bir yapay zeka ağından koordine edilmesi.
* **Detaylar:** Robotların merkeze sürekli telemetry (Batarya, Konum, Hastalık) göndermesi ve uzaktan filo yönetimi (Swarm Robotics).