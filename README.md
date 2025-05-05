# XSSCraft

**XSSCraft** is a lightweight and colorful reflected XSS fuzzing tool. It injects custom payloads from a wordlist into a target URL (using a `FUZZ` marker) and checks if the payload is reflected in the server's response — helping identify reflected Cross-Site Scripting vulnerabilities quickly and efficiently.

---

## 📁 Repo Contents

- `xsscraft.py` – Main Python script to perform the fuzzing.
- `payloads.txt` – Sample wordlist of common XSS payloads.

---

## ⚙️ Requirements

- Python 3.x
- `colorama` module for colored output (install instructions below)

---

## 🔧 Installation

```bash
git clone https://github.com/noface4823/xsscraft.git
cd xsscraft
pip install colorama
🚀 How to Use
Prepare your URL:
Make sure your target URL includes the keyword FUZZ where the payload should be injected.
Example:

arduino
Copy
Edit
https://example.com/search/FUZZ
Run the tool:

bash
Copy
Edit
python3 xsscraft.py
Follow the prompts:

Enter the target URL with FUZZ

Enter the path to your XSS payload wordlist (e.g., payloads.txt)

Choose whether to save reflected (vulnerable) URLs to a file

If yes, enter the output filename

🎯 Sample Output
javascript
Copy
Edit
[001] NOT VULNERABLE | No reflection     | <script>alert(1)</script>
[002] VULNERABLE     | Payload reflected | <img src=x onerror=alert(1)>
      -> https://target.com/search/%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E
✅ Green = Payload not reflected (safe)

🔴 Red = Payload reflected (potential XSS)

🧪 Wordlist
You can use the provided xss.txt or plug in your own custom payload list.

💡 Tip
The tool uses simple reflection matching, so if the payload appears exactly in the response body, it will be marked as reflected.
