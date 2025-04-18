# Public Wi-Fi Risk Analyzer

## Overview
The Public Wi-Fi Risk Analyzer is a Python application designed to assess the security of public Wi-Fi networks. It provides users with insights into various security aspects, including HTTPS support, DNS resolution, firewall status, VPN activity, and network connectivity. The application features a user-friendly graphical interface built with Tkinter.

## Features
- Check if HTTPS is supported by accessing secure websites.
- Verify DNS resolution and retrieve the IP address of a domain.
- Assess the status of the firewall based on the operating system.
- Determine if a VPN is active by checking network interfaces.
- Ping a domain to check connectivity.
- Log results with timestamps for future reference.

## Installation
To set up the Public Wi-Fi Risk Analyzer, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/public-wifi-risk-analyzer.git
   ```

2. Navigate to the project directory:
   ```
   cd public-wifi-risk-analyzer
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the Public Wi-Fi Risk Analyzer, execute the following command in your terminal:
```
python src/public_wifi_analyzer.py
```

Once the application is running, click the "Run Scan" button to analyze your network. The results will be displayed in a popup window and logged to a file named `wifi_scan_log.txt`.

## Contributing
Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.