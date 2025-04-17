#!/usr/bin/env python3
import os
import requests
import fitz             
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("PROTOCOLS_IO_ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise RuntimeError("Missing PROTOCOLS_IO_ACCESS_TOKEN in .env")

HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
BASE_URL = "https://www.protocols.io/api/v3"


BASE_DIR = Path(__file__).resolve().parent.parent   # backend/src → backend
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def load_common_protocols(filepath=BASE_DIR/"src"/"common_protocols.txt"):
    return [line.strip() for line in open(filepath) if line.strip()]

def list_protocols(key, page_size=5):
    url = f"{BASE_URL}/protocols"
    params = {"key": key, "filter":"public", "page_size": page_size, "page_id": 1}
    return requests.get(url, headers=HEADERS, params=params).json().get("items", [])

def download_pdf(protocol_id):
    """
    Returns PDF bytes, or None on failure.
    """
    url = f"https://www.protocols.io/view/{protocol_id}.pdf"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.content
    else:
        print(f"PDF download failed for {protocol_id}: {r.status_code}")
        return None

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def save_text(protocol_id, title, raw_text):
    safe_title = title.replace(" ", "_").replace("/", "-")
    filename = f"{safe_title}_{protocol_id}.txt"
    filepath = DATA_DIR / filename
    filepath.write_text(raw_text, encoding="utf-8")
    print(f"Saved to {filepath}")

def main():
    terms = load_common_protocols()
    for term in terms:
        print(f"Searching for: {term}")
        for proto in list_protocols(term):
            pid   = proto["id"]
            title = proto["title"]
            print(f"Processing: {title} ({pid})")

            pdf = download_pdf(pid)
            if not pdf:
                continue

            text = extract_text_from_pdf(pdf)
            save_text(pid, title, text)

if __name__ == "__main__":
    main()