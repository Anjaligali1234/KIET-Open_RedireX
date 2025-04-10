# KIET-Open_RedireX  
**A Fuzzer for Detecting Open Redirect Vulnerabilities**

**KIET-Open_RedireX** is a tool designed to detect open redirect vulnerabilities in web applications. It helps security researchers and penetration testers identify URLs that are susceptible to redirection attacks.

---

## 🚀 Features
- 🔍 Fast and efficient open redirect vulnerability scanning  
- ✍️ Customizable payloads and detection patterns  
- ⚡ Concurrent scanning capabilities  
- 💻 Easy-to-use command-line interface  
- 🧪 Customizable fuzzing engine  
- 📊 Comprehensive reporting capabilities  
- 🧵 Parallel processing and various payload encoding options  

---

## 📦 Installation
all necessary tools, requirements update and upgrade to latest versions upto date 2025

1. python3 
2. Virtual Box
3. Kali Linux
4. git - install on kali

5. git clone https://github.com/Anjaligali1234/KIET-Open_RedireX.git
6. cd KIET-Open_RedireX
7. pip install -r requirements.txt

📁 File Structure : List of files and folders in KIET-Open_RedireX main directory

KIET-Open_RedireX/
├── static/
├── KIET-CyberCrew-RedireX.py
├── LICENSE
├── README.md
├── payloads.txt
├── requirements.txt
├── server.py
├── setup.sh
└── urls.txt

🛠️ Usage

 ✅ Terminal 1 (Main Scanner)

cd KIET-Open_RedireX

sudo su  # Enter root terminal

python3 KIET-CyberCrew-RedireX.py -k FUZZ -c 1 < urls.txt

✅ Terminal 2 (Local Redirect Server)

cd KIET-Open_RedireX

sudo su   # Enter root terminal

python server.py



📝 Input Format
Your urls.txt file should contain URLs where FUZZ marks the injection point for the payloads.

https://example.com/redirect?url=FUZZ

https://example.com/redirect.php?url=FUZZ

https://example.com/redirect?next=FUZZ

Where:

-k FUZZ: Specifies the keyword to replace in URLs (FUZZ will be replaced with payload)
-c 1: Sets concurrency level to 1 (number of simultaneous requests)
urls.txt: A file containing target URLs, one per line


🔧 Command-Line Options
Option	Description
-h, --help	Show help message and exit
-k KEYWORD, --keyword KEYWORD	Keyword to replace with payloads (default: FUZZ)
-p PAYLOAD_FILE, --payload-file PAYLOAD_FILE	File containing payloads (default: payloads.txt)
-c CONCURRENCY, --concurrency CONCURRENCY	Number of concurrent requests (default: 10)
-t TIMEOUT, --timeout TIMEOUT	Request timeout in seconds (default: 5)
-o OUTPUT, --output OUTPUT	Output file to save results
-v, --verbose	Enable verbose output



💡 Example
Create a file named urls.txt with potential vulnerable URLs:

https://example.com/redirect?url=FUZZ

https://vulnerable-site.com/redirect?next=FUZZ


Run the Fuzzing Scanner:

python3 KIET-CyberCrew-RedireX.py -k FUZZ -c 1 < urls.txt

Review the results to identify vulnerable endpoints.

🤝 Contributing
Contributions are welcome!
Please feel free to submit a Pull Request or open an Issue for improvements.

📄 License
This project is licensed under the MIT License.

