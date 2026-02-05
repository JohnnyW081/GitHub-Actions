import requests
import re
import socket
from urllib.parse import urlparse

# --------------------------
# 配置节点源
# --------------------------
sources = [
    "https://example.com/vmess.txt",
    "https://example2.com/trojan.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/all_extracted_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vmess_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/trojan_configs.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_Sub.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
    "https://raw.githubusercontent.com/pourih/pfs-servers-list/refs/heads/main/pfs_servers.txt",
    "https://git.hubp.de/raw-githubusercontent-com/F0rc3Run/F0rc3Run/refs/heads/main/Best-Results/proxies.txt",
]

    # 可以继续添加更多 URL
]

# --------------------------
# 解析并分类节点
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
# 简单在线存活检测
# --------------------------
def is_alive(node: str) -> bool:
    try:
        if node.startswith("vmess://"):
            # vmess 直接返回 True（可扩展）
            return True
        elif node.startswith("trojan://") or node.startswith("trojan-go://"):
            # 解析 host:port
            match = re.match(r".*://([^:@]+)(?::(\d+))?", node)
            if match:
                host = match.group(1)
                port = int(match.group(2)) if match.group(2) else 443
                sock = socket.create_connection((host, port), timeout=3)
                sock.close()
                return True
        return False
    except Exception:
        return False

# --------------------------
# 抓取所有节点
# --------------------------
all_nodes = set()  # 自动去重

for url in sources:
    try:
        resp = requests.get(url, timeout=10)
        content = resp.text
        for line in content.splitlines():
            line = line.strip()
            if line:
                all_nodes.add(line)
        print(f"[INFO] Fetched {len(content.splitlines())} nodes from {url}")
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}")

print(f"[INFO] Total nodes before filtering: {len(all_nodes)}")

# --------------------------
# 分类 + 存活检测
# --------------------------
alive_nodes = []
for node in all_nodes:
    node_type = classify_node(node)
    if node_type != "unknown" and is_alive(node):
        alive_nodes.append(node)

print(f"[INFO] Total alive nodes: {len(alive_nodes)}")

# --------------------------
# 写入 v2rayN_nodes.txt
# --------------------------
with open("v2rayN_nodes.txt", "w", encoding="utf-8") as f:
    for node in alive_nodes:
        f.write(node + "\n")

print("[INFO] v2rayN_nodes.txt generated successfully!")
