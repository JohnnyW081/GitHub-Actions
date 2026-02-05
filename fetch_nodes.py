import requests
import re

SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
]

def fetch(url):
    try:
        return requests.get(url, timeout=15).text
    except:
        return ""

def main():
    nodes = set()

    for url in SOURCES:
        data = fetch(url)
        vmess = re.findall(r"vmess://[A-Za-z0-9+/=]+", data)
        trojan = re.findall(r"trojan://[^\s]+", data)

        for n in vmess + trojan:
            nodes.add(n.strip())

    with open("v2rayN_nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(nodes)))

    print(f"Saved {len(nodes)} nodes")

if __name__ == "__main__":
    main()
