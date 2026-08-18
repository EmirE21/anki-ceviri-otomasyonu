# Anki İçin Çeviri Otomasyonu

İngilizce kelimeleri, verilen cümle bağlamına göre analiz ederek Anki flashcard uygulamasına doğrudan import edilebilecek CSV dosyasına dönüştüren bir araçtır.

## Başlangıç

### Gereksinimler

- Python 3.8 veya üzeri

- Google Gemini API anahtarı (ücretsiz)

### Kurulum Adımları

1. Projeyi indirin veya kopyalayın.

2. Terminalde proje klasörüne gidin.

3. Bağımlılıkları yükleyin.

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

6. Çalıştırın.

   ```bash
   python anki_otomasyon.py
   ```

## Kullanım

Araç, girdi olarak bir CSV dosyası alır ve işlediği her kelime için B sütununa Cambridge sözlük tarzında Türkçe anlam ve açıklama ekler.

### Çıktı Dosyası

`anki_icin_hazir.csv` adıyla oluşur. Anki'de `;` (noktalı virgül) ayracı ile import edilebilir.

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

Bu nedenle en sağlıklı kullanım şekli, işlemi tek bir seansta değil güne yayarak yapmaktır. Örneğin sabah ve akşam olmak üzere iki ayrı seansta kelimeleri işleyebilirsiniz. Bu yöntemle hem limitlere takılmadan ilerleyebilir hem de sistemin sizi yavaşlatmasını engelleyebilirsiniz.

Araç, her 10 kelimede bir 75 saniye, her 30 kelimede bir ise 120 saniye mola verir. Bu, Google tarafından hızlı istek atan bot olarak algılanmamanız için alınmış bir önlemdir. Bu molalar sistemin işleyişinin bir parçasıdır.

Kota takibi için `--quota` argümanını düzenli olarak kullanmanız, gün içinde kaç istek hakkınız kaldığını görmenizi sağlar. Günlük limit dolduğunda, sistem otomatik olarak işlemi durdurur.

## Dikkat Edilmesi Gereken Durumlar

- CSV dosyasında sütun ayracı olarak ;; (çift noktalı virgül) kullanılmalıdır.

- API anahtarınızı .env dosyasında saklayın ve bu dosyayı asla paylaşmayın.

- Günde 500 kelimenin üzerinde işlem yapmak istiyorsanız, işlemi birden fazla seansa bölün.

- İşlem sırasında terminali kapatmayın. Kapatırsanız, dosyaya kaydedilen kelimeler kadar kaldığı yerden devam edebilirsiniz.

- Google'ın API limitleri değişirse, .env dosyasındaki GEMINI_RPM_LIMIT ve GEMINI_RPD_LIMIT değerlerini güncelleyerek sistemi uyarlayabilirsiniz.

- Bu araç, kelime çalışmalarınızı daha verimli hale getirmek için geliştirilmiştir. Amacı, manuel çeviri sürecini otomatize ederek zaman kazandırmak ve bağlama uygun anlam çıkarımı konusunda size yardımcı olmaktır.
