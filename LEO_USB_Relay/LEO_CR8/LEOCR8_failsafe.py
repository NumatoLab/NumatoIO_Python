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
#   Demonstrates IO Failsafe operation.
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


# ==================================
# Function for Enabling Failsafe mode
# ==================================
def failsafe_enable(ser_port):

    # ==============================
    # Enter the "MODE" for timer
    # L ➞ LOW |  H ➞  HIGH 
    # ==============================
    MODE = "Ln"     # enter your mode

    # ================================================
    # Enter the hexadecimal value to turn ON/OFF
    # one or more relays when failsafe is triggered.
    # ================================================
    RELAY = "00AA"    # enter input (0000 - 00FF)
    
    response = send(ser_port,f"fs 000 {MODE} A {RELAY}")

    if MODE == "":
        print("Enter DI 000 Mode (L/H)\n")
    elif MODE not in ["L", "H"]:
        print("Enter Valid MODE\n")
    elif not (len(RELAY) == 4 and RELAY[:2] == "00" and all(c in "0123456789ABCDEFabcdef" for c in RELAY[2:])):
        print("Enter Valid Relay Input (0000-00FF)\n")
    elif not response:
        pass
    elif "ERR: -2" in response:
        print("Invalid Command\n")
    else:
        print(response[0])
        print('\n')
    
    # ===================================
    # Returns Configured Failsafe status
    # ===================================
    print("======FS GET=======")
    response = send(ser_port,"fs get")
    print(response[1])
    print('\n')


# =========================================
# Function to read the status of all relays
# =========================================
def relay_status(ser_port):
    response = send(ser_port,"relay status")
    print(response[1])
    print('\n')
    time.sleep(2.0)


# ======================================
# Function to read the info of the module
# ======================================
def device_info(ser_port):

    response = send(ser_port,"info")
    for resp in response[1:-1]:
        print(f"{resp}")
        

# ==============================
# Function to Reset failsafe
# ==============================
def failsafe_reset(ser_port):
    # ===============================================================================================================
    # After changing the state of GPI 000 to state that is opposite of failsafe
    # we can use Fs reset where we can control relays again but Fs is triggered if the failsafe condition is achieved
    # ===============================================================================================================
    send(ser_port,"fs reset")
    print("FS Reset done")
    # ========================================
    # Device Info to check FS IDLE Status
    # ========================================
    print("=======DEVICE INFO AFTER FS RESET=====")
    device_info(ser_port)

    send(ser_port,"relay on all")
    time.sleep(2.0)

    send(ser_port,"relay off all")
    time.sleep(2.0)
    
    print("Relays are controlled using Relay On all and Off all commands, it works only if fs is RESET successfully\n")


    
# ==============================
# Function to disable failsafe
# ==============================
def failsafe_disable(ser_port):

    #Disable the Failsafe
    print("======FS DISABLED======\n")
    send(ser_port,"fs disable")

    response = send(ser_port,"fs get")
    print("======FS GET After FS Disabled======")
    print(response[1])
    print('\n')
    

# =====================
# Main
# =====================
def main():

    print("Numato Lab LEOCR8 - FailSafe Sample")
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

            # ========================================
            # Device Info to check FS IDLE Status
            # ========================================
            print("=======DEVICE INFO BEFORE FS IS TRIGGERED=====")
            device_info(ser_port)

            # =============================
            # Relay Status Before FS Triggered
            # =============================
            print("=======RELAY STATUS BEFORE FS IS TRIGGERED =====")
            relay_status(ser_port)

            # =============================
            # FS Configuration
            # =============================
            print("=======FS CONFIGURATION =====")
            failsafe_enable(ser_port)

            # ========================================
            # Device Info to check FS Triggered Status
            # ========================================
            print("=======DEVICE INFO WHEN FS IS TRIGGERED =====")
            device_info(ser_port)

            # ===============================
            # Relay Status After FS Triggered
            # ===============================
            print("=======RELAY STATUS AFTER FS IS TRIGGERED =====")
            relay_status(ser_port)
            
            
            # ================================================================================
            # Uncomment the `fs reset` function only when the state
            # of GPI 000 is opposite to the state configured in the failsafe (FS) configuration.
            # The FS reset will succeed only when this condition is met.
            # =================================================================================

            #failsafe_reset(ser_port)
            
            # ========================================
            # Disable FS
            # ========================================
            failsafe_disable(ser_port)

            # ========================================
            # Device Info to check FS IDLE Status
            # ========================================
            print("=======DEVICE INFO AFTER FS DISABLE=====")
            device_info(ser_port)

        except Exception as e:
            pass

        finally:
            ser_port.close()
    
    except:
        print("PORT Not available - Check PORT Number or Device Connection")

main() 
