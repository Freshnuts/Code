# Ruddy J. Woel
# Okta API Unlock Script
# Install module requests: py -m pip install requests

import requests
import time
import re

# Authorization to perform actions
print('Enter API Token: ')
read_token = input()

# Okta API URL
# unlock_url = "https://redacted.okta.com/api/v1/users/first.last/lifecycle/unlock"
# list_blocks_url = "https://subdomain.okta.com/api/v1/users/first.last/blocks"
# deprovisioned_users = 'https://redacted.okta.com/api/v1/users?filter=status eq "DEPROVISIONED"'

# Okta API token
api_token = read_token

# Auth. Headers
headers = {
    "Authorization": f"SSWS {api_token}",
    "Content-Type": "application/json"  # Ensure you're sending JSON data if required
}

data = {}

while True:
    if api_token is None:
        break

    print('''
    Menu:
    
    1. Unlock User
    2. Check for locked user
    3. List users with <status>
        - If LOCKED_OUT is chosen a submenu to unlock all users is provided.
    4. Automatically check for locked users & unlock them.
    0. Exit
    ''')

    print('Choose Option: ')
    menu_answer = input()

    if menu_answer == '1':
        print('Unlock User: ')
        unlock_user = input()
        unlock_url = "https://redacted.okta.com/api/v1/users/" + unlock_user + "/lifecycle/unlock"
        user_unlock_response = requests.post(unlock_url, headers=headers, json=data)
        
        if user_unlock_response.status_code == 200:
            print("Request successful!")
            print(user_unlock_response.text)
        else:
            print(f"Request failed with status code {user_unlock_response.status_code}")
            print(user_unlock_response.text)
            
            
    elif menu_answer == '2':
        print('Check for locked user: ')
        list_user = input()
        list_blocks_url = "https://redacted.okta.com/api/v1/users/" + list_user + "/blocks"
        list_blocks_response = requests.get(list_blocks_url, headers=headers, json=data)
        
        if list_blocks_response.status_code == 200:
            print("Request successful!")
            print(list_blocks_response.text)
        else:
            print(f"Request failed with status code {list_blocks_response.status_code}")
            print(list_blocks_response.text)
            
            
    if menu_answer == '3':
        print('''Insert Status:
                    STAGED
                    PROVISIONED
                    ACTIVE
                    RECOVERY
                    PASSWORD_EXPIRED
                    LOCKED_OUT
                    SUSPENDED
                    DEPROVISIONED''')
        user_status = input()
        status_url = 'https://redacted.okta.com/api/v1/users?filter=status eq "' + user_status + '"'
        status_response = requests.get(status_url, headers=headers, json=data)
        
        if status_response.status_code == 200:
            print("Request successful!")
            #print(status_response.text)
            
            data = status_response.text
            # Regular expression to find email addresses
            email_pattern = r'"login"\s*:\s*"([^"]+@[^"]+)"'
            matches = re.findall(email_pattern, data)
            for email in matches:
                print(email)
            
            if user_status == "LOCKED_OUT":
                print("Unlock all users? y or n")
                unlock_user = input()
                if unlock_user == 'y':
                    for email in matches:
                        print("Login:", email)
                        unlock_url = "https://redacted.okta.com/api/v1/users/" + email + "/lifecycle/unlock"
                        user_unlock_response = requests.post(unlock_url, headers=headers, json=data)
                        if status_response.status_code == 200:
                            print("Unlock Request successful!")
                else:
                    print("Users not unlocked.")
                    
                    
    if menu_answer == '4':
        while True:
            status_url = 'https://redacted.okta.com/api/v1/users?filter=status eq "LOCKED_OUT"'
            status_response = requests.get(status_url, headers=headers, json=data)
            
            if status_response.status_code == 200:
                print("Status Request successful!")
                #print(status_response.text)
                
                data = status_response.text
                # Regular expression to find email addresses
                email_pattern = r'"login"\s*:\s*"([^"]+@[^"]+)"'
                matches = re.findall(email_pattern, data)
                for email in matches:
                    print(email)
                    
                if not matches:
                    print("No emails found.")
                elif matches:
                    for email in matches:
                        print("Login:", email)
                        unlock_url = "https://redacted.okta.com/api/v1/users/" + email + "/lifecycle/unlock"
                        user_unlock_response = requests.post(unlock_url, headers=headers, json=data)
                        if status_response.status_code == 200:
                            print("Unlock Request successful!")
                        else:
                            print("Unlock failed.")
                # Frequency 5 minutes = Runs 228 times per 24 hours
                time.sleep(300)
            
    elif menu_answer == '0':
        print('Exit')
        break

