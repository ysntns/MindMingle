# MindMingleApp - APK ve iOS Çıktısı Nasıl Alınır?

Hazırladığımız bu projeden somut bir mobil uygulama dosyası (.apk) elde etmek için iki yönteminiz var:
1.  **Bulut Yöntemi (EAS):** En kolayıdır, kurulum gerektirmez.
2.  **Yerel Yöntem (Android Studio):** Bilgisayarınızda Android Studio yüklüyse en hızlısıdır.

---

## ⚠️ ÖNEMLİ: Yeni Özellik Kurulumu

Projeye **Yüz Tanıma (AI)** özelliği eklendiği için backend kütüphanelerini güncellemeniz GEREKMEKTEDİR.

Backend klasöründe şu komutu çalıştırın:
```bash
pip install -r requirements.txt
```
*(Bu işlem biraz uzun sürebilir çünkü yüz tanıma modellerini indirir.)*

---

## Yöntem 1: Bulut ile APK Oluşturma (Önerilen)

Eğer Android Studio kurmakla uğraşmak istemiyorsanız bu yöntemi kullanın.

1.  [https://expo.dev/signup](https://expo.dev/signup) adresinden ücretsiz hesap açın.
2.  Terminalden projeye gidin:
    ```bash
    cd MindMingleApp/mobile
    ```
3.  EAS aracını yükleyip giriş yapın:
    ```bash
    npm install -g eas-cli
    eas login
    ```

4.  **PROJEYİ BAŞLATMA:**
    ```bash
    eas init
    ```
    *(Size "Would you like to automatically create an EAS Project?" diye sorarsa "Yes" deyin.)*

5.  **APK OLUŞTURMA:**
    ```bash
    eas build -p android --profile preview
    ```

6.  İşlem bitince terminalde çıkan **linke tıklayıp** APK dosyasını indirin.

---

## Yöntem 2: Android Studio ile APK Oluşturma (Yerel)

Projenizin içinde hazır bir **Android Kaynak Kodu** (`android` klasörü) oluşturduk.

1.  **Hazırlık (Önemli):**
    Önce terminalden proje klasörüne gidip gerekli paketleri yükleyin:
    ```bash
    cd MindMingleApp/mobile
    npm install
    ```
    *(Eğer `android` klasöründe sorun yaşarsanız `npx expo prebuild --platform android --clean` komutuyla klasörü yeniden oluşturabilirsiniz.)*

2.  **Android Studio**'yu açın.
3.  "Open" diyerek `MindMingleApp/mobile/android` klasörünü seçin.
4.  Projenin senkronize olmasını bekleyin (Gradle Sync).
5.  Üst menüden **Build > Build Bundle(s) / APK(s) > Build APK(s)** yolunu izleyin.
6.  Derleme bittiğinde sağ altta çıkan bildirime tıklayarak APK dosyasının olduğu klasörü açın (`debug` klasörü içinde olacaktır).
7.  Bu dosyayı (`app-debug.apk`) telefonunuza atıp kurabilirsiniz.

---

## Sorun Giderme (Troubleshooting)

Eğer yerel derleme (Local Build) sırasında hata alırsanız:

*   **Java Sürümü:** Bu proje Java 11 veya Java 17 ile en iyi çalışır. Java 21 veya daha yeni sürümler Gradle ile uyumsuzluk yaratabilir.
    *   Hata Örneği: `Could not get unknown property 'release'` veya `Plugin [...] not found`.
    *   Çözüm: Java sürümünüzü kontrol edin (`java -version`) ve gerekirse Java 17 yükleyin.
*   **Gradle Hatası:** Eğer `SDK location not found` hatası alırsanız, `MindMingleApp/mobile/android/local.properties` dosyasına `sdk.dir=/path/to/android/sdk` satırını eklediğinizden emin olun (Android Studio bunu otomatik yapar).

## Önemli Not: Backend Bağlantısı

Uygulamanın çalışması için **Python Sunucusu** açık olmalıdır.

1.  Backend klasörüne gidin:
    ```bash
    cd MindMingleApp/backend
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
2.  Mobil uygulamanın bu sunucuya erişebilmesi için `mobile/App.js` içindeki IP adresini kendi bilgisayarınızın IP adresiyle değiştirdiğinizden emin olun (Örn: `192.168.1.35`).

İyi çalışmalar!
