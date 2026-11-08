import urllib.request

for mid in ['m_kd_01', 'm_kd_02', 'm_q4_02', 'm_hw_01']:
    url = f'http://127.0.0.1:8000/api/catalog/poster/{mid}'
    with urllib.request.urlopen(url) as r:
        ct = r.headers.get("Content-Type")
        size = len(r.read())
        print(f"{mid} -> HTTP {r.status}, Content-Type: {ct}, Size: {size} bytes")

