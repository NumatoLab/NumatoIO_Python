# ============================================================================
# Numato Lab LEO Web series Sample Script
#
# Copyright (c) 2026 Numato Lab
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Description:
#   Demonstrates Net1 RESTAPI network management.
#
# ============================================================================
import requests
import json

# ============================================================
# Current Configuration
# ============================================================

device_ip = "10.10.10.203"  # your device IP

current_username = "admin"          # your device Username
current_password_web = "admin1234"  # your device Password


# ============================================================
# API URLs
# ============================================================

login_url = "http://" + device_ip + "/login"

api_settings_url = ( "http://" + device_ip + "/api/v0/wifi/0/settings" )


def maestro_mfg_login_to_web_console(
        session,
        login_url,
        username,
        password):

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
    }

    form_data = {
        "user": current_username,
        "pass": current_password_web
    }

    response = session.post(
        login_url,
        data=form_data,
        headers=headers
    )
    
    if response.status_code == 200 and response.url.endswith("/index.html"):
        print("Logged in successfully!")
        return True

    print("Login failed ")
    return False

def get_network_settings(session):



    response = session.get(api_settings_url)

    print("\n========== CURRENT NETWORK SETTINGS ==========")

    data = response.json()

    print("SSID       :", data.get("ssid"))
    print("MAC        :", data.get("mac"))
    print("Hostname   :", data.get("hostname"))
    print("DHCP       :", data.get("dhcp"))
    print("IPv4       :", data.get("ipv4"))
    print("Subnet Mask:", data.get("subnetmask"))
    print("Gateway    :", data.get("defgateway"))
    print("Primary DNS:", data.get("dnsprim"))

# ====================================================================
# Network configuration to apply - configure new settings of your choice
# ====================================================================

def update_network_settings(session):

    print("\n========== UPDATING NETWORK SETTINGS ==========")

    data = {
        "ssid": "myssid",
        "password": "mypassword123",
        "hostname": "LEOWR8A-1234",
        "dhcp": "0",
        "ipv4": "192.168.1.100",
        "subnetmask": "255.255.255.0",
        "defgateway": "192.168.1.1",
        "dnsprim": "8.8.8.8"
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Sending network settings:")
    print(json.dumps(data, indent=4))

    response = session.post(
        api_settings_url,
        json=data,
        headers=headers
    )

    if response.status_code == 200:
        print("Network settings updated successfully!")
        print(
            "Reboot the device to save the updated network settings."
        )
        

# ============================================================
# Main
# ============================================================
def main():
    
    print("Numato Lab Net1 REST API - Network Settings Sample")
    print("---------------------------------------------------")
    print(f"Device: {device_ip}")
    print()

    print(
        "WARNING: Changing network settings may disconnect "
        "the device."
    )
    print()

    session = requests.Session()
    try:
        # ----------------------------------------------------
        # Login
        # ----------------------------------------------------
        if not maestro_mfg_login_to_web_console(
            session,
            login_url,
            current_username,
            current_password_web
        ):
            return

        # ----------------------------------------------------
        # Read current settings
        # ----------------------------------------------------
        get_network_settings(session)

        # ----------------------------------------------------
        # Update settings
        # ----------------------------------------------------
        
        update_network_settings(session)
        
    except requests.RequestException as exc:

        #print()
        print("Invalid Device IP or URL.")
        #print(exc)

    except Exception as exc:

        print()
        print("Operation failed.")
        #print(exc)


if __name__ == "__main__":
    main()
