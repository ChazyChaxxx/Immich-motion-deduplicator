import csv
import requests
import time

# -----------------------------
# CONFIGURATION
# -----------------------------
API_URL = "http://192.168.129.100:8212/api"
API_KEY = os.getenv("IMMICH_API_KEY")  # Remplacez par votre clé API réelle

INPUT_CSV = "motion_candidates_with_ids.csv"
BATCH_SIZE = 25       # Taille de la vague
DRY_RUN = True      # True = simulation, False = suppression réelle
SLEEP_BETWEEN_BATCHES = 3.5  # secondes

# -----------------------------
# HEADERS
# -----------------------------
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# -----------------------------
# FONCTIONS
# -----------------------------
def chunk_list(lst, size):
    """Divise une liste en sous-listes de taille 'size'"""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def delete_batch(ids):
    """Supprime un batch d'assets via API DELETE /assets"""
    payload = {
        "ids": ids,
        "force": False
    }

    response = requests.delete(
        f"{API_URL}/assets",
        json=payload,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    # Essaie de parser JSON, sinon retourne un dict simple
    try:
        return response.json()
    except ValueError:
        return {"status_code": response.status_code, "message": "No content returned"}

# -----------------------------
# LECTURE DU CSV
# -----------------------------
asset_ids = []

with open(INPUT_CSV, newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if row.get("asset_id"):
            asset_ids.append(row["asset_id"])

print(f"{len(asset_ids)} assets à supprimer.")

# -----------------------------
# EXECUTION DES BATCHES
# -----------------------------
if DRY_RUN:
    print("DRY RUN activé — aucune suppression effectuée.")
else:
    for batch_num, batch in enumerate(chunk_list(asset_ids, BATCH_SIZE), start=1):
        print(f"Suppression batch {batch_num} ({len(batch)} assets)...")
        try:
            result = delete_batch(batch)
            print(f"Batch {batch_num} OK. Réponse API : {result}")
        except requests.RequestException as e:
            print(f"[ERREUR] Batch {batch_num} a échoué :", e)

        time.sleep(SLEEP_BETWEEN_BATCHES)

print("Traitement terminé.")