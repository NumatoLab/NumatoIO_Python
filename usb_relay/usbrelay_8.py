#License
#-------
#This code is published and shared by Numato Systems Pvt Ltd under GNU LGPL 
#license with the hope that it may be useful. Read complete license at 
#http://www.gnu.org/licenses/lgpl.html or write to Free Software Foundation,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
 
#Simplicity and understandability is the primary philosophy followed while
#writing this code. Sometimes at the expence of standard coding practices and
#best practices. It is your responsibility to independantly assess and implement
#coding practices that will satisfy safety and security necessary for your final
#application.
 
#This demo code demonstrates how to turn ON, OFF, read a relay.

'''Prerequisites : Python 3.x , install serial module using pip'''

import serial
 
def send_command(ser_port, command):
    """Send command to the serial port and read the response."""
    ser_port.write(command.encode())
    response = ser_port.read(25).decode()
    return response
 
def main():
    port_name = "COM1"  # Replace with your actual COM port
    baud_rate = 19200
    timeout = 1
 
    try:
        with serial.Serial(port_name, baud_rate, timeout=timeout) as ser_port:

            # Relay number
            relay_number = 4
            
            if isinstance(relay_number, int) and 0 <= relay_number <= 7:
            
                # Example 1: ON Relay 4
                relay_on_command = f"relay on {relay_number}\r"
                send_command(ser_port, relay_on_command)
                print(f"Relay {relay_number} ON successfully.")
     
                # Example 2: Read Relay 4
                relay_read_command = f"relay read {relay_number}\r"
                relay_response = send_command(ser_port, relay_read_command)
                relay_state = relay_response[-5:-3]
                print(f"Relay {relay_number} state is: {relay_state}")
                
                # Example 3: OFF Relay 4
                relay_clear_command = f"relay off {relay_number}\r"
                send_command(ser_port, relay_clear_command)
                print(f"Relay {relay_number} OFF successfully.")
                
                # Example 4: Read Relay 4
                relay_read_command = f"relay read {relay_number}\r"
                relay_response = send_command(ser_port, relay_read_command)
                relay_state = relay_response[-6:-3]
                print(f"Relay {relay_number} state is: {relay_state}")
            
            else:
                print("Error: relay_number must be one of the digits between 0 and 7.")
            
    except serial.SerialException as e:
        print(f"Error opening or communicating with serial port: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
 
if __name__ == "__main__":
    main()
