"""LeafVision FastAPI servisi icin duman testi (smoke test).

Onceden calisan bir sunucu bekler (server.py). Calistirmadan once:
    python src/api/server.py
sonra ayri bir terminalde:
    python src/scripts/test_ui.py

Ek bagimlilik gerektirmez, sadece Python stdlib kullanir.
"""
import json
import os
import sys
import urllib.error
import urllib.request

SERVER_URL = os.environ.get("LEAFVISION_URL", "http://127.0.0.1:8000")
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/leaf.jpg"))

EXPECTED_STEPS = {
    "1_original",
    "2_color_mask",
    "3_cleaned_mask",
    "4_distance_map",
    "5_foreground_seeds",
    "6_watershed_markers",
    "7_final_edges",
}


def build_multipart_request(url, field_name, file_path):
    boundary = "----LeafVisionTestBoundary"
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{os.path.basename(file_path)}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    return req


def main():
    print(f"Sunucu test ediliyor: {SERVER_URL}")

    # 1. Ana sayfa erisilebilir mi?
    with urllib.request.urlopen(f"{SERVER_URL}/") as resp:
        assert resp.status == 200, f"Beklenmeyen durum kodu: {resp.status}"
    print("[OK] Ana sayfa (/) erisilebilir.")

    # 2. /process endpoint'i tum pipeline asamalarini eksiksiz donuyor mu?
    req = build_multipart_request(f"{SERVER_URL}/process", "file", IMAGE_PATH)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    assert data.get("success") is True, f"Islem basarisiz: {data}"
    missing = EXPECTED_STEPS - data["pipeline"].keys()
    assert not missing, f"Eksik pipeline asamalari: {missing}"
    print("[OK] /process 7 asamali pipeline'i eksiksiz dondu.")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as e:
        print(f"[HATA] Sunucuya baglanilamadi ({SERVER_URL}). Once server.py'yi calistirin. Detay: {e}")
        sys.exit(1)
    except AssertionError as e:
        print(f"[HATA] {e}")
        sys.exit(1)
    print("Tum testler basarili.")
