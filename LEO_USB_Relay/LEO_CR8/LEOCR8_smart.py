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
#   Demonstrates standalone automation management Smart Action Feature.
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
        return True

        

# =============================================
# Configure the smart action of your choice
# =============================================

def smart(ser_port):

    # =====================================
    # Enter the "MODE" for smart action
    # L ➞ LOW |  H ➞ HIGH  |  F ➞ FOLLOW
    # =====================================
    MODE = "L"     # enter mode

    # ==============================================
    # If MODE is H/L specify the state of relay 1/0
    # ==============================================
    STATE = "1"    # enter Relay state

    # =====================================================
    # Enter the DI pin number to which relay will be mapped
    # =====================================================
    DI = "000"    # enter DI number

    # =============================================
    # Enter the relay number you wish to map to DI
    # =============================================
    RELAY = "000"  # enter Relay number


    

    if MODE == "F":
        print("===== SMART CONFIGURATION =====")
        response=send(ser_port,f"smart {DI} {MODE} {RELAY}")
        if not response:
            pass
        elif "ERR: -2" in response:
            print("Invalid Command\n")
        elif "ERR: -41" in response:
            print("Invalid Condition\n")
        elif RELAY == "":
            print("Enter Relay Number\n")
        elif DI == "":
            print("Enter DI Number\n")
        else:
            print(response[0])
            print('\n')
        
    elif MODE == "H" or MODE == "L":
        print("===== SMART CONFIGURATION =====")
        response=send(ser_port,f"smart {DI} {MODE} {RELAY} {STATE}")
        if STATE == "":
            print("Enter Relay State\n")
        if STATE not in ["0" ,"1"]:
            print("Enter Valid State\n")
        elif not response:
            pass
        elif "ERR: -2" in response:
            print("Invalid Command\n")
        elif "ERR: -41" in response:
            print("Invalid Condition\n")
        elif RELAY == "":
            print("Enter Relay Number\n")
        elif DI == "":
            print("Enter DI Number\n")
        else:
            print(response[0])
            print('\n')

    elif MODE == "":
        print("Enter MODE\n")
    else:
        print("Enter Valid MODE\n")


    #Returns all the DI mapped with smart action
    print("===== SMART GET =====")
    response = send(ser_port,"smart get")
    print(response[1])
    print('\n')
    

    #Returns the detailed data mapped with the specified input
    print("===== SMART GET - DETAILED =====")
    response = send(ser_port,f"smart get {DI}")
    if "ERR: -2" in response:
            print("Invalid Command\n")
    elif DI == "":
            print("Enter DI Number\n")
    else:
        print(response[1])
        print('\n')



def smart_disable(ser_port):

    print("===== SMART DISABLE =====\n")

    send(ser_port,"smart disable")

  # ================================================================================
  #  We can disable the smart action for a particular relay or Digital Input
  #  using smart -i {DI_no} to disable the smart action for a specific Digital Input
  #  and smart -r {Relay_no} to disable the smart action for a specific Relay
  # ================================================================================

  #Returns all the DI mapped with smart action
    print("===== SMART GET AFTER SMART DISABLE =====")
    response = send(ser_port,"smart get")
    print(response[1])
    print('\n')
    

  
# ===============================
# Main
# ===============================
def main():

    
    print("Numato Lab LEOCR8 - Smart Action Sample")
    print("----------------------------------------")
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

            # ======================
            # Smart Configuration
            # ======================

            smart(ser_port)

            # ================================================
            # Smart Disable 
            # ================================================
            smart_disable(ser_port)

        except Exception as e:
            pass
        
        finally:
            ser_port.close()
    except:
        print("PORT Not available - Check PORT Number or Device Connection\n")


main()    
