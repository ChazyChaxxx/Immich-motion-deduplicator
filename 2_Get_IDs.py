import csv
import os
import requests

API_URL = "http://192.168.129.100:8212/api"
API_KEY = API_KEY = os.getenv("IMMICH_API_KEY")  # Remplacez par votre clé API réelle

INPUT_CSV = "motion_candidates_2025.csv"
OUTPUT_CSV = "motion_candidates_with_ids_2025.csv"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def get_asset_id(filename):
    payload = {
        "filter": {
            "originalFileName": {
                "like": filename
            },
            "type": {
                "eq": "VIDEO"
            }
        }
    }

    try:
        response = requests.post(
            f"{API_URL}/search/metadata",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        items = data.get("assets", {}).get("items", []) or data.get("items", [])

        if not items:
            print(f"[NOT FOUND] Aucun asset trouvé pour : {filename}")
            return None

        # Filtrage : On cherche l'asset de la 'library' (pas le 'encoded-video' masqué)
        library_items = [
            item for item in items 
            if "/upload/library/" in item.get("originalPath", "") or item.get("visibility") == "timeline"
        ]

        if len(library_items) == 1:
            asset_id = library_items[0]["id"]
            print(f"[FOUND] {filename} -> ID Library: {asset_id}")
            return asset_id
        elif len(library_items) == 0:
            print(f"[NOT FOUND IN LIBRARY] Trouvé uniquement dans encoded-video pour : {filename}")
            return None
        else:
            print(f"[MULTIPLE LIBRARY MATCHES] {len(library_items)} assets library trouvés pour : {filename}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR API] Erreur lors de la requête pour {filename}: {e}")
        return None


def main():
    if not os.path.exists(INPUT_CSV):
        print(f"[ERROR] Le fichier d'entrée '{INPUT_CSV}' introuvable.")
        return

    print(f"Début du traitement du fichier : {INPUT_CSV}")
    processed_count = 0
    found_count = 0

    with open(INPUT_CSV, newline="", encoding="utf-8") as infile, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["asset_id"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            processed_count += 1
            mp4_path = row["mp4_path"]

            # Extraction du nom de fichier exact sans modification de casse
            filename = os.path.basename(mp4_path)

            print(f"\n[{processed_count}] Recherche pour : {filename}")
            asset_id = get_asset_id(filename)

            if asset_id:
                found_count += 1

            row["asset_id"] = asset_id
            writer.writerow(row)

    print("\n----------------------------------------")
    print(f"Traitement terminé avec succès !")
    print(f"Total traités : {processed_count}")
    print(f"Asset IDs récupérés : {found_count}/{processed_count}")
    print(f"Résultat sauvegardé dans : {OUTPUT_CSV}")

if __name__ == "__main__":
    main()