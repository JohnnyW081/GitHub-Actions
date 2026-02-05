import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------------------------
# 节点源列表
# --------------------------
sources = [
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/all_extracted_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vmess_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/trojan_configs.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_Sub.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
    "https://raw.githubusercontent.com/pourih/pfs-servers-list/refs/heads/main/pfs_servers.txt",
    "https://git.hubp.de/raw-githubusercontent-com/F0rc3Run/F0rc3Run/refs/heads/main/Best-Results/proxies.txt",
]

# --------------------------
# 分类节点
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
# 在线存活检测
# --------------------------
def is_alive(node: str) -> bool:
    try:
        node_type = classify_node(node)
        if node_type == "vmess":
            # vmess 默认存活，可扩展 socket 检测
            return True
        elif node_type in ["trojan", "trojan-go"]:
            # 提取 host 和端口
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
# 多源抓取节点
# --------------------------
all_nodes = set()
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
# 多线程存活检测
# --------------------------
alive_nodes = []
max_workers = 20  # 可调，线程数越大越快

def check_node(node):
    if classify_node(node) != "unknown" and is_alive(node):
        return node
    return None

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_node = {executor.submit(check_node, node): node for node in all_nodes}
    for future in as_completed(future_to_node):
        result = future.result()
        if result:
            alive_nodes.append(result)

print(f"[INFO] Total alive nodes: {len(alive_nodes)}")

# --------------------------
# 按协议分类
# --------------------------
vmess_nodes = [n for n in alive_nodes if classify_node(n) == "vmess"]
trojan_nodes = [n for n in alive_nodes if classify_node(n) == "trojan"]
trojan_go_nodes = [n for n in alive_nodes if classify_node(n) == "trojan-go"]

# --------------------------
# 写入 TXT 文件
# --------------------------
def write_txt(filename, nodes):
    with open(filename, "w", encoding="utf-8") as f:
        for n in nodes:
            f.write(n + "\n")
    print(f"[INFO] {filename} generated with {len(nodes)} nodes")

write_txt("v2rayN_nodes.txt", alive_nodes)
write_txt("vmess.txt", vmess_nodes)
write_txt("trojan.txt", trojan_nodes)
write_txt("trojan-go.txt", trojan_go_nodes)

print("[INFO] All files generated successfully!")
