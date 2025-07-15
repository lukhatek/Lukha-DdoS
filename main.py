#!/usr/bin/python3
import os
import sys
import time
import random
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

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

def print_banner():
    print(BANNER)

def print_menu():
    print("\033[91m╔════════════════════════╗")
    print("\033[91m║      \033[93mLUKHA BOMBER\033[91m      ║")
    print("\033[91m╠════════════════════════╣")
    print("\033[91m║ \033[95m1.\033[91m \033[97mDDoS Saldırısı\033[91m ║")
    print("\033[91m║ \033[95m2.\033[91m \033[97mGereksinimler\033[91m  ║")
    print("\033[91m║ \033[95m3.\033[91m \033[97mÇıkış               \033[91m║")
    print("\033[91m╚════════════════════════╝\033[0m")

def install_requirements():
    print("\nGereksinimler yükleniyor...")
    os.system("pip install pysocks")
    print("Yükleme tamamlandı!\n")
    input("Devam etmek için Enter'a basın...")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print_menu()
        choice = input("\nSeçiminiz (1-3): ").strip()

        if choice == "1":
            target = input("Hedef IP/Domain: ").strip()
            port_input = input("Port (default 80): ").strip()
            port = int(port_input) if port_input else 80

            threads_input = input("Thread sayısı (default 200): ").strip()
            threads = int(threads_input) if threads_input else 200

            total_requests_input = input("Toplam gönderilecek paket sayısı: ").strip()
            if not total_requests_input.isdigit() or int(total_requests_input) <= 0:
                print("\033[91mGeçersiz paket sayısı!\033[0m")
                time.sleep(1.5)
                continue
            total_requests = int(total_requests_input)

            print("\nHedef türü seçin:")
            print("1. Site (HTTP Flood)")
            print("2. TCP Flood")
            print("3. UDP Flood")
            print("4. Minecraft Sunucusu")
            attack_choice = input("Seçiminiz (1-4): ").strip()

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
                print("\033[91mGeçersiz seçim!\033[0m")
                time.sleep(1.5)
                continue

            # Burada Lukha.py içindeki LukhaBomber sınıfını import edip kullanmalısın
            try:
                from lukha import LukhaBomber
            except ImportError:
                print("\033[91mlukha.py dosyasını bulamıyorum! Aynı dizinde olduğundan emin ol.\033[0m")
                input("Devam etmek için Enter'a basın...")
                continue

            bomber = LukhaBomber(target, port, threads, total_requests, attack_target)
            print("\nSaldırı başlatılıyor...")
            bomber.start()
            input("\nDevam etmek için Enter'a basın...")

        elif choice == "2":
            install_requirements()
        elif choice == "3":
            print("Çıkılıyor...")
            time.sleep(1)
            sys.exit()
        else:
            print("\033[91mGeçersiz seçim! Tekrar deneyin.\033[0m")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
