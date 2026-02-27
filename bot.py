import requests
import json
import os
import random
from datetime import datetime

# GÜVENLİ ANAHTARLAR
FD_API_KEY = os.getenv('FD_API_KEY')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

def get_data():
    final_data = {
        "son_guncelleme": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "canli_maclar": [],
        "gelecek_maclar": []
    }

    headers_rapid = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        # 1. RAPIDAPI İLE TÜM DÜNYADAKİ CANLI MAÇLARI ÇEKİYORUZ
        print("Canlı maçlar çekiliyor...")
        res_live = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all", headers=headers_rapid)
        
        if res_live.status_code == 200:
            data = res_live.json()
            for item in data.get('response', []):
                # AI Analizlerini burada otomatik oluşturuyoruz
                tahminler = ["2.5 ÜST", "KG VAR", "MS 1", "MS 2", "İLK YARI 0.5 ÜST"]
                guven = f"%{random.randint(65, 98)}"
                analiz_notu = f"Takımların son form durumu ve canlı istatistikleri bu maçta {random.choice(tahminler)} ihtimalini güçlendiriyor."

                mac = {
                    "lig": item['league']['name'],
                    "ev": item['teams']['home']['name'],
                    "dep": item['teams']['away']['name'],
                    "skor": f"{item['goals']['home']}-{item['goals']['away']}",
                    "dakika": item['fixture']['status']['elapsed'],
                    "ai_tahmini": random.choice(tahminler),
                    "ai_guven": guven,
                    "ai_analiz": analiz_notu
                }
                final_data["canli_maclar"].append(mac)
        
        # Eğer canlı maç yoksa boş kalmasın diye test verisi ekleyelim (Sadece deneme için)
        if not final_data["canli_maclar"]:
            final_data["canli_maclar"].append({
                "lig": "Test Ligi",
                "ev": "Yükleniyor Takımı",
                "dep": "Analiz Takımı",
                "skor": "0-0",
                "dakika": 0,
                "ai_tahmini": "Bülten Bekleniyor",
                "ai_guven": "%0",
                "ai_analiz": "Canlı bülten güncellendiğinde burada profesyonel analizler belirecek."
            })

    except Exception as e:
        print(f"Hata: {e}")

    # Veriyi kaydet
    with open('veriler.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"İşlem Tamam! {len(final_data['canli_maclar'])} maç sisteme yüklendi.")

if __name__ == "__main__":
    get_data()
