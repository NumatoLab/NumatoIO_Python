# ============================================================================
# Numato Lab LEO Web series Net0 REST API Example
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
#   Demonstrates relay control, and device status using the
#   Numato Lab REST API.
#
# ============================================================================

import requests
import time


# Device and login details
device_ip = "10.10.10.203"

login_url = "http://" + device_ip + "/login"

username = "admin"
password_web = "admin1234"

# APIs
api_status_url = (
    "http://" +
    device_ip +
    "/api/v0/status"
)

api_relay_control_url = (
    "http://" +
    device_ip +
    "/api/v0/relay/control"
)


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
        "user": username,
        "pass": password
    }

    response = session.post(
        login_url,
        data=form_data,
        headers=headers
    )

    if response.status_code == 200:
        print("Logged in successfully!")
        return True

    print("Login failed")
    print(response.status_code)
    print(response.text)

    return False


def get_peripheral_status(session):

    print("\n========== PERIPHERAL STATUS ==========")

    response = session.get(api_status_url)

    print("Status code:", response.status_code)

    if response.status_code != 200:
        print("Failed to get peripheral status")
        print(response.text)
        return None

    try:
        response_data = response.json()

    except ValueError:
        print("Invalid JSON response")
        print(response.text)
        return None

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
        api_relay_control_url,
        json=data,
        headers=headers
    )

    print("Status code:", response.status_code)

    if response.status_code == 200:

        print("Relay control command successful")

        try:
            print("Response:", response.json())
        except ValueError:
            print("Response:", response.text)

        return True

    print("Relay control failed")
    print(response.text)

    return False


def main():

    session = requests.Session()

    if not maestro_mfg_login_to_web_console(
        session,
        login_url,
        username,
        password_web
    ):
        return

    # ----------------------------------------------------------
    # Read status
    # ----------------------------------------------------------

    get_peripheral_status(session)

    # ----------------------------------------------------------
    # Relay control example
    # ----------------------------------------------------------

    # Relay 2 ON
    relay_control(session, 2, 1)

    time.sleep(1)

    # Read actual state after command
    get_peripheral_status(session)

    time.sleep(1)

    # Relay 2 OFF
    relay_control(session, 2, 0)

    time.sleep(1)

    # Read actual state again
    get_peripheral_status(session)


if __name__ == "__main__":
    main()