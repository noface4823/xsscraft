# XSSCraft

> **XSS Reflection Fuzzer** by `noface`  
> `██╗  ██╗███████╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗`  
> `╚██╗██╔╝██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝`  
> ` ╚███╔╝ ███████╗███████╗██║     ██████╔╝███████║█████╗     ██║   `  
> ` ██╔██╗ ╚════██║╚════██║██║     ██╔══██╗██╔══██║██╔══╝     ██║   `  
> `██╔╝ ██╗███████║███████║╚██████╗██║  ██║██║  ██║██║        ██║   `  
> `╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   `

## 🔍 Overview

**XSSCraft** is a lightweight but powerful XSS reflection fuzzing tool that supports both **GET** and **POST** based fuzzing using raw HTTP requests and a payload list.

It is designed to help penetration testers and bug bounty hunters test for reflected XSS in web applications by automating fuzzing and checking for reflected payloads.

---

## 🚀 Features

- ✅ Supports both **GET** and **POST** request fuzzing
- 📝 Uses **raw request files** with `FUZZ` markers to inject payloads
- 📁 Saves **reflected payloads** to a specified output file
- 🧪 Clean terminal output with status marking:
  - ✔ Reflected
  - ❌ Not reflected
- 📦 Simple installation and usage with no external modules beyond `requests`

---

## 🛠 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/xsscraft.git
cd xsscraft
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
✅ Only one dependency: requests

📂 File Structure
bash
Copy
Edit
.
├── payloads.txt           # Sample payload list
├── req.txt                # Sample raw request with FUZZ
├── test3.py               # Main fuzzer script
├── requirements.txt       # Required Python packages
├── README.md              # You're here!

▶️ Usage
Run the tool with:

bash
Copy
Edit
python3 xsscraft.py
Follow the prompts:

1. Select Request Type
pgsql
Copy
Edit
Enter request type (GET/POST):
GET: For fuzzing GET parameters

POST: For fuzzing raw body parameters

2. Save Results?
pgsql
Copy
Edit
Do you want to save reflected payloads to a file? (yes/no):
Choose yes if you want the results saved

3. Specify File Name
css
Copy
Edit
Enter the name of the file to save the reflected payloads:
Example: out.txt

4. Load Raw Request File
Burp Suite
Copy
Edit
Enter path to raw POST request file (with FUZZ in body):
Use a file like req.txt with FUZZ where payloads should be inserted.

Example POST raw request (req.txt):

http
Copy
Edit
POST /search.jsp HTTP/1.1
Host: demo.testfire.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 21

query=FUZZ&submit=Search
5. Load Payload List
css
Copy
Edit
Enter path to payload list file:
Example: payloads.txt, payloads2.txt

✅ Output Example
Terminal output:

javascript
Copy
Edit
[✔] Reflected payload: ><script>alert(123)</script>
[x] Not reflected: <script>alert(1)</script>
Saved to out.txt if you chose to store them.

📌 Tips
Make sure your raw request files are accurate.

Always use FUZZ in your raw request to indicate where payloads go.

Payloads must be XSS vectors you wish to test.

If testing POST, ensure Content-Length is approximate or disable checking server-side.

💡 Contributing
Feel free to fork and enhance the tool:
NOTE : use main.py to reduse false positive (slow)
Add proxy support (Burp/ZAP)

🧑‍💻 Author
noface
Red Teamer | Bug Hunter | Cybersecurity Researcher
