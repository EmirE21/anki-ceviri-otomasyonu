import os
from dotenv import load_dotenv

class Config:
    """Uygulama konfigürasyon yönetimi"""
    
    def __init__(self):
        # .env dosyasını yükle
        load_dotenv()
        self._load_config()
    
    def _load_config(self):
        """Tüm konfigürasyon değerlerini yükle"""
        
        # API Ayarları
        self.API_KEY = os.getenv("GEMINI_API_KEY", "BURAYA_API_ANAHTARINIZI_YAPISTIRIN")
        self.MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-3.6-flash")
        
        # API Limitleri (Google'ın güncel limitleri)
        self.RPM_LIMIT = int(os.getenv("GEMINI_RPM_LIMIT", 15))
        self.RPD_LIMIT = int(os.getenv("GEMINI_RPD_LIMIT", 1500))
        
        # Proje Ayarları
        self.MAX_DENEME = int(os.getenv("MAX_DENEME", 5))
        self.BASE_BEKLEME = int(os.getenv("BASE_BEKLEME", 65))
        
        # Mola Ayarları
        self.PROAKTIF_MOLA_ARALIGI = int(os.getenv("PROAKTIF_MOLA_ARALIGI", 10))
        self.PROAKTIF_MOLA_SURESI = int(os.getenv("PROAKTIF_MOLA_SURESI", 75))
        self.UZUN_MOLA_ARALIGI = int(os.getenv("UZUN_MOLA_ARALIGI", 30))
        self.UZUN_MOLA_SURESI = int(os.getenv("UZUN_MOLA_SURESI", 120))
        
        # Gecikme Ayarları
        self.MIN_GECIKME = float(os.getenv("MIN_GECIKME", 5.0))
        self.MAX_GECIKME = float(os.getenv("MAX_GECIKME", 7.5))
        
        # Güvenlik
        self.TOPLAM_KELIME_LIMITI = int(os.getenv("TOPLAM_KELIME_LIMITI", 500))
        
        # Dosya Ayarları
        self.GIRDI_DOSYASI = os.getenv("GIRDI_DOSYASI", "kelimeler.csv")
        self.CIKTI_DOSYASI = os.getenv("CIKTI_DOSYASI", "anki_icin_hazir.csv")
        self.USAGE_LOG = os.getenv("USAGE_LOG", "usage.log")
    
    def get_limits(self):
        """API limitlerini sözlük olarak döndür"""
        return {
            "rpm": self.RPM_LIMIT,
            "rpd": self.RPD_LIMIT
        }
    
    def show_config(self):
        """Mevcut konfigürasyonu göster"""
        print("\n" + "=" * 50)
        print("⚙️  SİSTEM KONFİGÜRASYONU")
        print("=" * 50)
        print(f"📌 Model:          {self.MODEL_NAME}")
        print(f"📈 RPM Limit:      {self.RPM_LIMIT} istek/dakika")
        print(f"📆 RPD Limit:      {self.RPD_LIMIT} istek/gün")
        print("-" * 50)
        print(f"⏱️ Max Deneme:     {self.MAX_DENEME}")
        print(f"🔄 Proaktif Mola:  {self.PROAKTIF_MOLA_ARALIGI} kelime → {self.PROAKTIF_MOLA_SURESI} sn")
        print(f"☕ Uzun Mola:      {self.UZUN_MOLA_ARALIGI} kelime → {self.UZUN_MOLA_SURESI} sn")
        print(f"⏳ Gecikme:        {self.MIN_GECIKME}-{self.MAX_GECIKME} sn")
        print(f"📂 Giriş:          {self.GIRDI_DOSYASI}")
        print(f"📂 Çıkış:          {self.CIKTI_DOSYASI}")
        print(f"📂 Log:            {self.USAGE_LOG}")
        print("=" * 50)

# Global config nesnesi
config = Config()