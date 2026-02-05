# v2rayN 自动节点生成（vmess / trojan）

本仓库通过 GitHub Actions 每天自动抓取 GitHub 公共免费节点，
生成 **v2rayN 可直接导入的 TXT 文件**。

## 📌 功能
- 自动抓取多个免费节点源
- 提取 vmess / trojan
- 自动去重
- 每日定时更新
- 输出纯节点 TXT（无订阅）

## 📄 输出文件
- `v2rayN_nodes.txt`

Raw 地址示例：
https://raw.githubusercontent.com/JohnnyW081/GitHub-Actions/main/v2rayN_nodes.txt

## 🧰 使用方法
1. 打开上面的 Raw 地址
2. 全选复制
3. v2rayN → 从剪贴板导入

## ⏱ 更新频率
- 每天 UTC 00:00 自动更新
- 支持 Actions 手动运行

## ⚠️ 说明
- 免费节点不保证稳定
- 建议仅用于学习和临时用途
