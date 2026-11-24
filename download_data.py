import shutil
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://opendata.rijdendetreinen.nl/public/"

FILES = [
    "services/services-2025-12.csv.gz",    # one month for quick testing
    "disruptions/disruptions-2025.csv",
    # "services/services-2024.csv.gz",
    # "services/services-2022.csv.gz",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (TIL4030 Group 17 research project)"}

data_dir = Path("data")

for name in FILES:
    dest = data_dir / name
    dest.parent.mkdir(parents=True, exist_ok=True)   # creates data/services/ etc.

    if dest.exists():
        print(f"{name} already exists, skipping")
        continue

    url = BASE_URL + name
    print(f"Downloading {url} ...")
    tmp = dest.with_name(dest.name + ".part")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as r, open(tmp, "wb") as f:
            shutil.copyfileobj(r, f)
        tmp.rename(dest)
        print(f"Saved to {dest}")
    except urllib.error.HTTPError as e:
        print(f"  FAILED ({e.code}) for {name}. Check the file name on the website.")
        tmp.unlink(missing_ok=True)