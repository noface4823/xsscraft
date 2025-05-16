#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from urllib.parse import urlparse, urljoin, parse_qs
import sys
import html

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def banner():
    print(f"""\033[91m
██╗  ██╗███████╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗
╚██╗██╔╝██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
 ╚███╔╝ ███████╗███████╗██║     ██████╔╝███████║█████╗     ██║
 ██╔██╗ ╚════██║╚════██║██║     ██╔══██╗██╔══██║██╔══╝     ██║
██╔╝ ██╗███████║███████║╚██████╗██║  ██║██║  ██║██║        ██║
╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝

             XSS Reflection Fuzzer (noface)
\033[0m""")

def get_input(prompt):
    return input(prompt).strip()

def parse_post_request(raw_post):
    lines = raw_post.strip().split('\n')
    request_line = lines[0]
    headers = {}
    body_lines = []
    is_body = False
    for line in lines[1:]:
        if line.strip() == '':
            is_body = True
            continue
        if not is_body:
            if ':' in line:
                k,v = line.split(':', 1)
                headers[k.strip()] = v.strip()
        else:
            body_lines.append(line)
    body = '\n'.join(body_lines)
    method, path, _ = request_line.split()
    return method, path, headers, body

def check_alert(driver, payload):
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        if payload in alert_text:
            alert.accept()
            return True
        alert.dismiss()
        return False
    except NoAlertPresentException:
        return False

def payload_reflected(driver, payload):
    try:
        if check_alert(driver, payload):
            return True
        try:
            page_text = driver.find_element(By.TAG_NAME, 'body').text
        except:
            page_text = ""
        if payload in page_text:
            return True
        page_source = driver.page_source
        decoded_source = html.unescape(page_source)
        if payload in decoded_source:
            return True
    except:
        pass
    return False

def inject_payload_get(driver, url, payload):
    test_url = url.replace("FUZZ", payload)
    driver.get(test_url)
    time.sleep(3)
    for _ in range(3):
        if payload_reflected(driver, payload):
            return True
        time.sleep(1)
    return False

def inject_payload_post(driver, base_url, path, headers, body, payload):
    full_url = urljoin(base_url, path)
    driver.get(base_url)
    time.sleep(1)
    post_data = body.replace("FUZZ", payload)
    params = parse_qs(post_data)
    js = f"""
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = '{full_url}';
    form.style.display = 'none';
    """
    for k, vs in params.items():
        for v in vs:
            safe_k = k.replace("'", "\\'")
            safe_v = v.replace("'", "\\'")
            js += f"""
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = '{safe_k}';
            input.value = '{safe_v}';
            form.appendChild(input);
            """
    js += "document.body.appendChild(form); form.submit();"
    driver.execute_script(js)
    time.sleep(3)
    for _ in range(3):
        if payload_reflected(driver, payload):
            return True
        time.sleep(1)
    return False

def main():
    banner()
    print("=== Simple GET/POST Fuzzer ===")
    while True:
        req_type = get_input("Enter request type (GET/POST): ").upper()
        if req_type in ['GET', 'POST']:
            break
        print("Invalid input, please enter GET or POST.")

    save_output = get_input("Do you want to save reflected payloads to a file? (yes/no): ").lower() == 'yes'

    if req_type == 'GET':
        url = get_input("Enter GET URL (use FUZZ where payloads go): ")
    else:
        post_file_path = get_input("Enter path to raw POST request file: ")
        try:
            with open(post_file_path, 'r') as f:
                raw_post = f.read()
        except Exception as e:
            print(f"Failed to read POST request file: {e}")
            sys.exit(1)
        method, path, headers, body = parse_post_request(raw_post)
        host = headers.get('Host', '')
        if not host.startswith('http'):
            base_url = f"https://{host}"
        else:
            base_url = host

    payload_file = get_input("Enter path to payload list file: ")
    try:
        with open(payload_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Failed to read payload file: {e}")
        sys.exit(1)

    if save_output:
        output_file = get_input("Enter output file name: ")
        out_f = open(output_file, 'w')
    else:
        out_f = None

    # ===== USER-AGENT LIST =====
    user_agents = [
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
    # ===========================

    print("\nStarting fuzzing...\n")
    reflected = []
    ua_index = 0

    try:
        for payload in payloads:
            # Rotate user-agent
            ua = user_agents[ua_index % len(user_agents)] if user_agents else None
            ua_index += 1

            options = Options()
            options.add_argument('--headless=new')  # or --headless if you're using older Chrome
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            if ua:
                options.add_argument(f"user-agent={ua}")
            driver = webdriver.Chrome(options=options)

            if req_type == 'GET':
                is_reflected = inject_payload_get(driver, url, payload)
            else:
                is_reflected = inject_payload_post(driver, base_url, path, headers, body, payload)

            if is_reflected:
                print(f"{RED}[+] Payload reflected: {payload}{RESET}")
                if out_f:
                    out_f.write(payload + '\n')
                reflected.append(payload)
            else:
                print(f"{GREEN}[-] Not reflected: {payload}{RESET}")
            driver.quit()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        if out_f:
            out_f.close()

    print("\n=== Fuzzing completed ===")
    print(f"Reflected payloads ({len(reflected)}):")
    for p in reflected:
        print(f"{RED} - {p}{RESET}")

if __name__ == "__main__":
    main()
