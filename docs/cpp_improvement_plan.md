# LeafVision C++ Çekirdeği İyileştirme Planı

Bu belge, temel OpenCV sınır bulma (Edge Detection) algoritmalarından, literatürdeki gelişmiş Tarım/Bitki (AgriTech) algoritmalarına geçiş sürecini aşamalandırır.

## Literatür ve GitHub Araştırma Özeti (Yeni)
Yaptığım araştırmalarda AgriTech alanında öne çıkan teknikler:
1. **Renk Alanı Seçimi**: Sadece LAB değil, **HSI (Hue-Saturation-Intensity)** ve **Cluttered Background** durumlarında **Excess Green Index (ExG)**: `2G - R - B` formülü çok popüler.
2. **Dinamik Eşikleme**: Sadece Otsu değil, değişken ışık altındaki tarlalar için **Adaptive Mean/Gaussian Thresholding**.
3. **Örtüşen Nesneler**: Literatürde "Overlapping Leaf Segmentation" için altın kural: **Distance Transform + Watershed**.
4. **Kenar Keskinleştirme**: Canny öncesi **Anisotropic Diffusion** veya **Bilateral Filter** kullanarak dokuyu koruyup gürültüyü silmek.

## Aşama 1: Işık ve Gölge Direnci (LAB Renk Uzayı & Otsu) - [TAMAMLANDI]
*   **Problem:** Mevcut RGB (justGreen) formülü, gölgeli alanları siyah veya toprak rengi olarak algılayıp yanlış kesimler yapabiliyor.
*   **Düzeltme:** BGR -> LAB dönüşümü yapıldı ve 'A' kanalı üzerinden yeşil izolasyonu sağlandı. Dinamik Otsu eklendi.

## Aşama 2: Üst Üste Binen Yaprakları Ayırma (Watershed & Distance Transform) - [TAMAMLANDI]
*   **Çözüm:** 
    1.  `cv::distanceTransform` ile yaprakların merkezlerini bulup "tohum" (seed) noktaları belirlemek.
    2.  `cv::watershed` ile bu tohumlardan başlayarak sınırları yaprakların birleşim noktalarına kadar genişletmek.
*   **Hedef:** Birbirine değen yaprakları jilet gibi ayırmak.
*   **Not:** `src/core/leaf_boundary.cpp` içindeki pipeline'da 4-7. adımlar (distance map,
    foreground seeds, watershed markers, final edges) olarak zaten uygulandı.

## Aşama 3: Doku ve Hastalık Analizi (GLCM / Gabor Filters)
*   **Gelişmiş:** Yaprak üzerindeki hastalık lekelerini sadece renk değil, **Doku (Texture)** analizi ile (Gabor filtreleri) ayırmak.
*   **Eylem:** Yaprak maskesi içindeki "pürüzlülük" oranını hesaplayıp kullanıcıya "Yaprak Sağlık Skoru" döndürmek.

## Aşama 4: Performans ve Entegrasyon
*   C++ motorunu **Multi-threading (OpenMP)** ile hızlandırarak 4K resimlerde bile <100ms seviyesine çekmek.
