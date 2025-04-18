# Public Wi-Fi Risk Analyzer with GUI 

import requests # type: ignore 
import socket
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox
import datetime

# Function to check if HTTPS is supported by trying multiple secure sites
def check_https_multiple():
    test_domains = ["https://google.com", "https://example.com", "https://cloudflare.com"]
    successes = 0
    for domain in test_domains:
        try:
            response = requests.get(domain, timeout=5)
            if response.url.startswith("https://"):
                successes += 1
        except:
            continue
    return successes >= 2

# Function to check DNS resolution by getting IP address of a domain
def check_dns():
    try:
        ip = socket.gethostbyname("google.com")
        return ip  # Expected: 142.250.x.x or similar
    except:
        return None

# Function to check if the firewall is active based on the OS
def check_firewall():
    system = platform.system()
    try:
        if system == "Windows":
            output = subprocess.getoutput("netsh advfirewall show allprofiles")
            return "ON" in output
        elif system == "Darwin":  # macOS
            output = subprocess.getoutput("/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate")
            return "enabled" in output.lower()
        elif system == "Linux":
            output = subprocess.getoutput("sudo ufw status")
            return "active" in output.lower()
    except:
        pass
    return False

# Function to check if VPN is active (based on presence of 'tun0' or 'ppp' interfaces)
def check_vpn():
    try:
        output = subprocess.getoutput("ifconfig" if platform.system() != "Windows" else "ipconfig")
        return "tun0" in output or "ppp" in output or "vpn" in output.lower()
    except:
        return False

# Function to get current Wi-Fi SSID on macOS
def get_wifi_ssid():
    try:
        result = subprocess.getoutput("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
        for line in result.splitlines():
            if " SSID:" in line:
                return line.split(": ")[-1].strip()
    except:
        pass
    return "Unknown"

# Function to ping a domain and check if it responds
def check_ping(domain="google.com"):
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.getoutput(f"ping -n 1 {domain}")
            return "Received = 1" in result
        else:
            result = subprocess.getoutput(f"ping -c 1 {domain}")
            return "1 received" in result or "0% packet loss" in result
    except:
        return False

# Function to log results to a file with timestamp
def log_results(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("wifi_scan_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}]\n{data}\n{'-'*40}\n")

# Function that runs all checks and determines the overall network risk level
def analyze_network_gui():
    https_ok = check_https_multiple()
    dns_ip = check_dns()
    firewall_ok = check_firewall()
    ping_ok = check_ping()
    vpn_ok = check_vpn()
    wifi_ssid = get_wifi_ssid()

    score = 0
    if https_ok:
        score += 1

    trusted_dns_prefixes = ["8.8.", "1.1.", "9.9.", "142.250.", "92.249."]
    if dns_ip and any(dns_ip.startswith(prefix) for prefix in trusted_dns_prefixes):
        score += 1
    elif vpn_ok:
        score += 1

    if firewall_ok:
        score += 1
    if ping_ok:
        score += 1
    if vpn_ok:
        score += 1

    if score == 5:
        risk = "Very Safe"
        color = "#c8e6c9"  # light green
        icon = "✅"
    elif score >= 3:
        risk = "Caution"
        color = "#fff9c4"  # light yellow
        icon = "⚠️"
    else:
        risk = "Dangerous"
        color = "#ffcdd2"  # light red
        icon = "❌"

    result_msg = (
        f"{icon} Network Scan Report\n"
        f"Wi-Fi SSID: {wifi_ssid}\n"
        f"HTTPS: {https_ok}\n"
        f"DNS IP: {dns_ip}\n"
        f"Firewall: {firewall_ok}\n"
        f"Ping: {ping_ok}\n"
        f"VPN Active: {vpn_ok}\n"
        f"\nRisk Score: {score}/5\nRisk Level: {risk}"
    )

    log_results(result_msg)

    # Create a custom popup with colored background and icon based on risk
    popup = tk.Toplevel()
    popup.title("Network Security Report")
    popup.configure(bg=color)

    label = tk.Label(popup, text=result_msg, justify="left", font=("Arial", 12), bg=color)
    label.pack(padx=20, pady=20)

    ok_btn = tk.Button(popup, text="OK", command=popup.destroy)
    ok_btn.pack(pady=10)

# GUI Setup
def main():
    root = tk.Tk()
    root.title("Public Wi-Fi Risk Analyzer")
    root.geometry("400x200")

    label = tk.Label(root, text="Click to Analyze Your Network", font=("Arial", 14))
    label.pack(pady=20)

    scan_btn = tk.Button(root, text="Run Scan", font=("Arial", 12), command=analyze_network_gui)
    scan_btn.pack(pady=10)

    root.mainloop()

# Run the GUI if the script is executed directly
if __name__ == "__main__":
    main()
