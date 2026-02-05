import requests, re

SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
]

nodes = set()

for url in SOURCES:
    print("Fetching:", url)
    try:
        r = requests.get(url, timeout=15)
        print("Status:", r.status_code, "Size:", len(r.text))
        data = r.text
    except Exception as e:
        print("Error:", e)
        continue

    nodes.update(re.findall(r"vmess://[A-Za-z0-9+/=]+", data))
    nodes.update(re.findall(r"trojan://[^\s]+", data))

print("Total nodes:", len(nodes))

with open("v2rayN_nodes.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(nodes))
