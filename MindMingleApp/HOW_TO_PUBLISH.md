# MindMingle Play Store Yayınlama ve Kurulum Rehberi

Bu rehber, MindMingle uygulamasını canlı verilerle çalıştırmak ve Google Play Store'a yüklemek için gerekli adımları içerir.

## 1. API Anahtarlarını Alma (Canlı Veriler İçin)

Uygulamanın film, müzik ve kitap verilerini güncel çekebilmesi için aşağıdaki servislerden API anahtarı almanız gerekir.

### A. TMDB (Filmler)
1. [The Movie Database (TMDB)](https://www.themoviedb.org/) sitesine üye olun.
2. Profil -> Ayarlar -> API bölümüne gidin.
3. Bir API anahtarı oluşturun.
4. Bu anahtarı `backend/.env` dosyasında `TMDB_API_KEY` karşısına yazın.

### B. Spotify (Müzik)
1. [Spotify for Developers](https://developer.spotify.com/dashboard) adresine gidin.
2. "Create App" diyerek yeni bir uygulama oluşturun.
3. `Client ID` ve `Client Secret` değerlerini alın.
4. Bu değerleri `backend/.env` dosyasında ilgili yerlere yazın.

### C. Google Books (Kitaplar)
1. [Google Cloud Console](https://console.cloud.google.com/) adresine gidin.
2. Yeni proje oluşturun ve "Books API" servisini etkinleştirin.
3. "Credentials" kısmından bir API Key oluşturun.
4. `backend/.env` dosyasına ekleyin.

**Not:** API anahtarları girilmezse uygulama otomatik olarak eski CSV verilerini kullanmaya devam eder.

## 2. Backend Kurulumu

Sunucuyu çalıştırmak için:

```bash
cd MindMingleApp/backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0
```

## 3. Mobil Uygulama Build (Play Store İçin)

Google Play Store'a yüklemek için `.aab` (Android App Bundle) formatında çıktı almanız gerekir. Bunun için `EAS Build` kullanacağız.

### Hazırlık
1. [Expo.dev](https://expo.dev) üzerinde hesap oluşturun.
2. EAS CLI yükleyin: `npm install -g eas-cli`
3. Giriş yapın: `eas login`

### Build Alma
Terminali `MindMingleApp/mobile` klasöründe açın:

```bash
# Gerekli bağımlılıkları yükleyin
npm install

# Build işlemini başlatın
eas build --platform android --profile production
```

Bu işlem sırasında Expo size bir Keystore oluşturmak isteyip istemediğinizi soracaktır. "Yes" diyerek Expo'nun sizin için yönetmesini sağlayabilirsiniz.

İşlem bittiğinde size bir indirme linki (.aab dosyası) verecektir.

## 4. Play Store'a Yükleme

1. İndirdiğiniz `.aab` dosyasını [Google Play Console](https://play.google.com/console) hesabınızda "Production" veya "Testing" kanalına yükleyin.
2. Mağaza görsellerini ve açıklamalarını girin.
3. İncelemeye gönderin.

Harika fikriniz artık yayında! 🚀
