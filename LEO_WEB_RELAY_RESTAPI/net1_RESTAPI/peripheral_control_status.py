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
#   Demonstrates Net1 RESTAPI Relay and Digital Input Control and monitor.
#
# ============================================================================
import requests
import time

# ============================================================
# Current Configuration
# ============================================================

device_ip = "10.10.10.203"    # your device IP

current_username = "admin"            # your device Username
current_password_web = "admin1234"    # your device Password


# ============================================================
# API URLs
# ============================================================

login_url = "http://" + device_ip + "/login"

device_status_url = ("http://" + device_ip + "/api/v0/status" )

relay_control_url = ("http://" + device_ip + "/api/v0/relay/control" )


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


def get_peripheral_status(session):


    response = session.get(device_status_url)

    
    print("\n========== PERIPHERAL STATUS ==========")

    if response.status_code != 200:
        print("Failed to get peripheral status")
        #print(response.text)
        return None

    
    response_data = response.json()

    data = response_data.get("data", {})

    # ----------------------------------------------------------
    # Relay status
    # ----------------------------------------------------------

    relays = data.get("relays", [])

    print("\n--- RELAYS ---")

    for relay in relays:

        relay_index = relay.get("index")
        relay_state = relay.get("rl_state")
        print(
            f"Relay {relay_index}: "
            f"{'ON' if relay_state == "1" else 'OFF'}"
        )

    # ----------------------------------------------------------
    # Digital Input status
    # ----------------------------------------------------------

    gpis = data.get("gpis", [])

    print("\n--- DIGITAL INPUTS ---")

    for index, gpi in enumerate(gpis):

        value = gpi.get("value")

        print(
            f"Digital Input {index}: "
            f"{'HIGH' if value == 1 else 'LOW'}"
        )



def relay_control(
        session,
        relay_num,
        relay_state):

    data = {
        "relay_num": relay_num,
        "relay_state": relay_state
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(
        f"\nSetting Relay {relay_num} "
        f"to {'ON' if relay_state else 'OFF'}"
    )

    response = session.post(
        relay_control_url,
        json=data,
        headers=headers
    )

    if response.status_code == 200:

        print("Relay control command successful")


        return True

    print("Relay control failed")
    #print(response.text)

    return False

# ============================================================
# Main
# ============================================================

def main():

    print("Numato Lab Net1 REST API - Relay Control & Status Sample")
    print("----------------------------------------------------------")
    print(f"Device: {device_ip}")
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

        # ----------------------------------------------------------
        # Read status
        # ----------------------------------------------------------

        get_peripheral_status(session)

        # ----------------------------------------------------------
        # Relay control example
        # ----------------------------------------------------------
        print("\n========== RELAY CONTROL ==========")

        # Relay 2 ON
        relay_control(session, 2, 1)

        time.sleep(1)

        # Read actual state after command
        get_peripheral_status(session)

        time.sleep(1)
        print("\n========== RELAY CONTROL ==========")
        # Relay 2 OFF
        relay_control(session, 2, 0)

        time.sleep(1)
        
        # Read actual state again 
        get_peripheral_status(session)
        
    except requests.RequestException as exc:

        #print()
        print("Invalid Device IP and URL.")
        #print(exc)

    except Exception as exc:

        #print()
        print("Operation failed.")
        #print(exc)


if __name__ == "__main__":
    main()
