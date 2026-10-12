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
#   Demonstrates Net0 RESTAPI Network management.
#
# ============================================================================
import json
import requests


# ============================================================
# Current Configuration
# ============================================================

DEVICE_IP = "10.10.10.204"  # your device IP
CURRENT_USERNAME = "admin"          # your device Username
CURRENT_PASSWORD = "admin1234"      # your device Password


# ============================================================
# Network configuration to apply
# ============================================================

NEW_HOSTNAME = "Leo-Wr8-net0" # New Hostname you want to update

NEW_DHCP_STATUS = 0              # DHCP status you want

NEW_STATIC_IP = "10.10.10.77"     # New Static IP you want to update
NEW_SUBNET_MASK = "255.255.255.0" # New Subnet Mask you want to update
NEW_GATEWAY = "10.10.10.1"        # New Gateway you want to update


# ============================================================
# API URLs
# ============================================================

BASE_URL = f"http://{DEVICE_IP}"

LOGIN_URL = f"{BASE_URL}/auth.cgi"
NETWORK_SETTINGS_URL = f"{BASE_URL}/api/v0/network/0/settings"


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
            "user": CURRENT_USERNAME,
            "pass": CURRENT_PASSWORD,
        },
        timeout=5,
        allow_redirects=False,
        stream=True,
    )
    sid = session.cookies.get("SID")

    response.close()

    if not sid:
        raise RuntimeError(
            "Login failed: SID cookie was not received."
        )

    print("Logged in successfully.")
    print()


def get_network_settings(session):
    """Get the current network configuration."""

    response = session.get(
        NETWORK_SETTINGS_URL,
        timeout=5,
    )

    response.raise_for_status()

    print("=== CURRENT NETWORK SETTINGS ===")
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

    print("=== UPDATING THE NETWORK SETTINGS ===")
    print(
        json.dumps(
            payload,
            indent=5
        )
    )
    print()

    response = session.post(
        NETWORK_SETTINGS_URL,
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

    print("Numato Lab Net0 REST API - Network Settings Sample")
    print("---------------------------------------------------")
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
            dhcp=NEW_DHCP_STATUS,
            ip=NEW_STATIC_IP,
            subnet=NEW_SUBNET_MASK,
            gateway=NEW_GATEWAY,
        )

        print(
            "Network configuration updated."
        )

        print(
            "The response indicates whether a restart is required."
        )

    except requests.RequestException as exc:

        print()
        print("Invalid BASE_URL")
        #print(exc)

    except Exception as exc:

        print()
        print("Operation failed")
        #print(exc)


if __name__ == "__main__":
    main()
