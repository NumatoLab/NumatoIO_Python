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
# ============================================================================

import requests


# Device and login details
device_ip = "10.10.10.203"

login_url = "http://" + device_ip + "/login"

username = "admin"
password_web = "admin1234"


# API
api_user_url = (
    "http://" +
    device_ip +
    "/api/v0/useraccount"
)


def maestro_mfg_login_to_web_console(
        session,
        login_url,
        username,
        password):

    form_data = {
        "user": username,
        "pass": password
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

    if response.status_code == 200:
        print("Logged in successfully!")
        return True

    print("Login failed")
    return False


def get_user_account(session):

    print("\n========== USER ACCOUNT ==========")

    response = session.get(api_user_url)

    print("Status code:", response.status_code)

    if response.status_code == 200:

        try:
            data = response.json()

            print("Username:", data.get("user"))
            return data

        except ValueError:
            print("Invalid JSON response")
            print(response.text)

    else:
        print("Failed to get user account")
        print(response.text)

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
        api_user_url,
        json=data,
        headers=headers
    )

    print("Status code:", response.status_code)

    if response.status_code == 200:

        print("User account updated successfully!")

        try:
            print("Response:", response.json())
        except ValueError:
            print("Response:", response.text)

        return True

    print("Failed to update user account")
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

    # GET
    get_user_account(session)

    # POST - keep disabled unless required
    #
    #update_user_account(
    #     session,
    #     "admin",
    #     "admin1234"
    #)


if __name__ == "__main__":
    main()