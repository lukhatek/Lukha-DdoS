import os
import sys
import time

def install_requirements():
    print("\n[+] Gereken paketler yükleniyor...\n")
    os.system("pip install pysocks")
    print("\n[✓] Kurulum tamamlandı!")
    input("\nDevam etmek için Enter'a bas...")
    main_menu()

def start_ddos():
    os.system("python lukha_bomber_proxy.py")

def main_menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print("""
╔════════════════════════════╗
║         LUKHA BOMBER v2         ║
╠════════════════════════════╣
║ 1. DDoS Saldırısı Başlat        ║
║ 2. Gereksinimleri Yükle         ║
║ 3. Çıkış                        ║
╚════════════════════════════╝
        """)
        choice = input("Seçiminiz (1-3): ")

        if choice == "1":
            start_ddos()
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
