import requests
import re

SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
]

TIMEOUT = 15

def fetch(url):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200 and r.text.strip():
            print(f"[OK] {url} ({len(r.text)})")
            return r.text
        else:
            print(f"[EMPTY] {url}")
    except Exception as e:
        print(f"[FAIL] {url} -> {e}")
    return ""

def main():
    nodes = set()

    for url in SOURCES:
        data = fetch(url)
        if not data:
            continue

        vmess = re.findall(r"vmess://[A-Za-z0-9+/=]+", data)
        trojan = re.findall(r"trojan://[^\s]+", data)

        for n in vmess + trojan:
            nodes.add(n.strip())

    print(f"[TOTAL] {len(nodes)} nodes")

    with open("v2rayN_nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(nodes)))

if __name__ == "__main__":
    main()
