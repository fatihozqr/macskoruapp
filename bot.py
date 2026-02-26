import json
import requests
from datetime import datetime

def analiz_et(takim1, takim2):
    # Basit AI tahmin simülasyonu
    guc1 = len(takim1)
    guc2 = len(takim2)
    
    if guc1 > guc2:
        return {"tahmin": "MS 1", "guven": "%72", "not": f"{takim1} iç sahada baskılı oynuyor."}
    elif guc1 == guc2:
        return {"tahmin": "KG VAR", "guven": "%65", "not": "İki takımın gücü birbirine çok yakın."}
    else:
        return {"tahmin": "MS 2", "guven": "%68", "not": f"{takim2} deplasmanda daha formda."}

def veri_guncelle():
    # Güncel veri kaynağı (İngiltere Premier Lig)
    url = "https://raw.githubusercontent.com/openfootball/football.json/master/2023-24/en.1.json"
    
    try:
        print("Veri çekiliyor...")
        res = requests.get(url)
        res.raise_for_status() 
        data = res.json()
        
        # 'rounds' hatasını önlemek için güvenli veri çekme yapısı
        maclar = data.get('matches', [])
        
        # Eğer veri yapısı farklıysa (eski format) alternatif kontrol
        if not maclar and 'rounds' in data:
            maclar = []
            for round_data in data['rounds']:
                maclar.extend(round_data.get('matches', []))
        
        final_lig = []
        # İlk 15 maçı alıp analiz edelim
        for m in maclar[:15]:
            takim1 = m.get('team1', 'Bilinmeyen Takım')
            takim2 = m.get('team2', 'Bilinmeyen Takım')
            tarih = m.get('date', 'Tarih Yok')
            
            ai = analiz_et(takim1, takim2)
            
            final_lig.append({
                "ev_sahibi": takim1,
                "deplasman": takim2,
                "tarih": tarih,
                "ai_tahmini": ai['tahmin'],
                "guven_skoru": ai['guven'],
                "analiz_notu": ai['not']
            })

        final_sonuc = {
            "bot_adi": "Skor AI",
            "guncelleme_zamani": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "mac_sayisi": len(final_lig),
            "veriler": final_lig
        }

        # JSON dosyasını güncelle
        with open('veriler.json', 'w', encoding='utf-8') as f:
            json.dump(final_sonuc, f, ensure_ascii=False, indent=4)
            
        print(f"Başarılı! {len(final_lig)} maç analiz edildi.")

    except Exception as e:
        print(f"Hata detayı: {e}")

if __name__ == "__main__":
    veri_guncelle()
