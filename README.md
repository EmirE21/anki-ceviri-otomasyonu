![Proje banner görseli](images/anki_ceviri_otomasyonu_banner.png)

<div align="center">
   <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python">
   <img src="https://img.shields.io/badge/Gemini-API-orange.svg" alt="Gemini API">
   <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</div>

# Kullanım Rehberi

CSV dosya formatında verilen İngilizce kelimeleri, dosyada yer alan cümlelerdeki bağlamlarına göre Gemini API yardımı ile Türkçe diline çevirip sözlük anlamını verilen CSV dosyasına işleyen bir araçtır.

## Başlangıç

### Gereksinimler

- Python 3.8 veya üzeri (ücretsiz)

- Google Gemini API anahtarı (ücretsiz)

### Kurulum Adımları

1. Projeyi indirin veya klonlayın.

2. Terminal üzerinden proje klasörüne gidin.

3. Gereklilikleri yükleyin.

   ```bash
   pip install -r requirements.txt
   ```

4. `.env` dosyasını oluşturun ve Google Gemini API anahtarınızı ekleyin.

   ```text
   GEMINI_API_KEY=sizin_api_anahtariniz
   ```

5. `kelimeler.csv` dosyasını aşağıdaki formatta hazırlayın.

   ```text
   kelime;;kelimenin geçtiği ingilizce cümle
   ```

   **Not:** CSV dosyasına bu formatta yazmak zor olabilir. Excel üzerinden; A sütununda İngilizce keimeler, C sütununda kelimenin geçtiği İngilizce cümle yer alacak şekilde doldurup dosyayı CSV (UTF-8) formatında farklı kaydederseniz aynı sonuca ulaşabilirsiniz.

6. Çalıştırın.

   ```bash
   python anki_otomasyon.py
   ```

## Kullanım

Araç, girdi olarak bir CSV dosyası alır ve işlediği her kelime için Excel programında B sütununa denk gelen bölgeye Cambridge Dictionary sitesinde yer alan kelime tanımı tarzında Türkçe anlam ve açıklama ekler.

### .env Dosyası Oluşturma Adımları

1. Proje klasörüne gidin.

2. Klasör içinde boş bir alana sağ tıklayın.

3. "Yeni" → "Metin Belgesi" seçeneğine tıklayın.

4. Oluşan dosyayı .env olarak yeniden adlandırın.
   1. Eğer dosya uzantısı görünmüyorsa: Dosya Gezgini → "Görünüm" → "Dosya adı uzantıları" seçeneğini işaretleyin.

   2. Önemli: Dosya adı env.txt değil, .env olmalıdır.

5. Dosyaya çift tıklayarak Notepad ile açın.

6. Aşağıdaki içeriği kopyalayıp yapıştırın.

7. Ctrl + S ile kaydedin.

```env
# Google Gemini API Ayarları
GEMINI_API_KEY=BURAYA_API_ANAHTARINIZI_YAPISTIRIN

# API Limitleri (Google'ın güncel limitlerine göre düzenleyin)
GEMINI_RPM_LIMIT=15
GEMINI_RPD_LIMIT=1500

# Model Ayarları
GEMINI_MODEL_NAME=gemini-3.6-flash

# Proje Ayarları
MAX_DENEME=5
BASE_BEKLEME=65
PROAKTIF_MOLA_ARALIGI=10
PROAKTIF_MOLA_SURESI=75
UZUN_MOLA_ARALIGI=30
UZUN_MOLA_SURESI=120
MIN_GECIKME=5.0
MAX_GECIKME=7.5
TOPLAM_KELIME_LIMITI=500
```

#### Değiştirilebilecek Ayarlar

| Kategori     | Değişken                | Açıklama                                         | Varsayılan       | Değiştirilebilir mi? |
| ------------ | ----------------------- | ------------------------------------------------ | ---------------- | -------------------- |
| **API**      | `GEMINI_API_KEY`        | Google Gemini API anahtarınız                    | **(Boş)**        | ✅ **Zorunlu**       |
| **Limit**    | `GEMINI_RPM_LIMIT`      | Dakikada maksimum API isteği                     | 15               | ✅ Evet              |
| **Limit**    | `GEMINI_RPD_LIMIT`      | Günde maksimum API isteği                        | 1500             | ✅ Evet              |
| **Model**    | `GEMINI_MODEL_NAME`     | Kullanılacak Gemini modeli                       | gemini-3.6-flash | ✅ Evet              |
| **Deneme**   | `MAX_DENEME`            | API hatasında maksimum deneme sayısı             | 5                | ✅ Evet              |
| **Bekleme**  | `BASE_BEKLEME`          | Hata durumunda başlangıç bekleme süresi (saniye) | 65               | ✅ Evet              |
| **Mola**     | `PROAKTIF_MOLA_ARALIGI` | Kaç kelimede bir kısa mola verileceği            | 10               | ✅ Evet              |
| **Mola**     | `PROAKTIF_MOLA_SURESI`  | Kısa mola süresi (saniye)                        | 75               | ✅ Evet              |
| **Mola**     | `UZUN_MOLA_ARALIGI`     | Kaç kelimede bir uzun mola verileceği            | 30               | ✅ Evet              |
| **Mola**     | `UZUN_MOLA_SURESI`      | Uzun mola süresi (saniye)                        | 120              | ✅ Evet              |
| **Gecikme**  | `MIN_GECIKME`           | İnsansı gecikme minimum süre (saniye)            | 5.0              | ✅ Evet              |
| **Gecikme**  | `MAX_GECIKME`           | İnsansı gecikme maksimum süre (saniye)           | 7.5              | ✅ Evet              |
| **Güvenlik** | `TOPLAM_KELIME_LIMITI`  | Tek seferde işlenecek maksimum kelime            | 500              | ✅ Evet              |

#### Önemli Uyarılar

##### 1. .env Dosyasını Paylaşmayın

- .env dosyası API anahtarınızı içerir. Bu dosyayı kimseyle paylaşmayın.

- .env dosyasını e-posta, mesaj veya herhangi bir platformda paylaşmayın.

- Eğer yanlışlıkla paylaştıysanız, Google AI Studio'dan API anahtarınızı iptal edip yeni bir tane oluşturun.

##### 2. .env Dosyasını GitHub'a Yüklemeyin

- .env dosyasını asla GitHub'a yüklemeyin.

- Projede zaten .gitignore dosyası bulunmaktadır ve .env bu dosyaya eklenmiştir.

- Eğer yanlışlıkla yüklediyseniz, GitHub reponuzdan hemen silin ve yeni bir API anahtarı oluşturun.

**Not:** .env dosyası, projeyi çalıştırmak için zorunludur. API anahtarınızı doğru bir şekilde yapılandırmadan proje çalışmayacaktır.

### Çıktı Dosyası

`anki_icin_hazir.csv` adıyla oluşur. Anki'de `;` (noktalı virgül) ayracı ile yüklenebilir.

### Kota Sorgulama

```bash
python anki_otomasyon.py --quota
```

### Konfigürasyon Kontrolü

```bash
python anki_otomasyon.py --config
```

## İdeal Kullanım Senaryosu

Sistem, Google'ın ücretsiz API kullanım limitleri çerçevesinde tasarlanmıştır: Dakikada 15 istek, günde 1500 istek.

Bu nedenle en sağlıklı kullanım şekli, işlemi tek seferde değil güne yayarak yapmaktır. Örneğin sabah ve akşam olmak üzere iki ayrı seansta kelimeleri işleyebilirsiniz. Bu yöntemle hem limitlere takılmadan ilerleyebilir hem de sistemin sizi yavaşlatmasını engelleyebilirsiniz.

### Detaylı Performans Tablosu

| Zaman Dilimi  | İstek Başarı Oranı | Bekleme Riski | İdeal Kullanım |
| ------------- | :----------------: | ------------- | -------------- |
| 06:00 - 09:00 |        %99         | Çok Düşük     | ✅ En İdeal    |
| 09:00 - 12:00 |        %97         | Düşük         | ⚠️ Uygun       |
| 12:00 - 14:00 |        %85         | Yüksek        | ❌ Önerilmez   |
| 14:00 - 17:00 |        %70         | Çok Yüksek    | ❌ Sakıncalı   |
| 17:00 - 20:00 |        %88         | Yüksek        | ❌ Önerilmez   |
| 20:00 - 23:00 |        %94         | Orta          | ⚠️ Uygun       |
| 23:00 - 06:00 |        %99         | Çok Düşük     | ✅ En İdeal    |

Araç, her 10 kelimede bir 75 saniye, her 30 kelimede bir ise 120 saniye mola verir. Bu, Google tarafından hızlı istek atan bot olarak algılanmamanız için alınmış bir önlemdir. Bu molalar sistemin işleyişinin bir parçasıdır.

### Önerilen İşlem Kapasitesi

| Zaman Dilimi  | Tahmini İşlem | Risk Seviyesi | Kullanım Önerisi  |
| ------------- | ------------- | ------------- | ----------------- |
| 06:00 - 09:00 | 200 - 250     | Düşük         | ✅ Yüksek Verim   |
| 09:00 - 12:00 | 150 - 200     | Orta          | ✅ Normal         |
| 12:00 - 14:00 | 80 - 120      | Yüksek        | ❌ Kaçının        |
| 14:00 - 17:00 | 50 - 80       | Çok Yüksek    | ❌ Sakıncalı      |
| 17:00 - 20:00 | 80 - 120      | Yüksek        | ❌ Kaçının        |
| 20:00 - 23:00 | 120 - 180     | Orta          | ⚠️ Dikkatli       |
| 23:00 - 06:00 | 200 - 300     | Düşük         | ✅ Maksimum Verim |

Kota takibi için `--quota` argümanını düzenli olarak kullanmanız, gün içinde kaç istek hakkınız kaldığını görmenizi sağlar. Günlük limit dolduğunda, sistem otomatik olarak işlemi durdurur.

## Dikkat Edilmesi Gereken Durumlar

- API anahtarınızı .env dosyasında saklayın ve bu dosyayı asla paylaşmayın.

- Günde yüksek miktardaki kelimenin üzerinde işlem yapmak istiyorsanız, kelime listesini birden fazla parçaya bölerek işlemi gerçekleştirin.

- İşlem sırasında terminali kapatmayın, ancak kapatırsanız, dosyaya kaydedilen kelimeler kadar kaldığı yerden devam edebilirsiniz.

- Google'ın API limitleri değişirse, .env dosyasındaki GEMINI_RPM_LIMIT ve GEMINI_RPD_LIMIT değerlerini güncelleyerek sistemi uyarlayabilirsiniz.

Bu araç, kelime çalışmalarınızı daha verimli hale getirmek için geliştirilmiştir. Amacı, manuel çeviri sürecini otomatize ederek zaman kazandırmak ve bağlama uygun anlam çıkarımı konusunda size yardımcı olmaktır. Bol ve zevkli öğrenimler hepinize!
