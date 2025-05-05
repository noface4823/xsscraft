import requests
import time
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
 __  ______ ____    _____ _   _ _______________ ____  
 \ \/ / ___/ ___|  |  ___| | | |__  /__  / ____|  _ \ 
  \  /\___ \___ \  | |_  | | | | / /  / /|  _| | |_) |
  /  \ ___) |__) | |  _| | |_| |/ /_ / /_| |___|  _ < 
 /_/\_\____/____/  |_|    \___//____/____|_____|_| \_\
                                                      
             XSS Reflection Fuzzer (by noface)
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

    headers = {
        "User-Agent": "Mozilla/5.0 (XSS Fuzzer)"
    }

    for i, payload in enumerate(payloads, 1):
        fuzzed_url = url_template.replace("FUZZ", requests.utils.quote(payload))
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

