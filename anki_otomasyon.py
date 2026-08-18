import csv
import time
import random
import sys
import argparse
from datetime import datetime, timedelta
from google import genai
from config import config  # Konfigürasyondan oku

# --- KONFİGÜRASYONDAN DEĞERLERİ AL ---
API_KEY = config.API_KEY
MODEL_ADI = config.MODEL_NAME
RPM_LIMIT = config.RPM_LIMIT
RPD_LIMIT = config.RPD_LIMIT

# --- DOSYA AYARLARI ---
GIRDI_DOSYASI = config.GIRDI_DOSYASI
CIKTI_DOSYASI = config.CIKTI_DOSYASI
USAGE_LOG = config.USAGE_LOG

# --- KONFİGÜRASYON ---
MAX_DENEME = config.MAX_DENEME
BASE_BEKLEME = config.BASE_BEKLEME
PROAKTIF_MOLA_ARALIGI = config.PROAKTIF_MOLA_ARALIGI
PROAKTIF_MOLA_SURESI = config.PROAKTIF_MOLA_SURESI
UZUN_MOLA_ARALIGI = config.UZUN_MOLA_ARALIGI
UZUN_MOLA_SURESI = config.UZUN_MOLA_SURESI
MIN_GECIKME = config.MIN_GECIKME
MAX_GECIKME = config.MAX_GECIKME
TOPLAM_KELIME_LIMITI = config.TOPLAM_KELIME_LIMITI

# --- LİMİTLER (Konfigürasyondan) ---
RPM_LIMIT = config.RPM_LIMIT
RPD_LIMIT = config.RPD_LIMIT

# --- API KONTROLÜ ---
if not API_KEY or API_KEY == "BURAYA_API_ANAHTARINIZI_YAPISTIRIN":
    print("\n" + "=" * 60)
    print("⚠️  UYARI: API Anahtarı ayarlanmamış!")
    print("=" * 60)
    print("Lütfen .env dosyasındaki GEMINI_API_KEY değerini güncelleyin.")
    print("Veya config.py dosyasında API_KEY değişkenini düzenleyin.")
    print("=" * 60 + "\n")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)


def log_mesaji(mesaj, tip="BILGI"):
    """Zaman damgalı log mesajı"""
    zaman = datetime.now().strftime("%H:%M:%S")
    print(f"[{zaman}] [{tip}] {mesaj}")


def track_usage(basarili=True):
    """Başarılı her isteği usage.log dosyasına kaydeder"""
    with open(USAGE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()},{basarili}\n")


def show_quota():
    """
    API kullanım istatistiklerini gösterir.
    """
    try:
        with open(USAGE_LOG, "r", encoding="utf-8") as f:
            satirlar = f.readlines()
    except FileNotFoundError:
        satirlar = []

    now = datetime.now()
    bugun_baslangic = datetime(now.year, now.month, now.day, 0, 0, 0)
    bir_dakika_once = now - timedelta(minutes=1)

    bugun_sayac = 0
    son_dakika_sayac = 0

    for satir in satirlar:
        if not satir.strip():
            continue
        try:
            ts_str, _ = satir.strip().split(",")
            ts = datetime.fromisoformat(ts_str)
            if ts >= bugun_baslangic:
                bugun_sayac += 1
            if ts >= bir_dakika_once:
                son_dakika_sayac += 1
        except ValueError:
            continue

    kalan_dakika = max(0, RPM_LIMIT - son_dakika_sayac)
    kalan_gun = max(0, RPD_LIMIT - bugun_sayac)

    print("\n" + "=" * 50)
    print("📊  GEMINI API KULLANIM DURUMU")
    print("=" * 50)
    print(f"🕒 Şu an: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    print(f"📈 Dakika limiti    : {RPM_LIMIT} istek / dakika")
    print(f"   Son 1 dakikada   : {son_dakika_sayac} istek")
    print(f"   Kalan hak        : {kalan_dakika} istek")
    print("-" * 50)
    print(f"📆 Günlük limit     : {RPD_LIMIT} istek / gün")
    print(f"   Bugün yapılan    : {bugun_sayac} istek")
    print(f"   Kalan hak        : {kalan_gun} istek")
    print("=" * 50)

    if kalan_gun < 50:
        print("⚠️  UYARI: Günlük kotanız azaldı, dikkatli kullanın!")
    if kalan_dakika < 5:
        print("⚠️  UYARI: Dakikalık kotanız dolmak üzere, biraz bekleyin!")
    
    # Konfigürasyon bilgisi
    print("-" * 50)
    print(f"📌 Model: {MODEL_ADI}")
    print(f"📂 Log dosyası: {USAGE_LOG}")
    print("=" * 50 + "\n")


def baglamli_sozluk(kelime, cumle):
    """
    Gemini API ile kelimenin bağlamsal anlamını çıkarır.
    chat.send_message kullanır (AFC uyarısı yok).
    """
    prompt = f"""Kelime: {kelime} | Cümle: {cumle}
    Görevin: Bu İngilizce kelimenin, verilen cümledeki bağlamına uygun olan kesin anlamını ve Cambridge sözlük tarzı açıklayıcı tanımını bul.
    Çıktıyı SADECE şu formatta ver: Anlam: [Bağlama uygun Türkçe karşılık] | Tanım: [Bu anlamın Türkçe açıklaması]"""

    for deneme in range(MAX_DENEME):
        try:
            chat = client.chats.create(model=MODEL_ADI)
            response = chat.send_message(prompt)

            if response.text and len(response.text.strip()) > 0:
                track_usage(basarili=True)
                return response.text.strip(), True
            else:
                log_mesaji(f"Boş yanıt alındı, yeniden deneniyor... (Deneme {deneme+1}/{MAX_DENEME})", "UYARI")
                time.sleep(10 * (deneme + 1))
                continue

        except Exception as e:
            hata_mesaji = str(e).lower()

            if "429" in hata_mesaji or "quota" in hata_mesaji or "exhausted" in hata_mesaji:
                bekleme_suresi = BASE_BEKLEME * (2 ** deneme)
                log_mesaji(
                    f"⏳ Hız sınırına takıldı! {bekleme_suresi} sn bekleniyor... (Deneme {deneme+1}/{MAX_DENEME})",
                    "BEKLEME"
                )
                time.sleep(bekleme_suresi)

            elif "500" in hata_mesaji or "502" in hata_mesaji or "503" in hata_mesaji or "504" in hata_mesaji:
                bekleme_suresi = 30 * (deneme + 1)
                log_mesaji(
                    f"⚠️ Sunucu hatası! {bekleme_suresi} sn bekleniyor... (Deneme {deneme+1}/{MAX_DENEME})",
                    "SUNUCU HATASI"
                )
                time.sleep(bekleme_suresi)

            else:
                log_mesaji(f"Hata: {e}", "HATA")
                if deneme == MAX_DENEME - 1:
                    track_usage(basarili=False)
                    return f"Hata: {e}", False
                time.sleep(5 * (deneme + 1))

    return "KOTA_DOLDU", False


def dosyayi_hazirla():
    """Çıktı dosyasında önceden kaç satır olduğunu bulur"""
    try:
        with open(CIKTI_DOSYASI, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')
            mevcut_satirlar = list(reader)
            if mevcut_satirlar and len(mevcut_satirlar) > 0:
                return len(mevcut_satirlar) - 1
    except FileNotFoundError:
        pass
    return 0


def otomasyonu_baslat():
    """Ana otomasyon fonksiyonu"""
    log_mesaji("🚀 Otomasyon başlatılıyor...", "BASLANGIC")
    
    # Başlangıçta konfigürasyonu göster
    config.show_config()

    try:
        with open(GIRDI_DOSYASI, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            satirlar = list(reader)
    except FileNotFoundError:
        log_mesaji(f"HATA: '{GIRDI_DOSYASI}' dosyası bulunamadı!", "HATA")
        return
    except Exception as e:
        log_mesaji(f"Dosya okuma hatası: {e}", "HATA")
        return

    satirlar = [satir for satir in satirlar if satir and len(satir) > 0]
    toplam_kelime = len(satirlar)

    if toplam_kelime == 0:
        log_mesaji("Hiç kelime bulunamadı!", "UYARI")
        return

    if toplam_kelime > TOPLAM_KELIME_LIMITI:
        log_mesaji(f"⚠️ Çok fazla kelime ({toplam_kelime}). İlk {TOPLAM_KELIME_LIMITI} kelime işlenecek.", "UYARI")
        satirlar = satirlar[:TOPLAM_KELIME_LIMITI]
        toplam_kelime = TOPLAM_KELIME_LIMITI

    once_islenen = dosyayi_hazirla()
    if once_islenen > 0:
        log_mesaji(f"📊 Önceden {once_islenen} kelime işlenmiş, devam ediliyor...", "BILGI")

    islenmis_satirlar = []
    islenen_kelime_sayaci = 0
    basarisiz_kelimeler = []

    log_mesaji(f"📝 Toplam {toplam_kelime} kelime işlenecek.\n", "BILGI")

    for index, satir in enumerate(satirlar):
        if not satir or len(satir) < 3:
            log_mesaji(f"⚠️ {index+1}. satır eksik veri içeriyor, atlanıyor.", "UYARI")
            islenmis_satirlar.append(satir if satir else ["", "", ""])
            continue

        kelime = satir[0].strip()
        cumle = satir[2].strip() if len(satir) > 2 else ""

        if not kelime:
            log_mesaji(f"⚠️ {index+1}. satırda kelime yok, atlanıyor.", "UYARI")
            islenmis_satirlar.append(satir)
            continue

        if not cumle:
            log_mesaji(f"⚠️ {kelime} için cümle yok, atlanıyor.", "UYARI")
            islenmis_satirlar.append([kelime, "CÜMLE YOK", ""])
            continue

        # --- PROAKTİF MOLA: Kısa ---
        if islenen_kelime_sayaci > 0 and islenen_kelime_sayaci % PROAKTIF_MOLA_ARALIGI == 0:
            log_mesaji(f"🛡️ {PROAKTIF_MOLA_ARALIGI} kelime işlendi. {PROAKTIF_MOLA_SURESI} sn proaktif dinlenme...", "MOLA")
            time.sleep(PROAKTIF_MOLA_SURESI)
            log_mesaji("✅ Dinlenme bitti, devam ediliyor.\n", "MOLA BITTI")

        # --- PROAKTİF MOLA: Uzun ---
        if islenen_kelime_sayaci > 0 and islenen_kelime_sayaci % UZUN_MOLA_ARALIGI == 0:
            log_mesaji(f"☕ {UZUN_MOLA_ARALIGI} kelime işlendi. {UZUN_MOLA_SURESI} sn uzun mola...", "UZUN MOLA")
            time.sleep(UZUN_MOLA_SURESI)
            log_mesaji("✅ Uzun mola bitti, devam ediliyor.\n", "MOLA BITTI")

        log_mesaji(f"[{index+1}/{toplam_kelime}] 🔄 İşleniyor: {kelime}", "ISLEM")

        cevap, basarili_mi = baglamli_sozluk(kelime, cumle)

        if cevap == "KOTA_DOLDU":
            log_mesaji("🚨 API kotası tamamen doldu! Otomasyon durduruluyor...", "KRITIK")
            break

        if basarili_mi:
            yeni_satir = [kelime, cevap, cumle]
            islenmis_satirlar.append(yeni_satir)
            islenen_kelime_sayaci += 1
            log_mesaji(f"✅ {kelime} başarıyla işlendi", "BASARILI")
        else:
            yeni_satir = [kelime, f"HATA: {cevap}", cumle]
            islenmis_satirlar.append(yeni_satir)
            basarisiz_kelimeler.append(kelime)
            log_mesaji(f"❌ {kelime} işlenemedi: {cevap}", "HATA")

        # --- İNSANSI GECİKME ---
        bekleme_suresi = random.uniform(MIN_GECIKME, MAX_GECIKME)
        if random.random() < 0.05:
            ekstra = random.uniform(3, 8)
            log_mesaji(f"⏳ İnsansı gecikme: +{ekstra:.1f} sn", "GECIKME")
            time.sleep(ekstra)
        time.sleep(bekleme_suresi)

        if islenen_kelime_sayaci % 10 == 0 and islenen_kelime_sayaci > 0:
            log_mesaji(
                f"📊 İlerleme: {islenen_kelime_sayaci}/{toplam_kelime} (%{(islenen_kelime_sayaci/toplam_kelime*100):.1f})",
                "RAPOR"
            )

    # --- DOSYAYA KAYDET ---
    if islenmis_satirlar:
        try:
            mevcut_veriler = []
            try:
                with open(CIKTI_DOSYASI, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.reader(f, delimiter=';')
                    mevcut_veriler = list(reader)
            except FileNotFoundError:
                pass

            if mevcut_veriler and len(mevcut_veriler) > 0:
                tum_veriler = mevcut_veriler + islenmis_satirlar
            else:
                tum_veriler = islenmis_satirlar

            with open(CIKTI_DOSYASI, mode='w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(tum_veriler)

            log_mesaji(f"💾 {len(islenmis_satirlar)} kelime '{CIKTI_DOSYASI}' dosyasına kaydedildi.", "KAYIT")

            if basarisiz_kelimeler:
                log_mesaji(f"⚠️ {len(basarisiz_kelimeler)} kelime işlenemedi: {', '.join(basarisiz_kelimeler[:5])}", "UYARI")
                if len(basarisiz_kelimeler) > 5:
                    log_mesaji(f"   ... ve {len(basarisiz_kelimeler)-5} kelime daha", "UYARI")

        except Exception as e:
            log_mesaji(f"Dosya kaydetme hatası: {e}", "HATA")
    else:
        log_mesaji("Hiçbir kelime işlenemedi, dosya oluşturulmadı.", "UYARI")

    # --- ÖZET RAPOR ---
    log_mesaji("\n" + "="*60, "RAPOR")
    log_mesaji(f"✅ Başarıyla işlenen: {islenen_kelime_sayaci} kelime", "RAPOR")
    log_mesaji(f"❌ İşlenemeyen: {len(basarisiz_kelimeler)} kelime", "RAPOR")
    log_mesaji(f"📂 Çıktı dosyası: {CIKTI_DOSYASI}", "RAPOR")
    log_mesaji("="*60 + "\n", "RAPOR")


def main():
    """Argüman yönetimi ve ana giriş noktası"""
    parser = argparse.ArgumentParser(
        description="📚 Anki için İngilizce kelime anlamlarını Gemini API ile otomatik çıkaran araç.",
        epilog="Örnek kullanım:\n  python anki_otomasyon.py          # Normal çalıştırma\n  python anki_otomasyon.py --quota  # Kullanım istatistiklerini göster"
    )
    parser.add_argument(
        "--quota", "-q",
        action="store_true",
        help="API kullanım istatistiklerini (son 1 dakika ve bugün) gösterir ve çıkar."
    )
    parser.add_argument(
        "--config", "-c",
        action="store_true",
        help="Mevcut konfigürasyon ayarlarını gösterir."
    )
    args = parser.parse_args()

    if args.config:
        config.show_config()
        sys.exit(0)

    if args.quota:
        show_quota()
        sys.exit(0)

    try:
        otomasyonu_baslat()
    except KeyboardInterrupt:
        log_mesaji("\n⏹️ Kullanıcı tarafından durduruldu!", "DURDURULDU")
        sys.exit(0)
    except Exception as e:
        log_mesaji(f"Beklenmeyen hata: {e}", "KRITIK HATA")
        sys.exit(1)


if __name__ == "__main__":
    main()