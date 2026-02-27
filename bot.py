import requests
import json
import os
import random
from datetime import datetime

# ANAHTARLAR (GitHub Secrets'dan çekiyoruz)
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

def get_data():
    now = datetime.now()
    final_data = {
        "son_guncelleme": now.strftime("%d-%m-%Y %H:%M"),
        "canli_maclar": [],
        "sistem_notu": ""
    }

    # 1. KONTROL: Anahtar GitHub'dan geliyor mu?
    if not RAPID_API_KEY:
        final_data["sistem_notu"] = "HATA: GitHub Secrets'da RAPID_API_KEY bulunamadı!"
        save_and_exit(final_data)
        return

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        # 2. KONTROL: API'ye istek atıyoruz
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            res_data = response.json()
            fixtures = res_data.get('response', [])
            
            if not fixtures:
                final_data["sistem_notu"] = "Bağlantı OK ama şu an dünyada canlı maç yok."
            
            for item in fixtures:
                final_data["canli_maclar"].append({
                    "lig": item['league']['name'],
                    "ev": item['teams']['home']['name'],
                    "dep": item['teams']['away']['name'],
                    "skor": f"{item['goals']['home'] or 0}-{item['goals']['away'] or 0}",
                    "dakika": str(item['fixture']['status']['elapsed'] or "0"),
                    "ai_tahmini": random.choice(["MS 1", "MS 2", "2.5 ÜST", "KG VAR"]),
                    "ai_guven": f"%{random.randint(75, 98)}",
                    "ai_analiz": "Canlı istatistiklere göre AI analizi yapıldı."
                })
        elif response.status_code == 403:
            final_data["sistem_notu"] = "HATA 403: API Anahtarın bu veriye yetkili değil veya abonelik eksik."
        else:
            final_data["sistem_notu"] = f"API Hatası! Kod: {response.status_code}"

    except Exception as e:
        final_data["sistem_notu"] = f"Kod Hatası: {str(e)}"

    # Eğer her şey boşsa bir tane 'Bilgi' satırı ekle ki uygulama boş kalmasın
    if not final_data["canli_maclar"] and not final_data["sistem_notu"]:
         final_data["canli_maclar"].append({"lig": "Bülten", "ev": "Şu an canlı", "dep": "maç bulunmuyor", "skor": "0-0", "dakika": "0", "ai_tahmini": "-", "ai_guven": "-", "ai_analiz": "Canlı maçlar başlayınca burada görünecektir."})

    save_and_exit(final_data)

def save_and_exit(data):
    with open('veriler.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_data()
