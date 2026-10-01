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
#   Demonstrates reading and updating network configuration using the
#   Numato Lab REST API.
#
#   WARNING:
#   Changing the network configuration can disconnect the device.
#
# ============================================================================

import json
import requests


# ============================================================
# Configuration
# ============================================================

DEVICE_IP = "10.10.10.82"  # your device IP
USERNAME = "admin"
PASSWORD = "admin1234"


# ============================================================
# Network configuration to apply
# ============================================================

NEW_HOSTNAME = "Leo-Wr8"

DHCP_ENABLED = 1

STATIC_IP = "10.10.10.82"
SUBNET_MASK = "255.255.255.0"
GATEWAY = "10.10.10.1"


# ============================================================
# API URLs
# ============================================================

BASE_URL = f"http://{DEVICE_IP}"

LOGIN_URL = f"{BASE_URL}/auth.cgi"
NETWORK_URL = f"{BASE_URL}/api/v0/network/0/settings"


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


def get_network_settings(session):
    """Get the current network configuration."""

    response = session.get(
        NETWORK_URL,
        timeout=5,
    )

    response.raise_for_status()

    print("=== NETWORK SETTINGS ===")
    print_json(response)
    print()

    return response.json()


def update_network_settings(
    session,
    hostname,
    dhcp,
    ip,
    subnet,
    gateway,
):
    """Update network configuration."""

    payload = {
        "hostname": hostname,
        "dhcp": dhcp,
        "ip": ip,
        "subnet": subnet,
        "gateway": gateway,
    }

    print("=== UPDATE NETWORK SETTINGS ===")
    print(
        json.dumps(
            payload,
            indent=4
        )
    )
    print()

    response = session.post(
        NETWORK_URL,
        json=payload,
        timeout=5,
    )

    response.raise_for_status()

    print_json(response)
    print()


# ============================================================
# Main
# ============================================================

def main():

    print("Numato PIC REST API - Network Settings Example")
    print("----------------------------------------------")
    print(f"Device: {DEVICE_IP}")
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
        login(session)

        # ----------------------------------------------------
        # Read current settings
        # ----------------------------------------------------
        get_network_settings(session)

        # ----------------------------------------------------
        # Update settings
        # ----------------------------------------------------
        update_network_settings(
            session,
            hostname=NEW_HOSTNAME,
            dhcp=DHCP_ENABLED,
            ip=STATIC_IP,
            subnet=SUBNET_MASK,
            gateway=GATEWAY,
        )

        print(
            "Network configuration updated."
        )

        print(
            "The response indicates whether a restart is required."
        )

    except requests.RequestException as exc:

        print()
        print("HTTP communication error:")
        print(exc)

    except Exception as exc:

        print()
        print("Operation failed:")
        print(exc)


if __name__ == "__main__":
    main()
