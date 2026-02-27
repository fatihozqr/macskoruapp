import requests
import json
import os
from datetime import datetime

# API ANAHTARLARI
# Not: GitHub'a yüklerken bunları "Secrets" kısmına ekleyeceğiz, şimdilik test için buradalar.
FD_API_KEY = "40c819a253bb47848c069fb45d497619"
RAPID_API_KEY = "711626cbc2mshad5cc598f05f3f3p118239jsn0cd4ef7dd02a"

def get_data():
    final_data = {
        "son_guncelleme": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "canli_maclar": [],
        "gelecek_maclar": [],
        "puan_durumu": {}
    }

    try:
        # 1. Football-Data: Günün Maçları ve Canlı Skorlar
        fd_url = "https://api.football-data.org/v4/matches"
        fd_headers = {'X-Auth-Token': FD_API_KEY}
        fd_res = requests.get(fd_url, headers=fd_headers)
        
        if fd_res.status_code == 200:
            matches = fd_res.json().get('matches', [])
            for m in matches:
                mac_obj = {
                    "id": m['id'],
                    "lig": m['competition']['name'],
                    "ev": m['homeTeam']['shortName'],
                    "dep": m['awayTeam']['shortName'],
                    "skor": f"{m['score']['fullTime']['home']}-{m['score']['fullTime']['away']}",
                    "durum": "canli" if m['status'] == 'IN_PLAY' else "gelecek",
                    "saat": m['utcDate'][11:16],
                    "dakika": m.get('minute', '0')
                }
                if mac_obj['durum'] == "canli":
                    final_data["canli_maclar"].append(mac_obj)
                else:
                    final_data["gelecek_maclar"].append(mac_obj)

        # 2. RapidAPI: Süper Lig Puan Durumu (League ID: 203)
        rapid_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        rapid_params = {"league": "203", "season": "2025"}
        rapid_headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        rapid_res = requests.get(rapid_url, headers=rapid_headers, params=rapid_params)
        
        if rapid_res.status_code == 200:
            standings = rapid_res.json()['response'][0]['league']['standings'][0]
            final_data["puan_durumu"]["super_lig"] = [
                {"sira": t['rank'], "takim": t['team']['name'], "puan": t['points']}
                for t in standings
            ]

    except Exception as e:
        print(f"Hata oluştu: {e}")

    # Dosyaya Yaz (Büfeye ekmekleri bırakıyoruz)
    with open('veriler.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("Veriler başarıyla güncellendi!")

if __name__ == "__main__":
    get_data()
