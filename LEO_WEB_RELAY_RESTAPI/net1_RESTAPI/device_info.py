import requests
import json

# ============================================================
# Current Configuration
# ============================================================

device_ip = "10.10.10.203"  # your device IP

current_username = "admin"          # your device Username
current_password_web = "admin1234"  # your device Password

NEW_DEVICE_ID = "00000001"          # your New Device ID

# ============================================================
# API URLs
# ============================================================

login_url = "http://" + device_ip + "/login"

device_info_url = "http://" + device_ip + "/api/v0/deviceinfo"



def maestro_mfg_login_to_web_console(session, login_url, username, password):

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
    }

    form_data = {
        "user": current_username,
        "pass": current_password_web
    }

    print(f"Attempting to log in to {login_url}")

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



def get_device_info(session):

    response = session.get(device_info_url)

    data = response.json()
            
    print("\n========== DEVICE INFORMATION ==========")

    print("Device ID      :", data.get("device_id"))
    print("Product Serial :", data.get("prod_serial"))
    print("DS FW Version  :", data.get("ds_fw_ver"))
    print("NET1 FW Version:", data.get("net1_fw_ver"))

    return data

def set_device_id(session, device_id):
    """Update the device ID."""

    if len(device_id) != 8:
        raise ValueError(
            "Device ID must contain exactly 8 characters."
        )

    print('\n')
    print(
        f"=== SET DEVICE ID -> {device_id} ==="
    )

    response = session.post(
        device_info_url,
        json={
            "device_id": device_id,
        },
        timeout=5,
    )



# ============================================================
# Main
# ============================================================

def main():

    
    print("Numato Lab Net1 REST API - Device Information Sample")
    print("------------------------------------------------------")
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
        # Read device information
        # ----------------------------------------------------
        get_device_info(session)


# ===================================================================================================
# UnComment the below set_device_id function and get_device_info if you want to update your device ID
# ===================================================================================================
        # ----------------------------------------------------
        # Update device ID
        # ----------------------------------------------------
        set_device_id(
           session,
         NEW_DEVICE_ID
        )

        # ----------------------------------------------------
        # Read device information again
        # ----------------------------------------------------
        print("Verifying device ID...")
        get_device_info(session)
        print('\n')

        print("=== TEST PASSED ===")
        

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
