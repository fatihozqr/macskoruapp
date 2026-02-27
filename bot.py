import requests
import json
import os
from datetime import datetime

# GÜVENLİ ANAHTARLAR (GitHub Secrets'tan çekilir)
FD_API_KEY = os.getenv('FD_API_KEY')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

# DÜNYANIN EN GELİŞMİŞ VE POPÜLER LİGLERİ (RapidAPI ID'leri)
# Bu liste uygulamanın zenginliğini belirler.
GELISMIS_LIGLER = {
    "Süper Lig": "203",
    "Premier League": "39",
    "La Liga": "140",
    "Serie A": "135",
    "Bundesliga": "78",
    "Ligue 1": "61",
    "Eredivisie": "88",        # Hollanda
    "Primeira Liga": "94",     # Portekiz
    "Serie A (Brezilya)": "71", # Brezilya
    "Pro League (S. Arabistan)": "307", # Ronaldo/Neymar etkisi için
    "Champions League": "2",
    "1. Lig (Türkiye)": "204"   # Yerel kullanıcılar için
}

def get_data():
    final_data = {
        "son_guncelleme": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "canli_maclar": [],
        "gelecek_maclar": [],
        "puan_durumlari": {}
    }

    headers_fd = {'X-Auth-Token': FD_API_KEY}
    headers_rapid = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        # 1. Football-Data: Tüm Dünya Genelindeki Günlük Maç Akışı
        fd_url = "https://api.football-data.org/v4/matches"
        fd_res = requests.get(fd_url, headers=headers_fd)
        if fd_res.status_code == 200:
            for m in fd_res.json().get('matches', []):
                mac = {
                    "lig": m['competition']['name'],
                    "ev": m['homeTeam']['shortName'],
                    "dep": m['awayTeam']['shortName'],
                    "skor": f"{m['score']['fullTime']['home']}-{m['score']['fullTime']['away']}",
                    "durum": "canli" if m['status'] in ['IN_PLAY', 'PAUSED'] else "gelecek",
                    "saat": m['utcDate'][11:16]
                }
                if mac["durum"] == "canli":
                    final_data["canli_maclar"].append(mac)
                else:
                    final_data["gelecek_maclar"].append(mac)

        # 2. RapidAPI: Gelişmiş Liglerin Puan Durumlarını Çekme
        # Not: Ücretsiz plandaki 100 istek limitini korumak için 
        # her çalıştırmada sadece seçili ligleri çekiyoruz.
        for lig_adi, lig_id in GELISMIS_LIGLER.items():
            # Mevcut yıl/sezon ayarı
            params = {"league": lig_id, "season": "2025"}
            res = requests.get("https://api-football-v1.p.rapidapi.com/v3/standings", 
                               headers=headers_rapid, params=params)
            
            if res.status_code == 200:
                data = res.json()
                if data['response'] and len(data['response']) > 0:
                    standings = data['response'][0]['league']['standings'][0]
                    final_data["puan_durumlari"][lig_adi] = [
                        {"sira": t['rank'], "takim": t['team']['name'], "puan": t['points'], "form": t.get('form', '-')} 
                        for t in standings
                    ]

    except Exception as e:
        print(f"Hata oluştu: {e}")

    # Veriyi JSON olarak kaydet
    with open('veriler.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("En gelişmiş veriler başarıyla kaydedildi!")

if __name__ == "__main__":
    get_data()
