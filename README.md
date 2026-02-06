# IP 连通性监控小工具

一个基于 Python + Flask + 前端网页的轻量级网络监控小工具，用于实时监控指定 IP 的连通性和延迟。  

适合家庭或公司小型网络监控，也可以扩展为专业监控面板。

---

## 功能特点

- **实时 ICMP Ping**：每 3 秒刷新指定 IP 的状态  
- **状态 + 延迟显示**：显示 `up/down` + 延迟(ms)  
- **延迟分级显示**：
  - <50ms → 绿色（良好）  
  - 50~200ms → 橙色（一般）  
  - >200ms 或 down → 红色（异常/不可达）  
- **在线管理 IP**：支持添加/删除 IP，无需重启服务  
- **后台运行 & 开机自启**：可配置 systemd 服务  
- **轻量快速**：前端秒开，后台线程异步 ping，不阻塞  

---

## 项目目录结构

ip-monitor/
├── server.py # 后端 Flask 程序
├── ips.txt # IP 列表文件（自动生成）
├── templates/
│ └── index.html # 前端网页
├── README.md # 项目说明
└── server.log # 日志文件（可选）

- `server.py` → 主程序  
- `ips.txt` → 保存监控 IP，每行一个  
- `templates/index.html` → 前端页面  
- `server.log` → nohup / 日志输出  

---

## 安装与运行

### 1. 安装依赖

```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install flask


2. 下载项目
git clone https://github.com/<你的用户名>/ip-monitor.git
cd ip-monitor

3. 本地运行（调试用）
python3 server.py


默认访问：http://127.0.0.1:5000
 或 http://服务器IP:5000

4. 后台运行（长期监控）
方法 1：使用 nohup
nohup python3 /root/ip-monitor/server.py > server.log 2>&1 &


> server.log 2>&1 将日志输出到 server.log

用 ps aux | grep server.py 查看是否运行

用 kill PID 停掉

方法 2：使用 systemd（推荐）

创建服务文件 /etc/systemd/system/ipmonitor.service：

[Unit]
Description=IP Monitor Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/ip-monitor
ExecStart=/usr/bin/python3 /root/ip-monitor/server.py
Restart=always

[Install]
WantedBy=multi-user.target


启动并设置开机自启：

sudo systemctl daemon-reload
sudo systemctl start ipmonitor
sudo systemctl enable ipmonitor


查看日志：

sudo journalctl -u ipmonitor -f


停止或重启：

sudo systemctl stop ipmonitor
sudo systemctl restart ipmonitor

前端使用说明

打开浏览器访问 http://服务器IP:5000

输入 IP 点击“添加 IP”即可监控

点击“删除”按钮可删除 IP

每 3 秒自动刷新状态

延迟显示为绿色/橙色/红色圆点或文字

示例：

10.0.0.1 : up (19.6 ms)
193.26.157.226 : down (-)
23.94.84.109 : up (228 ms)

可扩展功能

TCP/UDP 端口检测：可检测服务端口连通性

自定义刷新间隔：可调整 ping 刷新频率

延迟排序：慢的 IP 排下方，高优先显示

仪表盘风格：红黄绿方块或图表显示

技术栈

Python 3

Flask

HTML + JavaScript + CSS

开源协议

MIT License

联系方式

如有问题或建议，请在 GitHub Issue 提问或联系作者。
