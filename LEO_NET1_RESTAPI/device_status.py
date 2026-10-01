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
#   Demonstrates authentication and device information management using the
#   Numato Lab REST API.
#
# ============================================================================

import requests


# Device and login details
device_ip = "10.10.10.203"

login_url = "http://" + device_ip + "/login"

username = "admin"
password_web = "admin1234"


# APIs
api_status_url = "http://" + device_ip + "/api/v0/status"
api_device_info_url = "http://" + device_ip + "/api/v0/deviceinfo"


def maestro_mfg_login_to_web_console(session, login_url, username, password):

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

    print(f"Attempting to log in to {login_url}")

    response = session.post(
        login_url,
        data=form_data,
        headers=headers
    )

    if response.status_code == 200:
        print("Logged in successfully!")
        return True

    print("Login failed")
    print("Status code:", response.status_code)
    print("Response:", response.text)

    return False


def get_device_status(session):

    print("\n========== DEVICE STATUS ==========")

    response = session.get(api_status_url)

    print("Status code:", response.status_code)

    if response.status_code == 200:

        try:
            data = response.json()

            print("\nDevice Status:")
            print(data)

            return data

        except ValueError:
            print("Invalid JSON response")
            print(response.text)

    else:
        print("Failed to get device status")
        print(response.text)

    return None


def get_device_info(session):

    print("\n========== DEVICE INFORMATION ==========")

    response = session.get(api_device_info_url)

    print("Status code:", response.status_code)

    if response.status_code == 200:

        try:
            data = response.json()

            print("Device ID      :", data.get("device_id"))
            print("Product Serial :", data.get("prod_serial"))
            print("DS FW Version  :", data.get("ds_fw_ver"))
            print("NET1 FW Version:", data.get("net1_fw_ver"))

            return data

        except ValueError:
            print("Invalid JSON response")
            print(response.text)

    else:
        print("Failed to get device information")
        print(response.text)

    return None


def main():

    session = requests.Session()

    if not maestro_mfg_login_to_web_console(
        session,
        login_url,
        username,
        password_web
    ):
        return

    get_device_info(session)
    get_device_status(session)


if __name__ == "__main__":
    main()