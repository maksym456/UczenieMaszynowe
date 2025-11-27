import pandas as pd
import requests
import time

df = pd.read_csv("listaFirmInProgress.csv", sep=";", encoding="utf-8")

headers = {
    "Authorization": "Bearer eyJraWQiOiJjZWlkZyIsImFsZyI6IkhTNTEyIn0.eyJnaXZlbl9uYW1lIjoiTWFrc3ltIiwicGVzZWwiOiIwMzIzMTQwODk3NSIsImlhdCI6MTc2NDE2NjM2NCwiZmFtaWx5X25hbWUiOiJXaWxrIiwiY2xpZW50X2lkIjoiVVNFUi0wMzIzMTQwODk3NS1NQUtTWU0tV0lMSyJ9.7JNjjM8hVMAQ7huu43EZFOTv5Cg2I-6chI_3uymd_q5D1QUOKWF-ZKugLUz9iwLdZU-40TApPLOvLd4pVuU5nw"
}

for index, row in df.iterrows():
    nip = row["Nip"]
    url = f"https://dane.biznes.gov.pl/api/ceidg/v3/firma?nip={str(nip)[:10]}"
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        data = r.json()

        pkd = data["firma"][0]["pkdGlowny"]["nazwa"]

        # nadpisanie istniejącej kolumny
        df.at[index, "Przeważająca działalność gospodarcza"] = pkd

        # zapis po każdej aktualizacji (bezpieczne na przerwanie)
        df.to_csv("listaFirmInProgress.csv", sep=";", encoding="utf-8", index=False)

        time.sleep(0.2)  # lekkie opóźnienie, żeby API Cię nie zablokowało

    except Exception as e:
        print(f"Błąd przy NIP {nip}: {e}")
