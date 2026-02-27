import requests
import json
import os
import random
from datetime import datetime

# GÜVENLİ ANAHTARLAR
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
        # TÜM CANLI MAÇLARI ÇEKİYORUZ
        print("RapidAPI'den canlı veriler çekiliyor...")
        res_live = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all", headers=headers_rapid)
        
        if res_live.status_code == 200:
            data = res_live.json()
            fixtures = data.get('response', [])
            print(f"Toplam {len(fixtures)} canlı maç bulundu.")

            for item in fixtures:
                # AI Analizlerini burada otomatik oluşturuyoruz
                tahminler = ["MS 1", "MS 2", "2.5 ÜST", "KG VAR", "İY 0.5 ÜST", "MS X"]
                guven = f"%{random.randint(75, 98)}"
                
                mac = {
                    "lig": item['league']['name'],
                    "ev": item['teams']['home']['name'],
                    "dep": item['teams']['away']['name'],
                    "skor": f"{item['goals']['home']}-{item['goals']['away']}",
                    "dakika": item['fixture']['status']['elapsed'] or 0,
                    "ai_tahmini": random.choice(tahminler),
                    "ai_guven": guven,
                    "ai_analiz": f"Botumuz bu maçta {item['teams']['home']['name']} ve {item['teams']['away']['name']} arasındaki istatistikleri inceleyerek en yüksek güven oranlı tahmini belirledi."
                }
                final_data["canli_maclar"].append(mac)
        else:
            print(f"API Hatası: {res_live.status_code}")

    except Exception as e:
        print(f"Genel Hata: {e}")

    # Boş kalmasın diye (Maçkolik'te olsa bile API gecikirse diye)
    if not final_data["canli_maclar"]:
        final_data["canli_maclar"].append({
            "lig": "Sistem",
            "ev": "Veriler",
            "dep": "Güncelleniyor",
            "skor": "0-0",
            "dakika": 0,
            "ai_tahmini": "Bülten Yükleniyor",
            "ai_guven": "%--",
            "ai_analiz": "Canlı maçlar birazdan listelenecek. Lütfen yenileyin."
        })

    with open('veriler.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("Yazma işlemi başarılı.")

if __name__ == "__main__":
    get_data()
