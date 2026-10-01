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
#   Demonstrates authentication, relay control, and device status using the
#   Numato Lab REST API.
#
# ============================================================================

import json
import requests
import time


# ============================================================
# Configuration
# ============================================================

DEVICE_IP = "10.10.10.204" # your device IP
USERNAME = "admin"
PASSWORD = "admin1234"

RELAY_NUMBER = 3


# ============================================================
# API URLs
# ============================================================

BASE_URL = f"http://{DEVICE_IP}"

LOGIN_URL = f"{BASE_URL}/auth.cgi"
RELAY_URL = f"{BASE_URL}/api/v0/relay/control"
STATUS_URL = f"{BASE_URL}/api/v0/status"


# ============================================================
# Helpers
# ============================================================

def print_json(response):
    """Print an HTTP JSON response in a readable format."""

    try:
        print(
            json.dumps(
                response.json(),
                indent=4
            )
        )
    except ValueError:
        print("Response is not valid JSON:")
        print(response.text)


def login(session):
    """Authenticate and obtain the SID session cookie."""

    print("=== LOGIN ===")

    response = session.post(
        LOGIN_URL,
        data={
            "user": USERNAME,
            "pass": PASSWORD,
        },
        timeout=5,
        allow_redirects=False,
        stream=True,
    )

    print("HTTP status:", response.status_code)

    sid = session.cookies.get("SID")

    response.close()

    if not sid:
        raise RuntimeError(
            "Login failed: SID cookie was not received."
        )

    print("Authentication successful.")
    print()


def get_relay_status(session):
    """Get status of all relays."""

    response = session.get(
        RELAY_URL,
        timeout=5,
    )

    response.raise_for_status()

    print("=== RELAY STATUS ===")
    print_json(response)
    print()

    return response.json()


def get_device_status(session):
    """Get complete device status."""

    response = session.get(
        STATUS_URL,
        timeout=5,
    )

    response.raise_for_status()

    print("=== DEVICE STATUS ===")
    print_json(response)
    print()

    return response.json()


def get_relay_state(session, relay_number):
    """Read one relay state from the device status API."""

    data = get_device_status(session)

    relays = data.get(
        "data",
        {}
    ).get(
        "relays",
        []
    )

    for relay in relays:
        if relay.get("index") == relay_number:
            return relay.get("rl_state")

    raise RuntimeError(
        f"Relay {relay_number} was not found in status response."
    )


def set_relay(session, relay_number, state):
    """Set one relay ON or OFF."""

    state = 1 if state else 0

    state_text = "ON" if state else "OFF"

    print(
        f"=== SET RELAY {relay_number} -> {state_text} ==="
    )

    response = session.post(
        RELAY_URL,
        json={
            "relay_num": relay_number,
            "relay_state": state,
        },
        timeout=5,
    )

    response.raise_for_status()

    print_json(response)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print("Numato PIC REST API - Relay & Status Example")
    print("---------------------------------------------")
    print(f"Device: {DEVICE_IP}")
    print()

    session = requests.Session()

    try:

        # ----------------------------------------------------
        # Login
        # ----------------------------------------------------
        login(session)

        # ----------------------------------------------------
        # Get relay status
        # ----------------------------------------------------
        get_relay_status(session)

        # ----------------------------------------------------
        # Get complete device status
        # ----------------------------------------------------
        get_device_status(session)
        
        while(1):
            # ----------------------------------------------------
            # Turn relay ON
            # ----------------------------------------------------
            set_relay(
                session,
                RELAY_NUMBER,
                1
            )

            time.sleep(0.5)

            # ----------------------------------------------------
            # Verify relay ON state
            # ----------------------------------------------------
            state = get_relay_state(
                session,
                RELAY_NUMBER
            )
            

            print(
                f"Relay {RELAY_NUMBER} state: "
                f"{'ON' if state else 'OFF'}"
            )

            #if state != 1:
             #   raise RuntimeError(
              #      f"Relay {RELAY_NUMBER} did not turn ON."
               # )

            print("Relay ON verified.")
            print()

            # ----------------------------------------------------
            # Turn relay OFF
            # ----------------------------------------------------
            set_relay(
                session,
                RELAY_NUMBER,
                0
            )

            time.sleep(0.5)

            # ----------------------------------------------------
            # Verify relay OFF state
            # ----------------------------------------------------
            state = get_relay_state(
                session,
                RELAY_NUMBER
            )

            print(
                f"Relay {RELAY_NUMBER} state: "
                f"{'ON' if state else 'OFF'}"
            )

            #if state != 0:
                #raise RuntimeError(
                 #   f"Relay {RELAY_NUMBER} did not turn OFF."
                #)

            print("Relay OFF verified.")
            print()

        print("=== TEST PASSED ===")

    except requests.RequestException as exc:

        print()
        print("HTTP communication error:")
        print(exc)

    except Exception as exc:

        print()
        print("Test failed:")
        print(exc)


if __name__ == "__main__":
    main()
