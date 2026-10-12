# ============================================================================
# Numato Lab LEO USB series Sample Script
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
#   Demonstrates authentication and device information management.
#
# ============================================================================
import serial
import time

# ============================================================
# SERIAL PORT Configuration
# ============================================================

PORT = "COM56"   # your device COM Port
TIMEOUT = 1
BAUDRATE = 9600

# ============================================================
# Current Credentials
# ============================================================

CURRENT_USERNAME = "admin"      # your device Username
CURRENT_PASSWORD = "admin1234"  # your device Password


def send(ser_port,command):

    ser_port.write(f"{command}\r".encode())
    time.sleep(0.5)

    response = ser_port.read(300).decode().strip().splitlines()

    return response

def send_login(ser_port,COMMAND):
    ser_port.write(f"{COMMAND}\r".encode())
    time.sleep(0.5)
    response_login = ser_port.read(300).decode().strip()

    return response_login
    

def authentication(ser_port):
    
    Username = CURRENT_USERNAME   
    Password = CURRENT_PASSWORD

    response_login = send_login(ser_port,"")
    time.sleep(0.5)
   

    if "User Name :" in response_login:
        response_login = send_login(ser_port,Username)
        if "Please Try Again." in response_login:
            print("Username is incorrect. Check credentials.")
            ser_port.close()
            return False

    if "Password  :" in response_login:
        response_login = send_login(ser_port,Password)
        if "Please Try Again." in response_login:
            print("Password is incorrect. Check credentials.")
            ser_port.close()
            return False

    if "Logged in successfully" in response_login:
        print("========== Logged in Successfully =============\n")
        return True
    else:
        print("========== Already Logged In ==================\n")

# =======================================
# Function to get the version of the module
# =======================================    
def ver(ser_port):

    response = send(ser_port,"ver")
    print("=====Device Version======")
    print(f"VERSION:   {response[1]}\n")


# ======================================
# Function to read the info of the module
# ======================================
def info(ser_port):

    response = send(ser_port,"info")
    print("=====Device Information=====")
    for resp in response[1:-1]:
        print(f"{resp}")

# =============================================
# Functions to read current Device ID.
# And also to set New Device ID.
# =============================================
def id(ser_port):

    # Get the current ID
    response = send(ser_port,"id get")
    print("======Current Device ID======")
    print(f"ID:   {response[1]}\n")

    # Set the new ID value
    ID = "00000000"       # your New Device ID


    response = send(ser_port,f"id set {ID}")
    if "ERR: -2" in response:
        print("Invalid input for ID\n")
    else:
        print("======Updated Device ID======")
        response = send(ser_port,"id get")
        print(f"ID:   {response[1]}\n")
            
    

# =============================================
# Functions to read current Device Username.
# And also to set New Device Username.
# =============================================
def usr(ser_port):

    # Get the current username
    response = send(ser_port,"usr get")
    print("======Current Device Username=====")
    print(f"Username:  {response[1]}\n")

    # Set the new username
    USR = "Admin"        # your New Device Username

    
    response = send(ser_port,f"usr set {USR}")
    if "ERR: -2" in response:
        print("Invalid input for username\n")
    else:
        print("=====Updated Device Username=====")
        response = send(ser_port,"usr get")
        print(f"Username:  {response[1]}\n")
    


# =============================================
# Functions to read current Device Password.
# And also to set New Device Password.
# =============================================
def password(ser_port):

    # Get the current password
    response = send(ser_port, "pass get")
    print("=====Current Device Password======")
    print(f"Password:   {response[1]}\n")

    # Set the new password
    PASS = "Admin1234"      # your New Device Password

    
    response = send(ser_port, f"pass set {PASS}")
    if "ERR: -2" in response:
        print("Invalid input for password\n")
    else:
        print("=====Updated Device Password======")
        response = send(ser_port,"pass get")
        print(f"Password:   {response[1]}\n")

    

# =============================================
# Main
# =============================================
def main():

    print("Numato Lab LEOCR8 - Configuration Sample")
    print("-----------------------------------------")
    print(f"Device COM Port: {PORT}")
    print()
    try:
        # ============================
        # Open COM Port
        # ============================
        ser_port = serial.Serial(port = PORT,baudrate=BAUDRATE,timeout=TIMEOUT)
        
        try:
            # =====================
            # Login
            # =====================
            if authentication(ser_port) is False:
                raise Exception
            
            # =====================
            # Get Device Version
            # =====================
            ver(ser_port)

            # =====================
            # Get Device INFO
            # =====================

            info(ser_port)

            # ===========================
            # GeT Device ID and Update ID
            # ===========================

            id(ser_port)

            # ============================================
            # Get Current Username and Update New Username
            # ============================================
            usr(ser_port)

            # ============================================
            # Get Current Password and Update New Password
            # ============================================
            password(ser_port)

            print("New username and password have been set. Power-cycle the device and log in using the updated credentials.\n")


        except Exception as e:
            pass

        finally:
            ser_port.close()
    except:
        print("PORT Not available - Check PORT Number or Device Connection")


main()
