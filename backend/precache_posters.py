import os
import sys
import urllib.request
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.db.session import SessionLocal
from app.db.models import MovieTitle

cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster_cache")
os.makedirs(cache_dir, exist_ok=True)

db = SessionLocal()
movies = db.query(MovieTitle).all()

print(f"Pre-caching real posters for {len(movies)} movies into {cache_dir}...")
success = 0
for m in movies:
    file_path = os.path.join(cache_dir, f"{m.id}.jpg")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:
        success += 1
        continue
    
    if not m.poster_url:
        print(f"Skipping {m.id} (no poster URL)")
        continue

    try:
        req = urllib.request.Request(m.poster_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            with open(file_path, "wb") as f:
                f.write(data)
            success += 1
            print(f"[CACHED] {m.title} ({len(data)} bytes)")
    except Exception as e:
        print(f"[FAIL] {m.title}: {e}")
    time.sleep(0.05)

db.close()
print(f"\nDone! Successfully cached {success} / {len(movies)} posters.")

