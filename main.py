#!/usr/bin/python3
import os
import sys
import time

BANNER = """
\033[91m
  _      _____ _   _ _______ _____  
 | |    |_   _| \ | |__   __|  __ \ 
 | |      | | |  \| |  | |  | |__) |
 | |      | | | . ` |  | |  |  ___/ 
 | |____ _| |_| |\  |  | |  | |     
 |______|_____|_| \_|  |_|  |_|     
\033[0m
\033[93m>>> Ethical DDoS Testing Tool <<<\033[0m
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(BANNER)

def print_menu():
    print("\033[91m╔═════════════════════════╗")
    print("\033[91m║      \033[93mLUKHA BOMBER\033[91m       ║")
    print("\033[91m╠═════════════════════════╣")
    print("\033[91m║ \033[95m1.\033[91m \033[97mDDoS Saldırısı Başlat \033[91m║")
    print("\033[91m║ \033[95m2.\033[91m \033[97mGereksinimleri Yükle  \033[91m║")
    print("\033[91m║ \033[95m3.\033[91m \033[97mÇıkış                 \033[91m║")
    print("\033[91m╚═════════════════════════╝\033[0m")

def print_attack_types():
    print("\n\033[93mHedef türünü seçin:\033[0m")
    print("\033[94m1.\033[0m Site (HTTP Flood)")
    print("\033[94m2.\033[0m TCP Flood")
    print("\033[94m3.\033[0m UDP Flood")
    print("\033[94m4.\033[0m Minecraft Sunucusu")

def install_requirements():
    print("\n\033[93mGereksinimler yükleniyor...\033[0m")
    os.system("pip install pysocks")
    print("\033[92mYükleme tamamlandı!\033[0m")
    input("Devam etmek için Enter'a basın...")

def get_input(prompt, default=None, is_int=False):
    while True:
        val = input(f"\033[96m{prompt}\033[0m").strip()
        if val == "" and default is not None:
            return default
        if is_int:
            if val.isdigit() and int(val) > 0:
                return int(val)
            else:
                print("\033[91mLütfen geçerli pozitif bir sayı girin.\033[0m")
        else:
            return val

def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        choice = input("\n\033[95mSeçiminiz (1-3): \033[0m").strip()

        if choice == "1":
            target = get_input("Hedef IP veya Domain (örnek: example.com): ")
            port = get_input("Port numarası (default 80): ", default=80, is_int=True)
            threads = get_input("Thread sayısı (default 200): ", default=200, is_int=True)
            total_requests = get_input("Toplam gönderilecek paket sayısı: ", is_int=True)

            print_attack_types()
            attack_choice = input("\033[95mSeçiminiz (1-4): \033[0m").strip()

            if attack_choice == "1":
                attack_target = "http"
            elif attack_choice == "2":
                attack_target = "tcp"
            elif attack_choice == "3":
                attack_target = "udp"
            elif attack_choice == "4":
                attack_target = "minecraft"
                if port == 80:
                    port = 25565
            else:
                print("\033[91mGeçersiz seçim! Ana menüye dönülüyor...\033[0m")
                time.sleep(1.5)
                continue

            try:
                from lukha import LukhaBomber
            except ImportError:
                print("\033[91mlukha.py dosyası bulunamadı! Aynı klasörde olduğundan emin olun.\033[0m")
                input("Devam etmek için Enter'a basın...")
                continue

            bomber = LukhaBomber(target, port, threads, total_requests, "socks5", attack_target)
            print("\n\033[93mSaldırı başlatılıyor... Ctrl+C ile durdurabilirsiniz.\033[0m")
            bomber.start()
            input("\nDevam etmek için Enter'a basın...")

        elif choice == "2":
            install_requirements()
        elif choice == "3":
            print("\033[93mProgramdan çıkılıyor...\033[0m")
            time.sleep(1)
            sys.exit()
        else:
            print("\033[91mGeçersiz seçim! Lütfen 1 ile 3 arasında bir sayı girin.\033[0m")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
