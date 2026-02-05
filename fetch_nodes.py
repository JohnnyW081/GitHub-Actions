import requests
import re

# --------------------------
# 节点源列表
# --------------------------
sources = [
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/all_extracted_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vmess_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/trojan_configs.txt",
]

headers = {"User-Agent": "Mozilla/5.0"}

# --------------------------
# 节点分类函数
# --------------------------
def classify_node(node: str):
    node = node.strip()
    if node.startswith("vmess://"):
        return "vmess"
    elif node.startswith("trojan://"):
        return "trojan"
    elif node.startswith("trojan-go://"):
        return "trojan-go"
    else:
        return "unknown"

# --------------------------
# 抓取节点
# --------------------------
all_nodes = set()
for url in sources:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        lines = [l.strip() for l in r.text.splitlines() if l.strip()]
        print(f"[DEBUG] {url} fetched {len(lines)} lines")
        all_nodes.update(lines)
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}")

print(f"[INFO] Total nodes before classification: {len(all_nodes)}")

# --------------------------
# 分类输出
# --------------------------
vmess_nodes = [n for n in all_nodes if classify_node(n) == "vmess"]
trojan_nodes = [n for n in all_nodes if classify_node(n) == "trojan"]
trojan_go_nodes = [n for n in all_nodes if classify_node(n) == "trojan-go"]

# --------------------------
# 写入 TXT 文件
# --------------------------
def write_txt(filename, nodes):
    with open(filename, "w", encoding="utf-8") as f:
        for n in nodes:
            f.write(n + "\n")
    print(f"[INFO] {filename} generated with {len(nodes)} nodes")

write_txt("v2rayN_nodes.txt", all_nodes)
write_txt("vmess.txt", vmess_nodes)
write_txt("trojan.txt", trojan_nodes)
write_txt("trojan-go.txt", trojan_go_nodes)
