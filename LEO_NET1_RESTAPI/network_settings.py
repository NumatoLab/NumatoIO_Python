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
# ============================================================================

import requests


# Device and login details
device_ip = "10.10.10.203"

login_url = "http://" + device_ip + "/login"

username = "admin"
password_web = "admin1234"


# API
api_settings_url = (
    "http://" +
    device_ip +
    "/api/v0/wifi/0/settings"
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


def get_network_settings(session):

    print("\n========== NETWORK SETTINGS ==========")

    response = session.get(api_settings_url)

    print("Status code:", response.status_code)

    if response.status_code == 200:

        try:
            data = response.json()

            print("SSID       :", data.get("ssid"))
            print("MAC        :", data.get("mac"))
            print("Hostname   :", data.get("hostname"))
            print("DHCP       :", data.get("dhcp"))
            print("IPv4       :", data.get("ipv4"))
            print("Subnet Mask:", data.get("subnetmask"))
            print("Gateway    :", data.get("defgateway"))
            print("Primary DNS:", data.get("dnsprim"))

            return data

        except ValueError:
            print("Invalid JSON response")
            print(response.text)

    else:
        print("Failed to get network settings")
        print(response.text)

    return None


def update_network_settings(session):

    print("\n========== UPDATE NETWORK SETTINGS ==========")

    data = {
        "ssid": "myssid",
        "password": "mypassword123",
        "hostname": "LEOWR8A-1234",

        # DHCP
        "dhcp": "1",

        # These are still sent according to the backend API
        "ipv4": "192.168.1.100",
        "subnetmask": "255.255.255.0",
        "defgateway": "192.168.1.1",
        "dnsprim": "8.8.8.8"
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Sending network settings:")
    print(data)

    response = session.post(
        api_settings_url,
        json=data,
        headers=headers
    )

    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Network settings updated successfully!")

        try:
            print("Response:", response.json())
        except ValueError:
            print("Response:", response.text)

        return True

    print("Failed to update network settings")
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
    get_network_settings(session)

    # POST
    # Uncomment when you actually want to change settings.
    #
    #update_network_settings(session)


if __name__ == "__main__":
    main()