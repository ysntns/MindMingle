# MindMingleApp - Mobil Versiyon

Bu proje, MindMingle makine öğrenmesi projesinin mobil uygulamaya (Android/iOS) dönüştürülmüş halidir. Proje iki ana parçadan oluşur:
1. **Backend (Python/FastAPI):** Makine öğrenmesi modelini ve öneri sistemini çalıştıran API.
2. **Mobile (React Native/Expo):** Kullanıcı arayüzünü sağlayan mobil uygulama.

## Kurulum ve Çalıştırma

Projeyi çalıştırmak için bilgisayarınızda **Python** ve **Node.js** yüklü olmalıdır. Ayrıca telefonunuzda **Expo Go** uygulaması yüklü olmalıdır.

### 1. Backend Kurulumu (Sunucu)

Öneri sisteminin çalışması için önce sunucuyu ayağa kaldırmalısınız.

1. Terminali açın ve backend klasörüne gidin:
   ```bash
   cd MindMingleApp/backend
   ```

2. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Sunucuyu başlatın:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Bu komut sunucuyu `http://localhost:8000` adresinde başlatacaktır.

   **Önemli:** Mobil uygulamanın sunucuya erişebilmesi için bilgisayarınızın yerel IP adresini (Local IP) öğrenmeniz gerekebilir (örn: `192.168.1.x`). Windows'ta `ipconfig`, Mac/Linux'ta `ifconfig` komutuyla öğrenebilirsiniz.

### 2. Mobil Uygulama Kurulumu

1. Yeni bir terminal penceresi açın ve mobile klasörüne gidin:
   ```bash
   cd MindMingleApp/mobile
   ```

2. Gerekli JavaScript paketlerini yükleyin:
   ```bash
   npm install
   ```

3. **API Adresini Ayarlama:**
   `App.js` dosyasını açın ve `API_URL` satırını bulun. Eğer gerçek bir Android/iOS cihazda test ediyorsanız, `localhost` yerine bilgisayarınızın IP adresini yazın.

   ```javascript
   // Örnek:
   const API_URL = 'http://192.168.1.35:8000/recommend';
   ```

4. Uygulamayı başlatın:
   ```bash
   npx expo start
   ```

5. Çıkan QR kodu telefonunuzdaki **Expo Go** uygulaması ile okutun.

## Veri Güncelleme

Uygulama verileri `MindMingleApp/backend/data/` klasöründeki `.csv` dosyalarından okur. Verileri güncellemek için bu dosyaları yenileriyle değiştirip backend sunucusunu yeniden başlatmanız yeterlidir.

## Proje Yapısı

- `backend/`: Python FastAPI kodları ve veriler.
  - `main.py`: API sunucusu.
  - `data/`: CSV ve PKL dosyaları.
- `mobile/`: React Native mobil uygulama kodları.
  - `App.js`: Ana uygulama ekranı ve mantığı.

İyi eğlenceler!
