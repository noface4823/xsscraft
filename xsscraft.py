from colorama import Fore, Style, init
import random
import requests
import re
import sys
import argparse
import os

# Initialize Colorama
init(autoreset=True)

# Banner
banner = f"""{Fore.RED}{Style.BRIGHT}
██╗  ██╗███████╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗
╚██╗██╔╝██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
 ╚███╔╝ ███████╗███████╗██║     ██████╔╝███████║█████╗     ██║
 ██╔██╗ ╚════██║╚════██║██║     ██╔══██╗██╔══██║██╔══╝     ██║
██╔╝ ██╗███████║███████║╚██████╗██║  ██║██║  ██║██║        ██║
╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝

             {Fore.YELLOW}- Author : noface{Style.RESET_ALL}
"""

print(banner)

# List of user agents (you can add more user agents here)
user_agents = [
 # Desktop browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",

    # Mobile browsers
    "Mozilla/5.0 (Windows NT 10.0; Mobile; rv:96.0) Gecko/96.0 Firefox/96.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ3A.200805.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-J700F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/16E227 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.1.0; Nexus 6P Build/OPM6.171019.030) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36",

    # Web crawlers / bots
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +https://duckduckgo.com/duckduckbot)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; ARM; Microsoft Windows 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edg/80.0.361.66",

    # Additional mobile User-Agent
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edge/90.0.818.56",
]

# Function to get payloads from a file
def get_payloads(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Function to fuzz GET requests
def fuzz_get(url_template, payloads, save_to_file, file_name):
    print(Fore.CYAN + "\n[+] Starting GET fuzzing...")
    reflected_payloads = []
    for payload in payloads:
        target_url = url_template.replace("FUZZ", payload)
        headers = {'User-Agent': random.choice(user_agents)}
        try:
            response = requests.get(target_url, headers=headers)
            if payload in response.text:
                print(Fore.RED + Style.BRIGHT + f"[✔] Reflected payload: {payload}")
                reflected_payloads.append(payload)
            else:
                print(Fore.LIGHTBLACK_EX + Style.BRIGHT + f"[x] Not reflected: {payload}")
        except Exception as e:
            print(f"[!] Error with payload {payload}: {e}")

    if save_to_file:
        with open(file_name, "w") as f:
            for payload in reflected_payloads:
                f.write(payload + "\n")
        print(f"[+] Reflected payloads saved to {file_name}")

# Function to parse raw POST request file
def parse_raw_post_file(file_path):
    with open(file_path, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]

    method_line = lines[0]
    headers = {}
    data = ""
    is_body = False

    for line in lines[1:]:
        if line == "":
            is_body = True
            continue
        if not is_body:
            key, val = line.split(":", 1)
            headers[key.strip()] = val.strip()
        else:
            data += line + "&" if data else line

    path = method_line.split(" ")[1]
    host = headers.get("Host", "")
    url = f"http://{host}{path}"
    return url, headers, data

# Function to fuzz POST requests
def fuzz_post(raw_file, payloads, save_to_file, file_name):
    print(Fore.CYAN + "\n[+] Parsing raw POST file...")
    reflected_payloads = []
    try:
        url, headers, data_template = parse_raw_post_file(raw_file)
    except Exception as e:
        print(f"[!] Error parsing POST file: {e}")
        return

    # Custom headers to bypass WAF
    headers.update({
        'User-Agent': random.choice(user_agents),
        'X-Forwarded-For': '192.168.1.1',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Custom-Header': 'CustomHeaderValue',
        'Referer': 'http://example.com',
        'Origin': 'http://example.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    })

    print(f"[+] Target URL: {url}")
    print(Fore.CYAN + "[+] Starting POST fuzzing...")

    for payload in payloads:
        data = data_template.replace("FUZZ", payload)
        headers['User-Agent'] = random.choice(user_agents)
        # Add custom headers to bypass WAF
        headers['X-Custom-Header'] = 'CustomHeaderValue'
        try:
            response = requests.post(url, data=data, headers=headers)
            if payload in response.text:
                print(Fore.RED + Style.BRIGHT + f"[✔] Reflected payload: {payload}")
                reflected_payloads.append(payload)
            else:
                print(Fore.LIGHTBLACK_EX + Style.BRIGHT + f"[x] Not reflected: {payload}")
        except Exception as e:
            print(f"[!] Error with payload {payload}: {e}")

    if save_to_file:
        with open(file_name, "w") as f:
            for payload in reflected_payloads:
                f.write(payload + "\n")
        print(f"[+] Reflected payloads saved to {file_name}")

# Main function
def main():
    print(Fore.YELLOW + "\n=== Simple GET/POST Fuzzer ===")
    req_type = input("Enter request type (GET/POST): ").strip().upper()

    # Ask if the user wants to save reflected payloads to a file
    save_to_file = input("Do you want to save reflected payloads to a file? (yes/no): ").strip().lower() == 'yes'

    # Ask for file name if user wants to save payloads
    file_name = ""
    if save_to_file:
        file_name = input("Enter the name of the file to save the reflected payloads: ").strip()

    if req_type == "GET":
        url_template = input("Enter GET URL (use FUZZ where payloads go): ").strip()
        payload_file = input("Enter path to payload list file: ").strip()
        payloads = get_payloads(payload_file)
        fuzz_get(url_template, payloads, save_to_file, file_name)

    elif req_type == "POST":
        raw_post_file = input("Enter path to raw POST request file (with FUZZ in body): ").strip()
        payload_file = input("Enter path to payload list file: ").strip()
        payloads = get_payloads(payload_file)
        fuzz_post(raw_post_file, payloads, save_to_file, file_name)

    else:
        print(Fore.RED + "[!] Invalid request type. Use GET or POST.")

if __name__ == "__main__":
    main()

