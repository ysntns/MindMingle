# MindMingleApp - APK ve iOS Çıktısı Nasıl Alınır?

Hazırladığımız bu projeden somut bir mobil uygulama dosyası (.apk) elde etmek için **Expo Application Services (EAS)** kullanacağız. Bu işlem kodları buluta gönderir, orada derler ve size indirilebilir bir link verir.

Aşağıdaki adımları sırasıyla uygulayın:

## Hazırlık

1.  **Expo Hesabı Açın:**
    [https://expo.dev/signup](https://expo.dev/signup) adresinden ücretsiz bir hesap oluşturun ve giriş yapın.

2.  **EAS CLI Yükleyin:**
    Terminalde şu komutu çalıştırarak gerekli aracı yükleyin:
    ```bash
    npm install -g eas-cli
    ```

3.  **Giriş Yapın:**
    Terminalde şu komutu yazın ve Expo hesap bilgilerinizle giriş yapın:
    ```bash
    eas login
    ```

## 1. Android İçin APK Oluşturma (En Kolay Yöntem)

Eğer uygulamanızı hemen telefonunuza atıp denemek istiyorsanız (Play Store'a yüklemeden), "Preview" (Önizleme) modunu kullanacağız.

1.  Terminalde proje klasörüne gidin:
    ```bash
    cd MindMingleApp/mobile
    ```

2.  Projeyi Expo projesi olarak başlatın (Eğer sorarsa):
    ```bash
    npx expo install expo-updates
    eas build:configure
    ```
    *(Size "Which platforms?" diye sorarsa "All" veya "Android" seçin.)*

3.  **BÜYÜK AN:** APK oluşturma komutunu verin:
    ```bash
    eas build -p android --profile preview
    ```

4.  **Bekleyin ve İndirin:**
    Komut çalıştıktan sonra kodlarınız Expo sunucularına yüklenecek ve sıraya alınacaktır. İşlem bittiğinde terminalde size bir **QR Kod** ve bir **Link** verilecek.
    *   Linke tıklayarak `.apk` dosyasını bilgisayarınıza indirin.
    *   Dosyayı telefonunuza atıp yükleyin.
    *   **Tebrikler! MindMingleApp telefonunuzda.** 🎉

## 2. iOS İçin Çıktı Alma

Apple cihazlara uygulama yüklemek Android kadar kolay değildir (Apple'ın güvenlik politikaları nedeniyle).

*   **Simülatör İçin:**
    ```bash
    eas build -p ios --profile preview
    ```
    Bu komut size Simülatörde çalıştırabileceğiniz bir dosya verir.

*   **Gerçek Cihaz İçin:**
    Gerçek bir iPhone'a yüklemek için Apple Developer Hesabı'na (yıllık $99) ihtiyacınız vardır. Hesabınız varsa `eas build -p ios --profile production` diyerek ilerleyebilirsiniz.

## Önemli Not: Backend Bağlantısı

Unutmayın, mobil uygulama sadece bir "kabuktur". Verileri ve önerileri alabilmesi için **Backend Sunucusunun (Python)** çalışıyor olması gerekir.

1.  Uygulamayı telefonunuzda açtığınızda, bilgisayarınızdaki Python sunucusuna erişebilmesi için `mobile/App.js` dosyasındaki IP adresinin doğru olduğundan emin olun.
2.  Bilgisayarınız ve telefonunuz aynı Wi-Fi ağında olmalıdır.

İyi çalışmalar!
