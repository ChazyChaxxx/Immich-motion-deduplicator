import csv
import os
import requests

API_URL = "http://192.168.129.100:8212/api"
API_KEY = os.getenv("IMMICH_API_KEY")  # Remplacez par votre clé API réelle

INPUT_CSV = "Jumeaux.csv"
OUTPUT_CSV = "motion_candidates_with_ids.csv"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def get_asset_id(filename):
    payload = {
        "originalFileName": filename,
        "type": "VIDEO"
    }

    response = requests.post(
        f"{API_URL}/search/metadata",
        json=payload,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    items = data.get("assets", {}).get("items", [])

    if len(items) == 1:
        return items[0]["id"]
    elif len(items) == 0:
        print(f"[NOT FOUND] {filename}")
        return None
    else:
        print(f"[MULTIPLE MATCHES] {filename}")
        return None


with open(INPUT_CSV, newline="", encoding="utf-8") as infile, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["asset_id"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        mp4_path = row["mp4_path"]

        # Extraire le nom de fichier
        filename = os.path.basename(mp4_path)

        # Convertir extension en MAJUSCULE
        filename = filename.upper()

        asset_id = get_asset_id(filename)

        row["asset_id"] = asset_id
        writer.writerow(row)

print("Terminé.")