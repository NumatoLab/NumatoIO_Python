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
#   Demonstrates Relay Timer management.
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


# =============================================
# Configure the Relay Timer of your choice
# =============================================

def timer(ser_port):
    # ==================================================
    # Enter the "MODE" for timer
    # 0 ➞ DELAYED ON |  1 ➞  DELAYED OFF |  2 ➞ TOGGLE
    # ===================================================
    MODE = "2"    # enter your mode
    
    # ========================================
    # Enter the delay for the timer in seconds
    # ========================================
    DELAY = "2"   # enter your delay

    # ==================================================
    # Enter the relay number for which timer is to be set
    # ==================================================
    RELAY = "000"  # enter Relay Number

    
    #Setting timer for the specified relay
    print("===== RELAY TIMER CONFIGURATION =====")
    response = send(ser_port,f"relay tmr {RELAY} M{MODE} {DELAY}")

    if MODE == "":
        print("Enter Timer Mode\n")
    elif DELAY == "":
        print("Enter Timer Delay\n")
    elif RELAY == "":
        print("Enter Relay Number\n")
    elif MODE not in ["0" ,"1", "2"]:
        print("Enter Valid MODE\n")
    elif not response:
        pass
    elif "ERR: -2" in response:
        print("Invalid Command\n")
    elif "ERR: -51" in response:
        print("Invalid Delay\n")
    else:
        print(response[0])
        print('\n')
        

    # Returns the timer active Relays
    print("===== TIMER GET =====")
    response = send(ser_port,"relay tmr get")
    print(response[1])
    print("\n")

    # Returns the timer mode and delay set for the specified relay when timer is active
    print("===== TIMER GET - DETAILED =====")
    response = send(ser_port, f"relay tmr get {RELAY}")

    if RELAY == "":
        print("Enter Relay Number\n")
    elif "ERR: -2" in response:
        print("Invalid Command\n")
    else:
        print(response[1])

    print("Note:  Timer details are displayed only while the timer is active during the configured delay.")
    print( "Once the delay has elapsed, the timer will become inactive\n")
 

# ===================================== 
# Function to Disable the Relay Timers
# ====================================

def timer_disable(ser_port):
    RELAY = "000"
    # Disables the relay timer for the specified relay number
    # send(ser_port,f"relay tmr disable {RELAY}")
    
    print("===== TIMER Disabled =====\n")
    #Disable timer for all relays
    send(ser_port,"relay tmr disable")
    #Returns the relay numbers having timer if no timer is active displays no active timers
    print("===== TIMER GET - After Disable =====")
    response = send(ser_port,"relay tmr get")
    print(response[1])
    print('\n')

  
# ===============================
# Main
# ===============================
def main():

    print("Numato Lab LEOCR8 - Relay Timer Sample")
    print("----------------------------------------")
    print(f"Device COM Port: {PORT}")
    print()
    
    try:
        # ============================
        # Open COM Port
        # ============================
        ser_port = serial.Serial(port = PORT,baudrate=BAUDRATE,timeout=TIMEOUT)
        try:
            # ====================
            # Login
            # =====================
            if authentication(ser_port) is False:
                raise Exception


            # ======================
            # Timer Configuration
            # ======================
            timer(ser_port)

            # ================================================
            # Timer Disable 
            # ================================================
            timer_disable(ser_port)
            
        except Exception as e:
            pass
        
        finally:
            ser_port.close()
    except:
        print("PORT Not available - Check PORT Number or Device Connection\n")



main()   
