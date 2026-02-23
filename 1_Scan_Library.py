import os
import csv

# ==============================
# CONFIGURATION
# ==============================

ROOT_DIR = r"W:\immich\upload\library\fa76aac0-437a-4afc-a091-d0a0c3d24f09\2022"   # <-- À modifier
OUTPUT_CSV = "motion_candidates.csv"

# ==============================
# LOGIQUE
# ==============================

candidates = []
total_mp4 = 0

for root, dirs, files in os.walk(ROOT_DIR):
    files_lower = {f.lower(): f for f in files}

    for file in files:
        if file.lower().endswith(".mp4"):
            total_mp4 += 1
            base = file[:-4]
            jpg_name = base + ".jpg"

            if jpg_name.lower() in files_lower:
                mp4_path = os.path.join(root, file)
                jpg_path = os.path.join(root, files_lower[jpg_name.lower()])

                candidates.append({
                    "mp4_path": mp4_path,
                    "jpg_path": jpg_path,
                    "mp4_size_MB": round(os.path.getsize(mp4_path) / (1024 * 1024), 2)
                })

# ==============================
# EXPORT CSV
# ==============================

if candidates:
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=candidates[0].keys())
        writer.writeheader()
        writer.writerows(candidates)

    print(f"\n✅ Analyse terminée.")
    print(f"📹 MP4 analysés : {total_mp4}")
    print(f"🎯 Candidats Motion détectés : {len(candidates)}")
    print(f"📄 Résultat exporté dans : {OUTPUT_CSV}")

else:
    print("\n⚠ Aucun candidat détecté.")
    print(f"📹 MP4 analysés : {total_mp4}")