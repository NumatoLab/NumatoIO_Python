#########################################################################################
#   License                                                                             #
#                                                                                       #
#   Copyright © 2025, Numato Systems Private Limited. All rights reserved.              #
#                                                                                       #
#   This software including all supplied files, Intellectual Property, know-how         #
#   Or part of thereof as applicable (collectively called SOFTWARE) in source           #
#   And/Or binary form with accompanying documentation Is licensed to you by            #
#   Numato Systems Private Limited (LICENSOR) subject To the following conditions.      #
#                                                                                       #
#   1. This license permits perpetual use of the SOFTWARE if all conditions in this     #
#       license are met. This license stands revoked In the Event Of breach Of any      #
#       of the conditions.                                                              #
#   2. You may use, modify, copy the SOFTWARE within your organization. This            #
#       SOFTWARE shall Not be transferred To third parties In any form except           #
#       fully compiled binary form As part Of your final application.                   #
#   3. This SOFTWARE Is licensed only to be used in connection with/executed on         #
#       supported products manufactured by Numato Systems Private Limited.              #
#       Using/ executing this SOFTWARE On/In connection With custom Or third party      #
#       hardware without the LICENSORs prior written permission Is expressly            #
#       prohibited.                                                                     #
#   4. You may Not download Or otherwise secure a copy of this SOFTWARE for the         #
#       purpose of competing with Numato Systems Private Limited Or subsidiaries in     #
#       any way such As but Not limited To sharing the SOFTWARE With competitors,       #
#       reverse engineering etc... You may Not Do so even If you have no gain           #
#       financial Or otherwise from such action.                                        #
#   5. DISCLAIMER                                                                       #
#   5.1. USING THIS SOFTWARE Is VOLUNTARY And OPTIONAL. NO PART OF THIS SOFTWARE        #
#       CONSTITUTE A PRODUCT Or PART Of PRODUCT SOLD BY THE LICENSOR.                   #
#   5.2. THIS SOFTWARE And DOCUMENTATION ARE PROVIDED “AS IS” WITH ALL FAULTS,          #
#       DEFECTS And ERRORS And WITHOUT WARRANTY OF ANY KIND.                            #
#   5.3. THE LICENSOR DISCLAIMS ALL WARRANTIES EITHER EXPRESS Or IMPLIED, INCLUDING     #
#       WITHOUT LIMITATION, ANY WARRANTY Of MERCHANTABILITY Or FITNESS For ANY          #
#       PURPOSE.                                                                        #
#   5.4. IN NO EVENT, SHALL THE LICENSOR, IT'S PARTNERS OR DISTRIBUTORS BE LIABLE OR    #
#       OBLIGATED FOR ANY DAMAGES, EXPENSES, COSTS, LOSS Of MONEY, LOSS OF TANGIBLE     #
#       Or INTANGIBLE ASSETS DIRECT Or INDIRECT UNDER ANY LEGAL ARGUMENT SUCH AS BUT    #
#       Not LIMITED TO CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH     #
#       OF WARRANTY Or ANY OTHER SIMILAR LEGAL DEFINITION.                              #
#########################################################################################

#   Python code demonstrating basic Relay features Of Numato Lab WiFi DAQ Module.

#########################################################################################
#                                                                                       #
#                                   Prerequisites                                       #
#                                   -------------                                       #
#                                 Python version 3.x                                    #
#                                  pip version 6.x                                      #
#                                                                                       #
#########################################################################################

#########################################################################################
#       Module       : Wi-Fi DAQ Control Utility                                        #
#       Description  : This script logs into the WiFi DAQ device and provides           #
#                   control and monitoring features. It allows:                         #
#                       - Relay control (ON/OFF)                                        #
#                       - Reading device status                                         #
#                       - ADC raw and voltage readings                                  #
#                       - GPIO input status                                             #
#                       - Relay status                                                  #
#                       - Sensor status                                                 #
#                                                                                       #
#       Company      : Numato Systems Private Limited                                   #
#       Version      : v0.1                                                             #
#       Created      : July 2, 2025                                                     #
#       © 2025 Numato Systems Private Limited. All rights reserved.                     #
#########################################################################################

import time
import requests

#########################################################################################
# Device Login Details
device_ip = "192.168.10.64"                                         # Device IP Address
username = "admin"                                                  # Username
password_web = "YOURPASSWORD"                                       # Password

#########################################################################################
#                                   Utility Functions                                   #
#########################################################################################

# HTTP POST   
def numato_http_post(session, url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json'
    }
    try:
        response = session.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"[{url}] POST success: {data}")
        else:
            print(f"[{url}] POST failed: {response.status_code}")
    except Exception as e:
        print(f"[{url}] POST exception: {e}")

# HTTP GET
def numato_http_get(session, url):
    try:
        response = session.get(url)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                print(f"[{url}] Response not valid JSON")
        else:
            print(f"[{url}] GET failed: {response.status_code}")
    except Exception as e:
        print(f"[{url}] GET exception: {e}")
    return None
    
# Login to the Device
def numato_login_to_web_console(session, login_url, username, password):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    form_data = {
        'user': username,
        'pass': password
    }

    print(f"Attempting to log in to {login_url} with username: {username}")
    response = session.post(login_url, data=form_data, headers=headers)

    if response.status_code == 200:
        print("Logged in successfully!")
        return True
    else:
        print("Failed to log in.")
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        return False

# Relay Control 
def numato_relay_control(session, control_url, relay_num, relay_state):
    data = {
        'relay_num': relay_num,
        'relay_state': relay_state
    }
    numato_http_post(session, control_url, data)        # Posting Control Data

# Device Status - Relay status , ADC status, GPI status and Sensor status.    
def numato_fetch_device_status(session, status_url, device_ip):
    status = numato_http_get(session, status_url)       # Getting Device DAQ STATUS
    if status is not None:

        try:
            data = status['data']
            sensors = {f"sensor_{s['index']}": s['value'] for s in data.get('sensors', [])}
            adcs_raw = {f"adc_{a['index']}": a['value_raw'] for a in data.get('adcs', [])}
            adcs_v = {f"adc_{a['index']}": a['value_v'] for a in data.get('adcs', [])}
            gpis = {f"gpi_{g['index']}": g['value'] for g in data.get('gpis', [])}
            relays = {f"relay_{r['index']}": r['rl_state'] for r in data.get('relays', [])}
            print("\nFetched Device Status:\n")
            print("-> Sensor Data: "        + str(sensors))
            print("-> ADC Raw Value: "      + str(adcs_raw))
            print("-> ADC Voltage Value: "  + str(adcs_v))
            print("-> GPIO Input Value: "   + str(gpis))
            print("-> RELAY STATUS: "       + str(relays))
            print("\n")
        except Exception as e:
            print(f"[{device_ip}] Error parsing or writing status: {e}")
    else:
        print(f"[{device_ip}] Failed to fetch status.")

#########################################################################################
#                                    Main application code                              #
#########################################################################################
  
def numato_control_device(device_ip):
    login_url = f"http://{device_ip}/login"
    control_url = f"http://{device_ip}/api/v0/relay/control"
    status_url = f"http://{device_ip}/api/v0/status"
    
    session = requests.Session()
    # Logging in to the Web
    while True:
        try:
            if numato_login_to_web_console(session, login_url, username, password_web): # Logging in to the Device
                break
            else:
                print(f"[{device_ip}] Login failed. Retrying in 5 seconds...")
        except Exception as e:
            print(f"[{device_ip}] Exception during login: {e}")
        time.sleep(5)

    # Relay control loop
    
    print("\nTurning OFF All Relays:\n")
    for i in range(4):
        numato_relay_control(session, control_url, i, 0)        # Turning OFF All Relays
    print("\n")
    numato_fetch_device_status(session, status_url, device_ip)  # Get device Status
    time.sleep(9)

    print("\nTurning ON All Relays:\n")
    for i in range(4):
        numato_relay_control(session, control_url, i, 1)        # Turning ON All Relays
    print("\n")
    numato_fetch_device_status(session, status_url, device_ip)  # Get device Status
    time.sleep(3)
  
def main():
    numato_control_device(device_ip)

if __name__ == "__main__":
    main()
