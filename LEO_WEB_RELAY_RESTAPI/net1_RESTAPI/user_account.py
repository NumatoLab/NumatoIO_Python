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
#   Demonstrates Net1 RESTAPI User authentication management.
#
# ============================================================================
import requests

# ============================================================
# Current Configuration
# ============================================================

device_ip = "10.10.10.203"          # your device IP

current_username = "admin"          # your device Username
current_password_web = "admin1234"  # your devie Password

# ============================================================
# API URLs
# ============================================================

login_url = "http://" + device_ip + "/login"

user_account_url = ("http://" + device_ip + "/api/v0/useraccount")


def maestro_mfg_login_to_web_console(
        session,
        login_url,
        username,
        password):

    form_data = {
        "user": current_username,
        "pass": current_password_web
    }

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
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


def get_user_account(session):

    print("\n========== USER ACCOUNT ==========")

    response = session.get(user_account_url)


    if response.status_code == 200:

            data = response.json()

            print("Username:", data.get("user"))
            return data


    else:
        print("Failed to get user account")
        #print(response.text)

    return None


def update_user_account(
        session,
        new_username,
        new_password):

    print("\n========== UPDATE USER ACCOUNT ==========")

    data = {
        "username": new_username,
        "password": new_password,
        "confirmPassword": new_password
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = session.post(
        user_account_url,
        json=data,
        headers=headers
    )

    if response.status_code == 200:

        print("User account updated successfully!")
        
        print(
           "Reboot the device and log in using "
          "the new credentials to verify the change."
         )

        return True

    print("Failed to update user account")
    print(response.text)

    return False


# ============================================================
# Main
# ============================================================

def main():

    print("Numato Lab Net1 REST API - User Account Sample")
    print("-----------------------------------------------")
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

        # ----------------------------------------------------
        # Read current username
        # ----------------------------------------------------
        get_user_account(session)


        # ========================================================================================
        # UnComment the below update_user_account function with new username and password
        # of your choice if you want to update your device credentials.
        # ========================================================================================

        
        #update_user_account(
        #   session,
        #   "admin",
        #   "admin1234" )
    except requests.RequestException as exc:

        #print()
        print("Invalid Device IP.")
        #print(exc)

    except Exception as exc:

        print()
        print("Operation failed.")
        #print(exc)


if __name__ == "__main__":
    main()
