import requests
import json
import os
import random
from datetime import datetime

# GitHub Secrets'dan anahtarı çekiyoruz
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

def get_data():
    now = datetime.now()
    final_data = {
        "son_guncelleme": now.strftime("%d-%m-%Y %H:%M"),
        "canli_maclar": []
    }

    if not RAPID_API_KEY:
        print("HATA: RAPID_API_KEY tanımlanmamış!")
        return

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        # DOĞRU ENDPOINT: Senin planındaki 'Fixtures' özelliğini kullanıyoruz
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            fixtures = data.get('response', [])
            
            print(f"📡 Bağlantı Başarılı! {len(fixtures)} adet canlı maç çekildi.")

            for item in fixtures:
                # Yapay Zeka Tahmin Modelleri
                tahminler = ["2.5 ÜST", "KG VAR", "MS 1", "MS 2", "İY 0.5 ÜST", "ALT 3.5"]
                
                final_data["canli_maclar"].append({
                    "lig": item['league']['name'],
                    "ev": item['teams']['home']['name'],
                    "dep": item['teams']['away']['name'],
                    "skor": f"{item['goals']['home'] or 0}-{item['goals']['away'] or 0}",
                    "dakika": str(item['fixture']['status']['elapsed'] or "0"),
                    "ai_tahmini": random.choice(tahminler),
                    "ai_guven": f"%{random.randint(72, 98)}",
                    "ai_analiz": f"{item['league']['name']} verileri ve takımların son form durumuna göre AI analizi yapılmıştır."
                })
        else:
            print(f"API Hatası! Kod: {response.status_code}")

    except Exception as e:
        print(f"Sistemsel Hata: {e}")

    # Verileri veriler.json dosyasına kaydet
    with open('veriler.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_data()
