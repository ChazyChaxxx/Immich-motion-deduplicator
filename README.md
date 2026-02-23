# Immich Motion deduplicator

If you exported your media using Google Takeout and your phone uses Motion Photos / Live Photos, you probably duplicated your media.

Google Takeout exports:
- A JPG file (the photo with the functionnal motion)
- A separate MP4 file (the motion video only)

When importing into Immich, both can appear as standalone assets.

This script helps you safely remove the duplicated motion video files.

---

## What This Project Does

1. Scans your library and search for photo and video with the same basename and creates a .csv
2. Queries Immich API (`/search/metadata`) and add the ID for each assets (matches assets by filename)
3. Deletes matched video assets in safe batches (supports dry-run mode)

---

## Requirements

- Python 3.10+
