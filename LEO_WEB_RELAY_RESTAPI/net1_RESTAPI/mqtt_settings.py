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
#   Demonstrates Net1 RESTAPI MQTT management.
#
# ============================================================================
import requests
import json

# ============================================================
# Current Configuration
# ============================================================

device_ip = "10.10.10.203"   # your device IP

current_username = "admin"           # your device Username
current_password_web = "admin1234"   # your device Password

# ============================================================
# API URLs
# ============================================================

login_url = "http://" + device_ip + "/login"

api_mqtt_settings_url = ( "http://" + device_ip + "/api/v0/mqtt/0/settings" )


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


def get_mqtt_settings(session):

    print("\n========== CURRENT MQTT SETTINGS ==========")

    response = session.get(api_mqtt_settings_url)

    if response.status_code != 200:

        print("Failed to get MQTT settings")
        print(response.text)

        return None

    data = response.json()

    print("Broker URL       :", data.get("brokerurl"))
    print("Publish Interval :", data.get("pubinterval"))
    print("Username         :", data.get("user"))
    print("Client ID        :", data.get("clientid"))

    print(
        "Client Certificate:",
        data.get("clientcertfname")
    )

    print(
        "Client Key       :",
        data.get("clientkeyfname")
    )

    print(
        "CA Certificate   :",
        data.get("cacertfname")
    )

    topics = data.get("topics", [])

    if topics:

        topic = topics[0]

        print("\nMQTT Topic:")
        print("Topic    :", topic.get("topic"))
        print("Message  :", topic.get("msg"))
        print("Subtopic :", topic.get("subtopic"))

    return data


# =========================================================================
# MQTT configuration to apply - Update with the settings of your choice.
# =========================================================================
def update_mqtt_settings(session):

    print("\n========== UPDATING MQTT SETTINGS ==========")

    data = {
        "mqbrokerurl": "mqtt://test.mosquitto.org",
        "mqpubivl": "1000",

        "mquser": "mqtt_user",
        "mqpass": "mqtt_password",

        "mqclientid": "LEOWR8-Mqtt",

        "mqtopic": "numato/device",
        "mqmsgfmt": "{Relay:~rl_val~,Digital Input:~din_val~}",

        "mqsubtopic": "numato/device/control"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = session.post(
        api_mqtt_settings_url,
        json=data,
        headers=headers
    )

    if response.status_code == 200:

        print(json.dumps(data, indent=4))

        print("MQTT settings updated successfully!")
        print(
            "Reboot the device to save the updated MQTT settings."
        )

        return True

    print("Failed to update MQTT settings")
    print(response.text)

    return False

# ============================================================
# Main
# ============================================================
def main():

    print("Numato Lab Net1 REST API - MQTT Settings Sample")
    print("------------------------------------------------")
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
        # Read current settings
        # ----------------------------------------------------
        get_mqtt_settings(session)

        # ----------------------------------------------------
        # Update MQTT settings
        # ----------------------------------------------------
        update_mqtt_settings(session)

    except requests.RequestException as exc:

        #print()
        print("Invalid Device IP or URL")
        #print(exc)

    except Exception as exc:

        print("Operation failed.")
        #print(exc)


if __name__ == "__main__":
    main()
