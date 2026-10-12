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
#   Demonstrates Relay Control and monitor.
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


def relay(ser_port):
    """
    Function to read and write relay states using
    single and group commands.
    """
    # ====================================================
    # Enter the relay number which you want to turn ON/OFF
    # ====================================================
    print("===== INDIVIDUAL RELAY CONTROL =====\n")
    RELAY = "007"  # enter Relay number

    
    if RELAY in [f"{i:03d}" for i in range(8)]:
        try:
            # =================================
            # Turns ON the Relay of your choice
            # =================================
            print(f"TURNS ON Relay {RELAY}")
            send(ser_port,f"relay on {RELAY}\n")

            # ===========================================
            # Read the status of the Relay of your choice
            # ===========================================
            print(f"READS Relay {RELAY} STATUS ")
            response = send(ser_port,f"relay status {RELAY}")
            print(f"Relay {RELAY}:{response[1]}\n")
  
            # =================================
            # Turns ON the Relay of your choice
            # =================================
            if RELAY in [f"{i:03d}" for i in range(8)]:
                print(f"TURNS OFF Relay {RELAY}")
                send(ser_port,f"relay off {RELAY}\n")

            # ===========================================
            # Read the status of the Relay of your choice
            # ===========================================
            print(f"READS Relay {RELAY} STATUS")
            response = send(ser_port,f"relay status {RELAY}")
            print(f"Relay {RELAY}:{response[1]}\n")

        except:
            pass

    else:
        print("****** Enter Valid Input 000-007 *******\n")

    
   # ==============================================
   # Enter the hexadecimal value to turn ON/OFF
   # one or more relays.
   # ==============================================

    print("===== RELAY CONTROL USING WRITE COMMAND =====\n")
    writevalue = "00AA"  # enter input (0000 - 00FF)
    print("Relay Control Using WRITE Command")
    if len(writevalue) == 4 and writevalue[:2] == "00" and all(c in "0123456789ABCDEFabcdef" for c in writevalue[2:]):
        send(ser_port,f"relay write A {writevalue}")
        print(f"Write Input: {writevalue}\n")
    else:
        print("*******Enter Valid Input 0000-00FF*******\n")

   # =========================================
   # Reads the status of all relays and returns
   # the result as a hexadecimal value.
   # ==========================================
    print(f"READS All Relay STATUS AFTER WRITE COMMAND")
    response = send(ser_port,"relay status")
    print(f"Relay Status: {response[1]}\n")

   # ========================
   # Turns ON All the Relays
   # ========================
    print("===== ALL RELAY CONTROL=====\n")
    print("TURNS ON ALL THE RELAYS")
    send(ser_port,"relay on all")

   # =========================================
   # Reads the status of all relays and returns
   # the result as a hexadecimal value.
   # ==========================================
    response = send(ser_port,"relay status")
    print(f"Relay Status: {response[1]}\n")

    
   # ========================
   # Turns OFF All the Relays
   # ========================
    print("TURNS OFF ALL THE RELAYS")
    send(ser_port,"relay off all")

    
   # =========================================
   # Reads the status of all relays and returns
   # the result as a hexadecimal value.
   # ==========================================
    response = send(ser_port,"relay status") 
    print(f"Relay Status: {response[1]}\n")


# ========================================================
# Function to read and write relay power-on commands.

# When the board is powered on, the relays specified by
# the power-on value (pwron_value) will automatically turn ON
# after each power cycle.
# ===========================================================
def pwron(ser_port):
    
    # =================================
    # Returns the relay power-on value.
    # ==================================
    print("===== RELAY POWERON CONTROL =====\n")
    print("CURRENT RELAY POWERON-CONDITION")
    response = send(ser_port,"relay pwron get")
    print(f"Relay Poweron Status: {response[1]}\n")

    # ===============================================================
    # Enter the hexadecimal value to turn ON/OFF
    # one or more relays after each power cycle.
    # ===============================================================
    
    pwron_value = "00FF"  # enter input (0000 - 00FF)
    if len(pwron_value) == 4 and pwron_value[:2] == "00" and all(c in "0123456789ABCDEFabcdef" for c in pwron_value[2:]):
        print("UPDATING RELAY POWERON-CONDITION")
        send(ser_port,f"relay pwron A {pwron_value}")
        print(f"POWERON INPUT: {pwron_value}\n")
    else:
        print("*****Enter Valid Input 0000-00FF******\n")
    

    # =================================
    # Returns the relay power-on value.
    # ==================================
    print("UPDATED RELAY POWERON-CONDITION ")
    response = send(ser_port,"relay pwron get")
    print(f"Relay Poweron Status: {response[1]}\n")


# ===================================================
#   Function to Disable the Power-on Feature
#   Upon Disable the Poweron will be set at A:0000
# ====================================================   
def pwron_disable(ser_port):
    
    # Disables the power-on feature by writing the value 0000
    
    send(ser_port,"relay pwron disable")
    print("DISABLED POWERON-CONDITION")

    #Returns the power-on value
    response= send(ser_port,"relay pwron get")
    print(f"Relay Poweron Status after disable: {response[1]}\n")

# ====================================================
# Function to read GPI using single and group commands
# along with gpi notify commands
# ====================================================
def gpi(ser_port):
    
    # ===================================
    # Enter the GPI number of your choice
    # ===================================
    GPI = "000"  # enter GPI number
    print("===== INDIVIDUAL GPI READ =====\n")

    # =================================== 
    # Reads the status of  specific GPI
    # ===================================
    if GPI in [f"{i:03d}" for i in range(8)]:
        response = send(ser_port,f"gpi read {GPI}")
        print(f"READS DIGITAL INPUT {GPI} STATUS")
        print(f"GPI {GPI}:{response[1]}\n")
    else:
        print("*****Enter Valid Input 000-007******\n")

    # ===========================================================
    # Reads the status of all GPI and returns a hexadecimal value
    # ===========================================================
    print("===== ALL GPI READ =====\n")
    response = send(ser_port,"gpi read")
    print("READS ALL DIGITAL INPUTS STATUS")
    print(f"GPI Status:{response[1]}\n")

    # ======================================================
    # Reads the GPI notification status (enabled or disabled)
    # ======================================================
    print("===== GPI NOTIFICATION =====\n")
    print("DIGITAL INPUT NOTIFICATION STATUS")
    response = send(ser_port, "gpi notify get")
    print(response[1])
    print("\n")
    
    # =====================================================
    # Enables GPI notification to report GPI state changes
    # in the format: Previous State / Current State
    # =====================================================
    print("TURNS ON DIGITAL INPUTS NOTIFICATION")
    response = send(ser_port, "gpi notify on")
    print(response[1])
    print("\n")

    # =========================
    # Disables GPI notification
    # =========================
    print("TURNS OFF DIGITAL INPUTS NOTIFICATION")
    response = send(ser_port, "gpi notify off")
    print(response[1])
    print("\n")
    
# ===============================
# Main
# ===============================
def main():

    print("Numato Lab LEOCR8 - Peripherals Control & Status Sample")
    print("--------------------------------------------------------")
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
            # Relay Control
            # ======================
            relay(ser_port)

            # =========================
            # Relay Power-On Condition
            # =========================
            pwron(ser_port)

            # =======================
            # Relay Power-On Disable
            # ========================
            pwron_disable(ser_port)

            # ========================================
            # Digital Inputs Status and Notify Control
            # ========================================
            gpi(ser_port)

        except Exception as e:
            pass

        finally:
            ser_port.close()
    except:
        print("PORT Not available - Check PORT Number or Device Connection")



main()
