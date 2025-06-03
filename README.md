	•	Python 3.x
	•	requests library# getapinfo
# Aruba AP Info Extractor

A Python script to extract Access Point (AP) information from Aruba Mobility Conductors or Controllers and export the data to a CSV file.

## Overview

This script connects to an Aruba wireless controller via REST API, retrieves detailed AP database information, and exports it to a CSV file format suitable for inventory management or bulk configuration operations.

## Features

- Connects to Aruba Mobility Conductors and Controllers
- Retrieves comprehensive AP database information
- Exports data to CSV format
- Handles authentication and session management
- Suppresses SSL warnings for self-signed certificates
- Clean error handling with suppressed error messages

## Requirements

### Python Dependencies
- `requests` - For HTTP API calls
- `json` - For JSON data processing (built-in)
- `csv` - For CSV file operations (built-in)
- `os` - For file path operations (built-in)
- `warnings` - For warning management (built-in)

### Network Requirements
- Network connectivity to the Aruba controller
- HTTPS access on port 4343
- Valid credentials for the controller

## Installation

1. Ensure Python 3.x is installed on your system
2. Install required dependencies:
```bash
pip install requests
```
3. Download the `getapinfo.py` script

## Usage

1. Run the script:
```bash
python getapinfo.py
```

2. When prompted, provide the following information:
   - **Controller IP**: The IP address of your Mobility Conductor or Controller
   - **Username**: Your controller login username
   - **Password**: Your controller login password
   - **CSV filename**: Desired name for the output file (without .csv extension)

### Example Session
```
Enter the Mobility Conductor or Controller IP: 192.168.1.100
Enter the username: admin
Enter the password: ********
Enter the name for the CSV file (without extension): ap_inventory
```

## Output Format

The script generates a CSV file with the following columns:

| Column | Description | Source |
|--------|-------------|---------|
| `Serial_No` | AP Serial Number | From AP Database |
| `MAC_Address` | Wired MAC Address | From AP Database |
| `tag:name1` | Group Assignment | From AP Database |
| `tag:name2` | IP Address | From AP Database |
| `Location_Name (Optional)` | Location Information | Currently empty - can be populated manually |
| `Contact_Email (Optional)` | Contact Information | Currently empty - can be populated manually |

## API Endpoint Used

The script utilizes the following Aruba controller API endpoint:
- **Command**: `show ap database long`
- **URL Pattern**: `https://{controller_ip}:4343/v1/configuration/showcommand?command=show+ap+database+long`

## Security Considerations

- The script disables SSL certificate verification for self-signed certificates
- Passwords are entered interactively (not stored in the script)
- Sessions are properly closed with logout functionality
- CSRF tokens are handled automatically

## Error Handling

The script includes comprehensive error handling that:
- Suppresses detailed error messages for cleaner output
- Handles HTTP errors gracefully
- Ensures proper session cleanup (logout) even if errors occur
- Manages SSL/TLS certificate warnings

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify controller IP address and network connectivity
   - Ensure port 4343 is accessible
   - Check firewall settings

2. **Authentication Failed**
   - Verify username and password credentials
   - Ensure account has sufficient privileges to run show commands

3. **Empty CSV Output**
   - Verify APs are connected and visible in the controller
   - Check if the controller has AP database information populated

4. **SSL/Certificate Errors**
   - The script automatically handles self-signed certificates
   - If issues persist, verify HTTPS connectivity manually

### File Output Location

The CSV file is created in the same directory where the script is executed. Check your current working directory if you cannot locate the output file.

## Version Information

- **Version**: 1.0
- **Author**: Travis Knapp
- **Compatible with**: Aruba Mobility Conductors and Controllers with REST API support

## License

This script is provided as-is for educational and administrative purposes. Please ensure compliance with your organization's security policies when using API-based tools.

## Support
NO SUPPORT

---


