import requests
import os
import concurrent.futures
import sys
import json
import urllib3

print('''
  ________           ___ 
 / ___/ _ \___ _  __|_  |
/ /__/ , _/ -_) |/ / __/ 
\___/_/|_|\__/|___/____/ 
                         ''')
print("CRev2 - Reverse IP to Domain")
print("Github: IM-Hanzou\n")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "https://api.webscan.cc/?action=query&ip="
file_input = input("List IPs: ")
file_result = input("Result filename: ")

try:
    threads = int(input("Thread: "))
    if threads <= 0:
        raise ValueError
except ValueError:
    print("Please provide a valid number!")
    sys.exit()

if not os.path.exists(file_result):
    open(file_result, "w").close()

def reverse(ip):
    response = requests.get(url + ip, verify=False)
    data = response.json()
    domains = [item['domain'] for item in data]
    total_domains = len(domains)
    print(f"From IP {ip} we got {total_domains} domains")
    with open(file_result, "a", encoding="utf-8") as f:
        for domain in domains:
            f.write(domain + "\n")

try:
    ips = []
    with open(file_input, "r") as f:
        ips = f.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = [executor.submit(reverse, ip) for ip in ips]

except KeyboardInterrupt:
    print("\nStopped!")
finally:
    print(f"Result saved to {file_result}")
