import requests
import json
import warnings
import csv
import os
# v1.0 by travis knapp
# Suppress the NotOpenSSLWarning warning
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# Welcome banner
welcome_banner = """
   _____ __________                       
  /  _  \\______   \                      
 /  /_\  \|     ___/                      
/    |    \    |                          
\____|__  /____|                          
        \/                                
.___ _______  ___________________         
|   |\      \ \_   _____/\_____  \        
|   |/   |   \ |    __)   /   |   \       
|   /    |    \|     \   /    |    \      
|___\____|__  /\___  /   \_______  /      
            \/     \/            \/       
  ______________________________          
 /  _____/\_   _____/\__    ___/          
/   \  ___ |    __)_   |    |             
\    \_\  \|        \  |    |             
 \______  /_______  /  |____|             
        \/        \/                      
___________________   ________  .____     
\__    ___/\_____  \  \_____  \ |    |    
  |    |    /   |   \  /   |   \|    |    
  |    |   /    |    \/    |    \    |___ 
  |____|   \_______  /\_______  /_______ \               
                   
"""

print(welcome_banner)

# Prompt the user for the controller IP, username, password, and output CSV file name
controller_ip = input("Enter the Mobility Conductor or Controller IP: ")
username = input("Enter the username: ")
password = input("Enter the password: ")
csv_file_name = input("Enter the name for the CSV file (without extension): ") + '.csv'

# Disable warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def run_show_command(session, headers, command):
    show_command_url = f'https://{controller_ip}:4343/v1/configuration/showcommand?command={command}'
    response = session.get(show_command_url, headers=headers, verify=False)
    response.raise_for_status()

    # Process the show command response
    show_data = response.json()
    return show_data

try:
    # Login to the controller
    login_url = f'https://{controller_ip}:4343/v1/api/login'
    login_data = {
        'username': username,
        'password': password
    }

    session = requests.Session()
    response = session.post(login_url, data=login_data, verify=False)
    response.raise_for_status()

    # Extract CSRF token from the login response
    csrf_token = response.json().get('_global_result', {}).get('X-CSRF-Token')
    if not csrf_token:
        raise ValueError("CSRF token not found in the login response")

    # Define headers including the CSRF token
    headers = {
        'X-CSRF-Token': csrf_token
    }

    # Run the show command to get AP database long details
    command = 'show+ap+database+long'
    show_data = run_show_command(session, headers, command)

    # Extract AP details from show command response
    ap_list = []
    for ap in show_data.get('AP Database', []):
        serial_number = ap.get('Serial #', 'N/A')
        mac_address = ap.get('Wired MAC Address', 'N/A')
        tag_name1 = ap.get('Group', 'N/A')
        tag_name2 = ap.get('IP Address', 'N/A')
        ap_list.append({
            'Serial_No': serial_number,
            'MAC_Address': mac_address,
            'tag:name1': tag_name1,  # Assuming these tags are not provided by the API
            'tag:name2': tag_name2,
            'Location_Name (Optional)': '',  # Optional, can be populated if available
            'Contact_Email (Optional)': ''  # Optional, can be populated if available
        })

    # Define the output CSV file path
    output_file_path = os.path.join(os.getcwd(), csv_file_name)

    # Write AP details to CSV
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Serial_No', 'MAC_Address', 'tag:name1', 'tag:name2', 'Location_Name (Optional)', 'Contact_Email (Optional)'])
        writer.writeheader()
        for ap in ap_list:
            writer.writerow(ap)

except requests.exceptions.HTTPError as http_err:
    pass  # Suppressing HTTP error messages
except Exception as err:
    pass  # Suppressing all other error messages
finally:
    # Logout
    try:
        logout_url = f'https://{controller_ip}:4343/v1/api/logout'
        response = session.post(logout_url, headers=headers, verify=False)
        response.raise_for_status()
    except Exception as e:
        pass  # Suppressing logout error messages

# Welcome banner
end_banner = """
  _____  .____    .____                                                       
  /  _  \ |    |   |    |                                                      
 /  /_\  \|    |   |    |                                                      
/    |    \    |___|    |___                                                   
\____|__  /_______ \_______ \                                                  
        \/        \/       \/                                                  
________   ________    _______  ___________._.                                 
\______ \  \_____  \   \      \ \_   _____/| |                                 
 |    |  \  /   |   \  /   |   \ |    __)_ | |                                 
 |    `   \/    |    \/    |    \|        \ \|                                 
/_______  /\_______  /\____|__  /_______  / __                                 
        \/         \/         \/        \/  \/                                   
                                                                               
                                                                                     
                   
"""

print(end_banner)