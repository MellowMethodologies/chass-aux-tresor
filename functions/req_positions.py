
import difflib
import requests

def get_positions(language, coordinates, direction_string, limit, indice):
    # Extract x and y from the coordinates string
    try:
        x, y = eval(coordinates)  # Convert string '[0,0]' to tuple (0, 0)
    except (SyntaxError, TypeError):
        return "Erreur: Les coordonnées doivent être au format '[x,y]'"

    # Mapping des directions
    direction_map = {
        "right": 6,
        "down": 2,
        "left": 4,
        "up": 0
    }
    direction = direction_map.get(direction_string.lower(), 6)
    # Configuration de la requête API
    url = f'https://api.dofusdb.fr/treasure-hunt?x={x}&y={y}&direction={direction}&limit={limit}'
    headers = {"token": "03AFcWeA6nAY6QzOYxiOr-3049o_SVvKoIzpVd7Na0VnXvAajaSS-jfnWIWUYtcKs1-9lAGP9z328WbRjM4DfLSsnQEQCjRrSP7dcfnyZl_PzRcfZ4_0Dwu84SnhHpFFZOWMKxqhbx6ROBJHL0_VkX4qPP4Ujkqklm6c3o4m1Ed96RLXaqNKUpx8nh01aVRVHbZk_s-CjopvqxmugSqbjaoNtlCUhYIfncYvI5KPgrIjgHdORzJDfqLAPYnrlp9q3pXIe-eirxxxeeBc2Ap7lNt9156hL8GH-WttZkldle3qgQMKnQugfoMEGMDTbRShyreYLTpvRsoSUAHVY9epnShLN5p9VmurelK7vZl_MrF9fafgjHxQQBhjZGQYwAUzzKXHSV_9BROfDNtqkhURD8wN27NuYGanPUq45WtNsLj90FJYR97w2nnGk_snXsjdWrM0tG-B170A1h_9emltKSC1QeRYZxzg1PJSLWjBBze1iVDY8uz9CIEI_Rb2fW-aeo-TFUlu1InVbo7XGdB2fGA-F5l4Ev28_k0FW4CB8GFGlf7ir2ixFU77pR0lLMNg_ZQz7OP7nGXUUA5NW2TO95g2S9GjSghjOKyJyE4WUfyDBM7_rujW3MvkhvU5JhrxdT65sQCpn6Bm-oQI540JnqsyzsRBDiGdTXxbct36aqf_wYXOznQPMIF7trFIQey7NGpNcPYhDL43XzEyxNs023en9FHjxlHEbNG9IPW3iwjIcUpSFqyaUHnXmwhsTulUF2nVNJifUL4byf12HHl3kuhGh2buD4KoKGkzB9QZBLtaVJzdPIlzny-CZUb53dZ5GT4Ri6hmyEOHj9FHlNUFZcmk0nRl4FWi73-JwhtsPxqpXe3K2iidkomCfSY7W2CU8zKzBE8Oc8PMJdzPpX4d7pgekrltj0InICz8tAW_hJevgWv6eTY-f6xfBqXQgjZNuZFcb4hhbDz0jaL5EJVyE1J9La4k96Z6BOR7K_au7sliEV2VuPcEP-ROEszu6sQZIfsFhti0XwdmYb8FdxytwFu02XfIcksr-lYYev1waJ0AhHYw0q_Oy3sWPaYzNHEtKX8LjS0CZP-YDxduA1aJNfhfV3qMtL-DCO8yLfa6NZfZr5N8_90i_ZytIcKRO53EE6nay7nljiTgQTpJWa57H0o6nKltnz-cXhE5E9httTk1mQZ256Ff4Csy_ar8Rekr51Oihw1-Gi_R8ycQhe3nWiguAtEdDD0md_EC8I9-fFY6OmvrAb_rU2qNvodE2jsdae43vnf_9sVfAts6XWcmZAgAL_si41k8cykJ4TMBTtOASCWjmL1oQNcnacv9MdeFZ76i22jznADVUPfSxAzZTecm48ECYTsZNg0QoO-eL96LnfuTXNZULM6uZa1BjeVp_121tZiKp0Y3yX6eNp9wD-1BikJWjXiKaq0uW5B7dZsvDcD1ft3Fe_qA0SpyWUrgynufFIVgmvLZ317U9bUqT243num8jbTJ4ZJbvoM_5ngQ_uPlNBwppXQ7dpoIcI2zwYXBjH6-8YfeK3c4Owas3ffz_zGLbG5ulcxvQK1K456e2K-4IuJoiEwS1ZhLxHyOxGH1aMAGgwXrGTHDdbHPFYeUN2u0ezLqU0mJokdxeLWdZAUMnSPPzqouM0tAMESPD1eTS_LLo_v88hTfdl73UKXvVoUx8h9YRX4tJ5u8WNCjUH4LGeSApps7Ld981tBmjCI1cOiAtWdLHh9eY50Pef6xHAQQWx_lyLUuqHu32YhwsoRLEggTyz7D5O1ntZr9I_bPqP5BrFvtsuXlZ13f5qi-MWvNvRxICf_3AlrWFYdT5_avuWKmMjLY2sbLnv9iUEe_gcCnwF28tI3_1Yuoyno77YYULx8kZ4XUVyRJ3uFrkqpgogY12orB9ensxfbvC1aqDO5hOSR5Guaw-z5Rmo5wWTL4XbfTcnpWduN6ae8vjbItAGKKNKpOXaadJM6g2Lca1ePhZLlOV7aOqewyWnOZ50GXpmvJvE8GcHe88QUwRnt8YqDIEUtwGb766rxv9c-Q08k167LSbJ"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get('data', [])
    except Exception as e:
        return "dr"

    # Collecte de tous les POIs avec leurs positions
    pois = []
    for location in data:
        for poi in location.get('pois', []):
            poi_name = poi.get('name', {}).get(language, '')
            if poi_name:
                pois.append({
                    'name': poi_name,
                    'x': location.get('posX'),
                    'y': location.get('posY'),
                    'score': 0
                })

    if not pois:
        return "dr"

    # Recherche exacte
    exact_match = next((p for p in pois if p['name'].lower() == indice.lower()), None)
    if exact_match:
        return f"{exact_match['x']},{exact_match['y']}"

    # Calcul de similarité
    for p in pois:
        seq = difflib.SequenceMatcher(None, p['name'].lower(), indice.lower())
        p['score'] = seq.ratio()

    # Tri par meilleur score
    best_match = max(pois, key=lambda x: x['score'])
    # Seuil de similarité (ajuster selon besoin)
    if best_match['score'] > 0.6:
        return f'{best_match["x"]},{best_match["y"]}'
    else:
        indice_lower = indice.lower()
        
        if "drheller" in indice_lower:
            return "dr"
        
        drheller_similarity = difflib.SequenceMatcher(None, "drheller", indice_lower).ratio()
        
        if drheller_similarity > 0.7:  # You can adjust this threshold
            return "dr"
    
        return None

