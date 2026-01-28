# MindMingleApp - APK ve iOS Çıktısı Nasıl Alınır?

Hazırladığımız bu projeden somut bir mobil uygulama dosyası (.apk) elde etmek için iki yönteminiz var:
1.  **Bulut Yöntemi (EAS):** En kolayıdır, kurulum gerektirmez.
2.  **Yerel Yöntem (Android Studio):** Bilgisayarınızda Android Studio yüklüyse en hızlısıdır.

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

4.  **PROJEYİ BAŞLATMA (Çok Önemli Adım):**
    Aşağıdaki komutu yazın ve sorulara cevap verin:
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

1.  **Android Studio**'yu açın.
2.  "Open" diyerek `MindMingleApp/mobile/android` klasörünü seçin.
3.  Projenin senkronize olmasını bekleyin (Gradle Sync).
4.  Üst menüden **Build > Build Bundle(s) / APK(s) > Build APK(s)** yolunu izleyin.
5.  Derleme bittiğinde sağ altta çıkan bildirime tıklayarak APK dosyasının olduğu klasörü açın (`debug` klasörü içinde olacaktır).
6.  Bu dosyayı (`app-debug.apk`) telefonunuza atıp kurabilirsiniz.

---

## Önemli Not: Backend Bağlantısı

Uygulamanın çalışması için **Python Sunucusu** açık olmalıdır.

1.  Backend klasörüne gidin:
    ```bash
    cd MindMingleApp/backend
    pip install -r requirements.txt
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
2.  Mobil uygulamanın bu sunucuya erişebilmesi için `mobile/App.js` içindeki IP adresini kendi bilgisayarınızın IP adresiyle değiştirdiğinizden emin olun (Örn: `192.168.1.35`).

İyi çalışmalar!
