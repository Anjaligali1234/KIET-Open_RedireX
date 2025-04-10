# KIET-Open_RedireX
- A Fuzzer for Detecting Open Redirect Vulnerabilities
KIET-CyberCrew-RedireX is a tool designed to detect open redirect vulnerabilities in web applications. It helps security researchers and penetration testers identify URLs that are susceptible to redirection attacks. 

Features: 
1.Fast and efficient open redirect vulnerability scanning
2.Customizable payloads and detection patterns
3.Concurrent scanning capabilities
4.Easy to use command-line interface
5.customizable fuzzing engine
6.comprehensive reporting capabilities
7.parallel processing for faster scanningand various payload encoding options



Installation: 
git clone https://github.com/Anjaligali1234/KIET-Open_RedireX.git
cd KIET-Open_RedireX
pip install -r requirements.txt

FILE SYSTEM : List of files and folders in KIET-Open_RedireX main directory

static
KIET-CyberCrew-RedireX.py
LICENSE
README.md
payloads.txt
requirements.txt
server.py
setup.sh
urls.txt

Usage:
  //  1 st terminal 
1. cd KIET-Open_RedireX
2. sudo su - enter into root terminal for administative privileges
3. ls 
4. python3 KIET-CyberCrew-RedireX.py -k FUZZ -c 1 < urls.txt

   // 2nd terminal
1. cd KIET-Open_RedireX
2. sudo su - enter into root terminal for administative privileges
3. python server.py


Input Format:
Your urls.txt file should contain URLs with the FUZZ keyword marking where the payload should be inserted:

https://example.com/redirect?url=FUZZ
https://example.com/redirect.php?url=FUZZ
https://example.com/redirect?next=FUZZ

Where:

-k FUZZ: Specifies the keyword to replace in URLs (FUZZ will be replaced with payload)
-c 1: Sets concurrency level to 1 (number of simultaneous requests)
urls.txt: A file containing target URLs, one per line


Advanced Options
  -h, --help            Show help message
  -k KEYWORD, --keyword KEYWORD
                        Keyword to replace with payloads (default: FUZZ)
  -p PAYLOAD_FILE, --payload-file PAYLOAD_FILE
                        File containing payloads (default: payloads.txt)
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of concurrent requests (default: 10)
  -t TIMEOUT, --timeout TIMEOUT
                        Request timeout in seconds (default: 5)
  -o OUTPUT, --output OUTPUT
                        Output file to save results
  -v, --verbose         Enable verbose output


Example:
Create a file named urls.txt with potential vulnerable URLs:

https://example.com/redirect?url=FUZZ
https://vulnerable-site.com/redirect?next=FUZZ
Run KIET-Open_RedireX:

python3 KIET-CyberCrew-RedireX.py -k FUZZ -c 1 < urls.txt
Review the results to identify vulnerable endpoints.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
