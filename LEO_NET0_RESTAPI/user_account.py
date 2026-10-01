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
#   Demonstrates user account management using the Numato Lab REST API.
#
# ============================================================================

import json
import requests


# ============================================================
# Configuration
# ============================================================

DEVICE_IP = "10.10.10.204"  # your device IP
USERNAME = "admin"
PASSWORD = "Admin1234"

NEW_USERNAME = "admin"
NEW_PASSWORD = "admin1234"


# ============================================================
# API URLs
# ============================================================

BASE_URL = f"http://{DEVICE_IP}"

LOGIN_URL = f"{BASE_URL}/auth.cgi"
USER_URL = f"{BASE_URL}/api/v0/useraccount"


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


def get_user_account(session):
    """Get the configured username."""

    response = session.get(
        USER_URL,
        timeout=5,
    )

    response.raise_for_status()

    print("=== USER ACCOUNT ===")
    print_json(response)
    print()

    return response.json()


def update_user_account(
    session,
    username,
    password,
):
    """Update username and password."""

    if not 1 <= len(username) <= 8:
        raise ValueError(
            "Username must contain 1 to 8 characters."
        )

    if not 9 <= len(password) <= 31:
        raise ValueError(
            "Password must contain 9 to 31 characters."
        )

    print(
        f"=== UPDATE USER ACCOUNT -> {username} ==="
    )

    response = session.post(
        USER_URL,
        json={
            "username": username,
            "password": password,
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

    print("Numato PIC REST API - User Account Example")
    print("------------------------------------------")
    print(f"Device: {DEVICE_IP}")
    print()

    session = requests.Session()

    try:

        # ----------------------------------------------------
        # Login
        # ----------------------------------------------------
        login(session)

        # ----------------------------------------------------
        # Read current username
        # ----------------------------------------------------
        get_user_account(session)

        # ----------------------------------------------------
        # Update credentials
        # ----------------------------------------------------
        update_user_account(
            session,
            NEW_USERNAME,
            NEW_PASSWORD
        )

        print(
            "User account updated successfully."
        )

        print(
            "Create a new session and log in again using "
            "the new credentials to verify the change."
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
