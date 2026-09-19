# Otonom Filo Yönetimi (Fleet Management) Uygulama Planı

Bu plan, LeafVision çekirdeğini tekil bir uygulamadan, arazide görev yapan çoklu robotları yöneten merkezi bir hub sistemine dönüştürmeyi amaçlar.

## Mimari Vizyon: Merkezi Yönetimli Otonom Sürü

### 1. Katman: Fleet Hub (Merkezi Yönetim) - [FastAPI]
- **Görev:** Robotların konumlarını, batarya durumlarını ve analiz sonuçlarını takip etmek.
- **WebSocket Desteği:** Robotlarla anlık (real-time) çift yönlü haberleşme.
- **Haritalama:** Robotların arazideki izdüşümlerinin görselleştirilmesi.

### 2. Katman: Robot Standart Modülü (Edge AI) - [Python/C++]
- **Leaf Analyzer:** Mevcut C++ motoru her robotun içinde yerel olarak çalışır.
- **Task Processor:** Merkezden gelen "Git", "Analiz Et", "Püskürt" komutlarını işler.
- **Hardware Abstraction:** Motor sürücüleri (Arduino/Serial) ile konuşan katman.

## Önerilen Değişiklikler

### Modüler Yapılandırma (Clean Architecture)
#### [NEW] `core/analyzer.py`
- C++ motorunu sarmalayan ve hata yönetimini yapan ana iş mantığı katmanı.

#### [NEW] `communication/protocol.py`
- Robot-Merkez arası JSON tabanlı mesajlaşma standartları (MQTT/Websocket simülasyonu).

#### [MODIFY] [server.py](file:///c:/Users/Halil/Downloads/Compressed/GoruntuIsleme/server.py) (Fleet Hub Upgrade)
- `/robot/register` ve `/robot/status` endpointleri ile çoklu robot yönetimi.

#### [NEW] `simulator/robot_client.py`
- Fiziksel robot olmadan sistemi test etmek için sanal bir robot istemcisi.

## Doğrulama Planı
### Senaryo Testi
1. [server.py](file:///c:/Users/Halil/Downloads/Compressed/GoruntuIsleme/server.py) (Merkez) başlatılır.
2. 3 adet `robot_client.py` (Sanal Robotlar) farklı kimliklerle merkeze bağlanır.
3. Merkezden "Robot-1, Resim Analiz Et" komutu gönderilir.
4. Robot-1'in yerel C++ motoruyla resmi işleyip sonucu merkeze yansıttığı doğrulanır.

## Kullanıcı Onayı Gerekenler
- **ROS 2 Entegrasyonu:** Şu aşamada tam ROS 2 kurulumu Windows üzerinde ağır gelebilir, bunun yerine Python tabanlı hafif bir ROS-Like (MQTT/Websocket) protokolü üzerinden ilerlenmesi önerilir.
